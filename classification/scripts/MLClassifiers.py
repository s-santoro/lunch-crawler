#!/usr/bin/env python
# coding: utf-8

# Imports
from luigi.contrib.spark import PySparkTask
from luigi.parameter import IntParameter
from luigi import LocalTarget, Task, WrapperTask
from luigi.format import UTF8
import datetime
import pandas as pd
import numpy as np
import re
import os
from configs.Configurations import Configurations

'''bigrams'''
from DataVisualizer import DataVisualizer

'''Features'''
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MaxAbsScaler

'''Classifiers'''
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier

from sklearn.svm import LinearSVC
from sklearn.linear_model import RidgeClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import BernoulliNB, ComplementNB, MultinomialNB, GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid

'''Metrics/Evaluation'''
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from scipy import interp
from itertools import cycle

'''Plotting'''
import matplotlib.pyplot as plt
import seaborn as sns

class MLClassifiers(Task):
    # Date for Output-File prefix
    from datetime import date
    date = datetime.datetime.now()
    configId = IntParameter(default=0)

    # Method to declare the Output-File
    def output(self):
        prefix = self.date.strftime("%Y-%m-%dT%H%M%S")
        return LocalTarget("../data/%s_configID_%s_MLClassifiers.csv" % (prefix, self.configId), format=UTF8)

    # Method to define the required Task (Importer)
    def requires(self):
        return DataVisualizer(self.configId)

    # Prepare prprocessed data for ML evaluation
    def run(self):
        # use configID from commandline
        configs = Configurations().configs[self.configId]
        eval_dict = {}

        # parameters for config
        holdout = 20
        prefix = self.date.strftime("%Y-%m-%dT%H%M%S")
        # train test split
        test_size = configs.get("test_size")
        shuffle = configs.get("shuffle")
        random_state = configs.get("random_state")
        # bag of words
        max_features = configs.get("maxFeatures")
        # tfidf
        ngram_range = configs.get("ngram_range")
        min_df = configs.get("min_df")
        max_df = configs.get("max_df")
        # dimension reduction (truncated svd)
        n_components = configs.get("n_components")
        n_iter = configs.get("n_iter")

        input_df = pd.read_csv(self.input().path)
        cleaned_df = pd.DataFrame(columns=('text', 'cleaned_text', 'url', 'title', 'class'))

        # convert document['cleaned_text'] from string to list of words
        for index, document in input_df.iterrows():
            text = document['cleaned_text']
            text = re.sub(r"[',\[\]]", "", text)
            wordlist = text.split(" ")
            row = [document.text, wordlist, document.url, document.title, document['class']]
            cleaned_df.loc[index] = row

        # Preparing the dataframes
        # Splitting the df into the different classes
        df_menu = cleaned_df.loc[cleaned_df['class'] == 1]
        df_no_menu = cleaned_df.loc[cleaned_df['class'] == 0]

        # Holding out 10 articles from each class for prediction at the end
        df_menu_holdout = df_menu.iloc[:holdout]
        df_no_menu_holdout = df_no_menu.iloc[:holdout]

        # the rest is used for ML evaluation
        df_menu = df_menu.iloc[holdout:]
        df_no_menu = df_no_menu.iloc[holdout:]

        # Appending the dfs back together
        cleaned_df = pd.concat([df_menu, df_no_menu])
        df_holdout = pd.concat([df_menu_holdout, df_no_menu_holdout])

        # Turning the labels into numbers
        labelEncoder = LabelEncoder()
        cleaned_df['class_num'] = labelEncoder.fit_transform(cleaned_df['class'])

        # Feature Extraction

        # Creating the features (tf-idf weights) for the processed text
        # Create tf-idf weights for data and target

        X = cleaned_df['cleaned_text'].astype('str')     # features
        y = cleaned_df['class_num'].values               # target

        # Train test split with stratified sampling for evaluation
        X_train, X_test, y_train, y_test = train_test_split(X,
                                                            y,
                                                            test_size=test_size,
                                                            shuffle=shuffle,
                                                            stratify=y,
                                                            random_state=random_state)

        # https://stackoverflow.com/questions/48692500/fit-transform-on-training-data-and-transform-on-test-data/48692740
        #
        # Centering and scaling happens independently on each feature by computing the
        # relevant statistics on the samples in the training set. Mean and standard deviation
        # are then stored to be used on later data using the transform method. - sklearn.StandardScaler
        #

        # Bag of Words
        if configs.get("use_BoW"):
            vectorizer = CountVectorizer(max_features=max_features,
                                         binary=True)

            X_train = vectorizer.fit_transform(X_train).toarray()
            X_test = vectorizer.transform(X_test).toarray()

        # Tf-Idf
        if configs.get("use_tfidf"):
            tfidf_vectorizer = TfidfVectorizer(ngram_range=ngram_range,
                                               min_df=min_df,
                                               max_df=max_df)

            X_train = tfidf_vectorizer.fit_transform(X_train).toarray()
            X_test = tfidf_vectorizer.transform(X_test).toarray()

        # Dimensionality reduction
        if configs.get("use_dimension_reduction"):
            lsa = TruncatedSVD(n_components=n_components,
                               n_iter=n_iter,
                               random_state=random_state)

            X_train = lsa.fit_transform(X_train)
            X_test = lsa.transform(X_test)
            scaler = MinMaxScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)

        # Preliminary model evaluation using default parameters

        # Creating a dict of the models
        # set all to random_state to 3 if parameter exists
        # all other parameters are set to default
        model_dict = {'Linear SVC': LinearSVC(),
                      'Ridge Classifier': RidgeClassifier(random_state=random_state),
                      'Perceptron': Perceptron(random_state=random_state),
                      'Passive Aggressive Classifier': PassiveAggressiveClassifier(random_state=random_state),
                      'Stochastic Gradient Descent': SGDClassifier(random_state=random_state),
                      'Random Forest': RandomForestClassifier(random_state=random_state),
                      'Decsision Tree': DecisionTreeClassifier(random_state=random_state),
                      'AdaBoost': AdaBoostClassifier(random_state=random_state),
                      'Gaussian Naive Bayes': GaussianNB(),
                      'Bernoulli Bayes': BernoulliNB(),
                      'Complement Bayes': ComplementNB(),
                      'Multinomial Bayes': MultinomialNB(),
                      'K Nearest Neighbor': KNeighborsClassifier(),
                      'Nearest Centroid': NearestCentroid()
                      }

        all_model_scores = self.model_score_df(model_dict, X_train, y_train, X_test, y_test)
        models_report = ""
        models_report += "All model performances with default parameters:\n"
        models_report += str(all_model_scores)
        models_report += "\n"
        models_report += "\n"
        models_report += str("Best 3 models with parameters for hyperparameter tuning:\n")
        models_report += str(self.format_params(self.model_params(model_dict, all_model_scores)))
        #print(models_report)

        # bar plot of all classifiers
        model_name = all_model_scores['model_name']
        precision = all_model_scores['precision_score']
        recall = all_model_scores['recall_score']
        f1 = all_model_scores['f1_score']
        indices = np.arange(len(all_model_scores))

        plt.figure(figsize=(12, 8))
        plt.title("Classifier-Comparison")
        p1 = plt.barh(indices, precision, .2, label="precision", color='#41f4a0')
        p2 = plt.barh(indices + .3, recall, .2, label="recall", color='#f4bc42')
        p3 = plt.barh(indices + .6, f1, .2, label="f1 score", color='#4286f4')
        plt.yticks(())
        plt.legend((p3[0], p2[0], p1[0]), ('f1 score', 'recall', 'precision'), loc='best')
        plt.subplots_adjust(left=.25)
        plt.subplots_adjust(top=.95)
        plt.subplots_adjust(bottom=.05)

        for i, c in zip(indices, model_name):
            plt.text(-.3, i, c)

        fig = plt.gcf()
        plt.show()
        plt.close()

        # Hyperparameter tuning



        # # Confusion Matrix
        #
        # # Fit the training data
        # best_model.fit(X_train, y_train)
        #
        # # Predict the testing data
        # y_pred = sgd_best_model.predict(X_test)
        #
        # # Get the confusion matrix and put it into a df
        # cm = confusion_matrix(y_test, y_pred)
        #
        # cm_df = pd.DataFrame(cm,
        #                      index=['menu', 'no_menu'],
        #                      columns=['menu', 'no_menu'])
        #
        # # Plot the heatmap
        # plt.figure(figsize=(12, 8))
        #
        # sns.heatmap(cm_df,
        #             center=0,
        #             cmap=sns.diverging_palette(220, 15, as_cmap=True),
        #             annot=True,
        #             fmt='g')
        #
        # plt.title('SGD (loss = log) \nF1 Score (avg = macro) : {0:.2f}'.format(f1_score(y_test, y_pred, average='macro')),
        #           fontsize=13)
        # plt.ylabel('True label', fontsize=13)
        # plt.xlabel('Predicted label', fontsize=13)
        # plt.show()

        # write report to file
        filename = "../data/models_report/configID_%s_%s.txt" % (self.configId, prefix)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        f = open(filename, "w")
        f.write(models_report)
        f.close()
        fig.savefig("../data/models_report/models-comparison_%s_%s.png" % (self.configId, prefix))

        # Write .csv-File
        with self.output().open("w") as out:
            cleaned_df.to_csv(out, encoding="utf-8")

    # Function to get the scores for each model in a df
    def model_score_df(self, model_dict, X_train, y_train, X_test, y_test):
        model_name, p_score_list, r_score_list, f1_score_list = [], [], [], []
        for k, v in model_dict.items():
            model_name.append(k)
            v.fit(X_train, y_train)
            y_pred = v.predict(X_test)
            p_score_list.append(precision_score(y_test, y_pred, average='macro'))
            r_score_list.append(recall_score(y_test, y_pred, average='macro'))
            f1_score_list.append(f1_score(y_test, y_pred, average='macro'))
            model_comparison_df = pd.DataFrame([model_name, p_score_list, r_score_list, f1_score_list]).T
            model_comparison_df.columns = ['model_name', 'precision_score', 'recall_score', 'f1_score']
            model_comparison_df = model_comparison_df.sort_values(by='f1_score', ascending=False)
        return model_comparison_df

    # Function get parameters of 3 best models
    def model_params(self, model_dict, model_comparison):
        model_name, parameters = [], []
        for i in range(0, 3):
            for k, v in model_dict.items():
                if model_comparison.iloc[i]['model_name'] == k:
                    model_name.append(k)
                    parameters.append(v.get_params())
        model_params = pd.DataFrame([model_name, parameters]).T
        model_params.columns = ['model_name', 'parameters']
        return model_params

    def format_params(self, model_params):
        report = ""
        for name in model_params['model_name']:
            report += str(name) + ":\n"
            for param in model_params['parameters']:
                report += "\t" + str(param) + "\n"
        return report
