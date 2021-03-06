import sys
import os

import matplotlib.pyplot as plt
import numpy as np
from shallowlearn.models import FastText
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

module_path = os.path.abspath(os.getcwd()).replace('/src', '')

if module_path not in sys.path:
    sys.path.append(module_path)

from src import calc_wrapper
from src.confusion import plot_confusion_matrix
from src.consts import plotFormat, dpi, plot_save_path
from src.method import bowMethod
from src.method import fastTextMethod
from src.xml_reader import read_stop_words_list

svm_clf = LinearSVC()
dt_clf = DecisionTreeClassifier()
nb_clf = MultinomialNB()
ft_clf = FastText(dim=7, min_count=15, loss='ns', epoch=200, bucket=200000, word_ngrams=1)

stop_words_list = read_stop_words_list()
d_vectorizer = TfidfVectorizer(stop_words=stop_words_list)


def show_confusion_matrix(y_test, y_pred, class_names, file_name, title, korpus_name):
    cnf_matrix = confusion_matrix(y_test, y_pred)
    plt.figure()
    title = title + ' - ' + korpus_name
    plot_confusion_matrix(cnf_matrix, classes=class_names, title=title)
    file_name = file_name + '-' + korpus_name
    plt.savefig(plot_save_path + 'c-matrix-' + file_name.lower().replace(' ', '-').replace('ł', 'l') + "." + plotFormat,
                dpi=dpi,
                format=plotFormat, bbox_inches='tight')
    plt.show()


def draw_fit_time_plot(ax_samples, korpus_name):
    plt.plot(ax_samples, ft_fit_times, 'c-+', label="fastText (zmodyfikowany)")
    plt.plot(ax_samples, nb_fit_times, 'r-*', label="NaiveBayes + BoW")
    plt.plot(ax_samples, svm_fit_times, 'g-^', label="SVM + BoW")
    plt.plot(ax_samples, dt_fit_times, 'b-s', label="Drzewo decyzyjne + BoW")
    plt.grid(color='tab:gray', linestyle='-', linewidth=0.15)
    plt.ylabel('czas [s]')
    plt.xlabel('liczba próbek')
    title = 'Czas nauki - ' + korpus_name
    plt.title(title)
    plt.legend()
    plt.ylim(0, 13) #8
    plt.savefig(plot_save_path +
                'fit-time-' +
                korpus_name.lower().replace(' ', '-').replace('ł', 'l') + "." + plotFormat, dpi=dpi,
                format=plotFormat)
    plt.show()


def draw_predict_time_plot(ax_samples, korpus_name):
    plt.plot(list(reversed(ax_samples)), list(reversed(ft_predict_times)), 'c-+', label="fastText (zmodyfikowany)")
    plt.plot(list(reversed(ax_samples)), list(reversed(nb_predict_times)), 'r-*', label="NaiveBayes + BoW")
    plt.plot(list(reversed(ax_samples)), list(reversed(svm_predict_times)), 'g-^', label="SVM + BoW")
    plt.plot(list(reversed(ax_samples)), list(reversed(dt_predict_times)), 'b-s', label="Drzewo decyzyjne + BoW")
    plt.grid(color='tab:gray', linestyle='-', linewidth=0.15)
    plt.ylabel('czas [s]')
    plt.xlabel('liczba próbek')
    title = 'Czas klasyfikacji - ' + korpus_name
    plt.title(title)
    plt.legend()
    plt.ylim(0, 2.5) # 1.5
    plt.savefig(plot_save_path +
                'predict-time-' +
                korpus_name.lower().replace(' ', '-').replace('ł', 'l') + "." + plotFormat, dpi=dpi,
                format=plotFormat)
    plt.show()


def draw_time_plot(ax_samples, korpus_name):
    plt.plot(ax_samples, ft_times, 'c-+', label="fastText (zmodyfikowany)")
    plt.plot(ax_samples, nb_times, 'r-*', label="NaiveBayes + BoW")
    plt.plot(ax_samples, svm_times, 'g-^', label="SVM + BoW")
    plt.plot(ax_samples, dt_times, 'b-s', label="Drzewo decyzyjne + BoW")
    plt.grid(color='tab:gray', linestyle='-', linewidth=0.15)
    plt.ylabel('czas [s]')
    plt.xlabel('liczba próbek')
    title = 'Całkowity czas pracy - ' + korpus_name
    plt.title(title)
    plt.ylim(0, 13)
    plt.legend()
    plt.savefig(plot_save_path + 'total-work-time-' +
                korpus_name.lower().replace(' ', '-').replace('ł',
                                                              'l') + "." + plotFormat,
                dpi=dpi,
                format=plotFormat)
    plt.show()


def draw_accuracy_plot(ax_samples, korpus_name):
    plt.plot(ax_samples, ft_accuracies, 'c-+', label="fastText (zmodyfikowany)")
    plt.plot(ax_samples, nb_accuracies, 'r-*', label="NaiveBayes + BoW")
    plt.plot(ax_samples, svm_accuracies, 'g-^', label="SVM + BoW")
    plt.plot(ax_samples, dt_accuracies, 'b-s', label="Drzewo decyzyjne + BoW")
    plt.grid(color='tab:gray', linestyle='-', linewidth=0.15)
    plt.ylabel('dokładność')
    plt.xlabel('liczba próbek')
    plt.ylim(0, 1)
    title = 'Dokładność - ' + korpus_name
    plt.title(title)
    plt.legend()
    plt.savefig(plot_save_path + 'accuracy-' +
                korpus_name.lower().replace(' ', '-').encode("ascii", errors="ignore").decode()
                + "." + plotFormat,
                dpi=dpi,
                format=plotFormat)
    plt.show()


def accuracy_time_report(train_sizes, iterations, korpus_path, korpus_name):
    global train_samples_array, test_samples_array, ft_accuracies, nb_accuracies, svm_accuracies, dt_accuracies, ft_fit_times, nb_fit_times, svm_fit_times, dt_fit_times, ft_predict_times, nb_predict_times, svm_predict_times, dt_predict_times, ft_times, nb_times, svm_times, dt_times
    train_samples_array = []
    test_samples_array = []
    ft_accuracies = []
    nb_accuracies = []
    svm_accuracies = []
    dt_accuracies = []
    ft_fit_times = []
    nb_fit_times = []
    svm_fit_times = []
    dt_fit_times = []
    ft_predict_times = []
    nb_predict_times = []
    svm_predict_times = []
    dt_predict_times = []
    ft_times = []
    nb_times = []
    svm_times = []
    dt_times = []

    files_data = load_files(korpus_path, encoding='utf-8')

    step = 0  # do obliczania % ukonczenia
    for train_size in train_sizes:
        X_train, X_test, y_train, y_test = train_test_split(
            files_data.data,
            files_data.target,
            train_size=train_size,
            test_size=1 - train_size)

        test_samples_count = len(X_test)
        train_samples_count = len(X_train)
        train_samples_array.append(train_samples_count)
        test_samples_array.append(test_samples_count)

        print('Calculating... train:', str(train_samples_count), '| test:', str(test_samples_count))

        # learning curve
        ft_accuracy, ft_fit_time, ft_predict_time = calc_wrapper.start_test(
            iterations, y_test, fastTextMethod.learn_predict, (X_train, X_test, y_train, ft_clf))

        nb_accuracy, nb_fit_time, nb_predict_time = calc_wrapper.start_test(
            iterations, y_test, bowMethod.learn_predict, (X_train, X_test, y_train, nb_clf, d_vectorizer))

        svm_accuracy, svm_fit_time, svm_predict_time = calc_wrapper.start_test(
            iterations, y_test, bowMethod.learn_predict, (X_train, X_test, y_train, svm_clf, d_vectorizer))

        dt_accuracy, dt_fit_time, dt_predict_time = calc_wrapper.start_test(
            iterations, y_test, bowMethod.learn_predict, (X_train, X_test, y_train, dt_clf, d_vectorizer))

        ft_fit_times.append(ft_fit_time)
        nb_fit_times.append(nb_fit_time)
        svm_fit_times.append(svm_fit_time)
        dt_fit_times.append(dt_fit_time)

        ft_predict_times.append(ft_predict_time)
        nb_predict_times.append(nb_predict_time)
        svm_predict_times.append(svm_predict_time)
        dt_predict_times.append(dt_predict_time)

        ft_times.append(ft_fit_time + ft_predict_time)
        nb_times.append(nb_fit_time + nb_predict_time)
        svm_times.append(svm_fit_time + svm_predict_time)
        dt_times.append(dt_fit_time + dt_predict_time)

        ft_accuracies.append(ft_accuracy)
        nb_accuracies.append(nb_accuracy)
        svm_accuracies.append(svm_accuracy)
        dt_accuracies.append(dt_accuracy)

        # draw plots
        draw_accuracy_plot(train_samples_array, korpus_name)
        draw_fit_time_plot(train_samples_array, korpus_name)
        draw_predict_time_plot(test_samples_array, korpus_name)
        draw_time_plot(train_samples_array, korpus_name)
        step += 1
        print("Finished:", format((step / len(train_sizes)) * 100, '.2f') + "%")


def cls_report(korpus_path, korpus_name):
    train_size = 0.3
    X_test, X_train, y_test, y_train, files_data = load_string_korpus(korpus_path, train_size)
    target_names = files_data.target_names
    iter = 1

    # calc_wrapper.report_data(
    #     'fastText - ' + korpus_name, iter, y_test, target_names, fastTextMethod.learn_predict,
    #     (X_train, X_test, y_train, ft_clf))
    # calc_wrapper.report_data(
    #     'NaiveBayes - ' + korpus_name, iter, y_test, target_names, bowMethod.learn_predict,
    #     (X_train, X_test, y_train, nb_clf, d_vectorizer))
    # calc_wrapper.report_data(
    #     'SVM - ' + korpus_name, iter, y_test, target_names, bowMethod.learn_predict,
    #     (X_train, X_test, y_train, svm_clf, d_vectorizer))
    # calc_wrapper.report_data(
    #     'Drzewo decyzyjne - ' + korpus_name, iter, y_test, target_names, bowMethod.learn_predict,
    #     (X_train, X_test, y_train, dt_clf, d_vectorizer))

    # confusion matrix
    # y_pred_ft, fit_time, predict_time = fastTextMethod.learn_predict(X_train, X_test, y_train, ft_clf)
    # show_confusion_matrix(y_test, y_pred_ft, target_names, 'fasttext', 'fastText', korpus_name)
    #
    # y_pred_nb, fit_time, predict_time = bowMethod.learn_predict(X_train, X_test, y_train, nb_clf, d_vectorizer)
    # show_confusion_matrix(y_test, y_pred_nb, target_names, 'naivebayes', 'NaiveBayes', korpus_name)
    #
    # y_pred_svm, fit_time, predict_time = bowMethod.learn_predict(X_train, X_test, y_train, svm_clf,
    #                                                              d_vectorizer)
    # show_confusion_matrix(y_test, y_pred_svm, target_names, 'svm', 'SVM', korpus_name)

    y_pred_dt, fit_time, predict_time = bowMethod.learn_predict(X_train, X_test, y_train, dt_clf, d_vectorizer)
    show_confusion_matrix(y_test, y_pred_dt, target_names, 'decisiontree', 'Drzewo decyzyjne', korpus_name)


def load_string_korpus(korpus_path, train_size):
    files_data = load_files(korpus_path, encoding='utf-8')
    X_train, X_test, y_train, y_test = train_test_split(
        files_data.data,
        files_data.target,
        train_size=train_size,
        test_size=1 - train_size)
    return X_test, X_train, y_test, y_train, files_data


def start_tests():
    iterations_wiki = 3
    iterations_articles = 5
    train_sizes_wiki = np.arange(0.01, 0.51, 0.06)
    train_sizes_articles = np.arange(0.01, 0.51, 0.03)

    wiki_data_sets = [('Wikipedia', "../data/wiki/lemma", iterations_wiki, train_sizes_wiki),
                      ('Wikipedia (rzeczowniki)', "../data/wiki/noun", iterations_wiki, train_sizes_wiki)]

    article_data_sets = [('Artykuły', "../data/korpus/lemma", iterations_articles, train_sizes_articles),
                         ('Artykuły (rzeczowniki)', "../data/korpus/noun", iterations_articles, train_sizes_articles)]

    data_sets = []

    argument_data_set = sys.argv[1:]
    if 'w' in argument_data_set:
        print("loading Wikipedia data set only")
        data_sets = wiki_data_sets

    if 'a' in argument_data_set:
        print("loading Articles data set only")
        data_sets = article_data_sets

    if len(sys.argv) < 2:
        print("loading full data set")
        data_sets = article_data_sets + wiki_data_sets

    for korpus_name, korpus_path, iter_size, train_size in data_sets:
        print('Korpus name: %s' % korpus_name)
        accuracy_time_report(train_size, iter_size, korpus_path, korpus_name)
        # cls_report(korpus_path, korpus_name)


start_tests()
