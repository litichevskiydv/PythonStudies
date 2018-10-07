import os
import numpy as np
from sklearn.metrics import accuracy_score


def main():
    passes_values = [1, 3, 5]
    ngram_values = [1, 2, 3]

    best_score = -1
    best_passes = 0
    best_ngram = 0
    for passes in passes_values:
        for ngram in ngram_values:
            train_command = 'vw --oaa 10 -d stackoverflow_train.vw -f vw_model_passes_{0}_ngram_{1}.vw -b 28 --loss_function hinge --random_seed 17 --quiet --passes {0} --ngram {1}{2}'.format(passes, ngram, ' -c -k' if passes > 1 else '')
            print(train_command)
            os.system(train_command)

            predict_command = 'vw -t -i vw_model_passes_{0}_ngram_{1}.vw -d stackoverflow_valid.vw -p vw_predict_passes_{0}_ngram_{1}.csv --random_seed 17 --quiet'.format(passes, ngram)
            print(predict_command)
            os.system(predict_command)

            vw_pred = np.loadtxt('vw_predict_passes_{0}_ngram_{1}.csv'.format(passes, ngram))
            valid_labels = np.loadtxt('stackoverflow_valid_labels.txt')
            score = accuracy_score(valid_labels, vw_pred)
            print('Passes: {0}, ngram: {1}, score: {2}'.format(passes, ngram, score))

            if score > best_score:
                best_score = score
                best_passes = passes
                best_ngram = ngram

    print('Best passes: {0}, best ngram: {1}, best score: {2}'.format(best_passes, best_ngram, best_score))


if __name__ == '__main__':
    main()
