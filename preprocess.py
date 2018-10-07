import argparse
from tqdm import tqdm


def to_vw_format(label, text):
    return str(label) + ' | ' + text.replace(':', '').replace('|', '') + '\n'


def main():
    parser = argparse.ArgumentParser(add_help=True, description='Convert raw data')
    parser.add_argument('input_file_path')
    parser.add_argument('output_file_path')
    args = parser.parse_args()

    tags = ['javascript', 'java', 'python', 'ruby', 'php', 'c++', 'c#', 'go', 'scala', 'swift']
    selected_rows_count = 0
    bad_rows_count = 0

    with open(args.input_file_path, encoding='utf-8') as input_file:
        with open(args.output_file_path, 'w') as output_file:
            for line in tqdm(input_file):
                if line.count('\t') != 1:
                    bad_rows_count += 1
                    continue

                article_text, article_tags = line.split('\t')
                article_text = article_text.strip()
                article_tags = article_tags.rstrip().split(' ')
                if len(article_text) == 0 or len(article_tags) == 0:
                    bad_rows_count += 1
                    continue

                article_tags_indexes = []
                for i in range(0, len(tags)):
                    if tags[i] in article_tags:
                        article_tags_indexes.append(i + 1)
                if len(article_tags_indexes) != 1:
                    continue

                output_file.write(to_vw_format(article_tags_indexes[0], article_text))
                selected_rows_count += 1

    print('{0} lines selected, {1} lines corrupted.'.format(selected_rows_count, bad_rows_count))


if __name__ == '__main__':
    main()
