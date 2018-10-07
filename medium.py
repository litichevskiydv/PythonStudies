import os
import json
import re
import argparse
from tqdm import tqdm
import numpy as np
import pandas as pd
from datetime import datetime
from html.parser import HTMLParser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from scipy.sparse import csr_matrix, hstack
from sklearn.linear_model import Ridge


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def read_json_line(line=None):
    result = None
    try:
        result = json.loads(line)
    except Exception as e:
        # Find the offending character index:
        idx_to_replace = int(str(e).split(' ')[-1].replace(')', ''))
        # Remove the offending character:
        new_line = list(line)
        new_line[idx_to_replace] = ' '
        new_line = ''.join(new_line)
        return read_json_line(line=new_line)
    return result


def prepare_features(path_to_data, is_train, authors_dict, authors_scaler, title_vectorizer, content_vectorizer,
                     reading_time_scaler):
    prefix = 'train' if is_train else 'test'

    features = ['content', 'published', 'title', 'author', 'meta_tags']
    features_lists = [[] for x in features]
    with open(os.path.join(path_to_data, '{0}.json'.format(prefix)), encoding='utf-8') as json_input_file:
        for line in tqdm(json_input_file):
            json_data = read_json_line(line)
            for i in range(0, len(features)):
                feature = features[i]
                data = json_data[feature]

                if feature == 'published':
                    data = datetime.strptime(data['$date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                elif feature == 'author':
                    data = data['url'].split('@')[1].upper()
                    if data not in authors_dict and is_train:
                        authors_dict[data] = len(authors_dict) + 1
                    data = authors_dict[data] if data in authors_dict else 0
                elif feature == 'meta_tags':
                    data = np.log1p(float(re.findall('(\\d+) min read', data['twitter:data1'])[0]))
                else:
                    data = data.replace('\n', ' ').replace('\r', ' ')
                    data = strip_tags(data)

                features_lists[i].append(data)

    authors_ids = np.reshape(features_lists[features.index('author')], newshape=(-1, 1))
    if is_train:
        authors_feature = authors_scaler.fit_transform(authors_ids)
    else:
        authors_feature = authors_scaler.transform(authors_ids)

    publish_dates = features_lists[features.index('published')]
    publish_dates_df = pd.DataFrame(publish_dates, index=np.arange(1, len(publish_dates) + 1), columns=['published'])

    titles = features_lists[features.index('title')]
    if is_train:
        titles_feature = title_vectorizer.fit_transform(titles)
    else:
        titles_feature = title_vectorizer.transform(titles)

    contents = features_lists[features.index('content')]
    if is_train:
        contents_feature = content_vectorizer.fit_transform(contents)
    else:
        contents_feature = content_vectorizer.transform(contents)

    reading_times = np.reshape(features_lists[features.index('meta_tags')], newshape=(-1, 1))
    if is_train:
        reading_times_feature = reading_time_scaler.fit_transform(reading_times)
    else:
        reading_times_feature = reading_time_scaler.transform(reading_times)

    return authors_feature, publish_dates_df, titles_feature, contents_feature, reading_times_feature


def prepare_publish_date_features(df):
    df['year'] = df['published'].apply(lambda x: x.year)
    df['month'] = df['published'].apply(lambda x: x.month)
    df['day'] = df['published'].apply(lambda x: x.day)
    df['dow'] = df['published'].apply(lambda x: x.weekday())
    df['tod'] = df['published'].apply(lambda x: x.hour)

    df['is_year_other'] = df['year'].apply(lambda x: 1 if x < 2012 else 0)
    df['is_year_2012'] = df['year'].apply(lambda x: 1 if x == 2012 else 0)
    df['is_year_2013'] = df['year'].apply(lambda x: 1 if x == 2013 else 0)
    df['is_year_2014'] = df['year'].apply(lambda x: 1 if x == 2014 else 0)
    df['is_year_2015'] = df['year'].apply(lambda x: 1 if x == 2015 else 0)
    df['is_year_2017'] = df['year'].apply(lambda x: 1 if x == 2017 else 0)

    df['is_weekend'] = df['dow'].apply(lambda x: 1 if x in (5, 6) else 0)

    df['is_night'] = df['tod'].apply(lambda x: 1 if 23 <= x <= 24 or 0 <= x < 8 else 0)
    df['is_morning'] = df['tod'].apply(lambda x: 1 if 8 <= x < 11 else 0)
    df['is_day'] = df['tod'].apply(lambda x: 1 if 11 <= x < 19 else 0)

    time_bool_features = df[
        ['is_year_other', 'is_year_2012', 'is_year_2013', 'is_year_2014', 'is_year_2015', 'is_year_2017', 'is_weekend',
         'is_night', 'is_morning', 'is_day']]
    time_categorical_features = OneHotEncoder(n_values=[12, 24]).fit_transform(df[['month', 'tod']])
    return hstack([time_bool_features, time_categorical_features]).tocsr()


def write_submission_file(prediction, path_to_data, filename):
    path_to_sample = os.path.join(path_to_data, 'sample_submission.csv')
    submission = pd.read_csv(path_to_sample, index_col='id')

    submission['log_recommends'] = prediction
    submission.to_csv(os.path.join(path_to_data, filename))


def main():
    parser = argparse.ArgumentParser(add_help=True, description='Compute solution for Medium competition')
    parser.add_argument('--path_to_data', default=os.getcwd(), help='Path to files with data')
    args = parser.parse_args()

    path_to_data = args.path_to_data

    authors_dict = {}
    authors_scaler = OneHotEncoder(handle_unknown='ignore')
    title_vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=100000, sublinear_tf=True)
    content_vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=100000, sublinear_tf=True)
    reading_time_scaler = StandardScaler()

    (train_authors, train_publish, train_titles, train_contents, train_reading_times) = prepare_features(path_to_data, True, authors_dict, authors_scaler, title_vectorizer, content_vectorizer, reading_time_scaler)
    (test_authors, test_publish, test_titles, test_contents, test_reading_times) = prepare_features(path_to_data, False, authors_dict, authors_scaler, title_vectorizer, content_vectorizer, reading_time_scaler)
    train_target = pd.read_csv(os.path.join(path_to_data, 'train_log1p_recommends.csv'), index_col='id')

    y_train = train_target['log_recommends'].values
    x_train_sparse = csr_matrix(hstack(
        [train_contents, train_titles, train_authors, prepare_publish_date_features(train_publish),
         train_reading_times]))
    x_test_sparse = csr_matrix(hstack(
        [test_contents, test_titles, test_authors, prepare_publish_date_features(test_publish), test_reading_times]))

    ridge = Ridge(alpha=1.2, random_state=17)
    ridge.fit(x_train_sparse, y_train)

    ridge_test_pred = ridge.predict(x_test_sparse)
    avg = np.mean(ridge_test_pred)
    ridge_test_pred = list(map(lambda x: x - avg + 4.33328, ridge_test_pred))

    write_submission_file(ridge_test_pred, path_to_data, 'assignment6_medium_submission.csv')


if __name__ == '__main__':
    main()
