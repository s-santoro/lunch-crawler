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
        return LocalTarget("../output/%s_configID_%s_MLClassifiers.csv" % (prefix, self.configId), format=UTF8)

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
        binary = configs.get("binary")
        # tfidf
        ngram_range = configs.get("ngram_range")
        min_df = configs.get("min_df")
        max_df = configs.get("max_df")
        max_features_tfidf = configs.get("maxFeaturesTFIDF")
        # dimension reduction (truncated svd)
        n_components = configs.get("n_components")
        n_iter = configs.get("n_iter")

        input_df = pd.read_csv(self.input().path)
        cleaned_df = pd.DataFrame(columns=('text', 'cleaned_text', 'url', 'title', 'class'))

        # convert document['cleaned_text'] from string to list of words
        for index, document in input_df.iterrows():
            text = document['cleaned_text']
            #print("MLClassifier")
            #print(text)
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
        X_train, X_validation, y_train, y_validation = train_test_split(X,
                                                            y,
                                                            test_size=test_size,
                                                            shuffle=shuffle,
                                                            stratify=y,
                                                            random_state=random_state)

        # Bag of Words
        if configs.get("use_BoW"):
            vectorizer = CountVectorizer(max_features=max_features, binary=binary)

            X_train = vectorizer.fit_transform(X_train).toarray()
            X_validation = vectorizer.transform(X_validation).toarray()

        # Tf-Idf
        if configs.get("use_tfidf"):
            tfidf_vectorizer = TfidfVectorizer(ngram_range=ngram_range,
                                               min_df=min_df,
                                               max_df=max_df,
                                               max_features=max_features_tfidf)

            X_train = tfidf_vectorizer.fit_transform(X_train).toarray()
            X_validation = tfidf_vectorizer.transform(X_validation).toarray()

        # Dimensionality reduction
        if configs.get("use_dimension_reduction"):
            lsa = TruncatedSVD(n_components=n_components,
                               n_iter=n_iter,
                               random_state=random_state)

            X_train = lsa.fit_transform(X_train)
            X_validation = lsa.transform(X_validation)
            scaler = MinMaxScaler()
            X_train = scaler.fit_transform(X_train)
            X_validation = scaler.transform(X_validation)

        # calculate class weights
        # Bring unequal distribution of pos/neg samples into account
        negatives = np.count_nonzero(cleaned_df['class_num']==0)
        positives = np.count_nonzero(cleaned_df['class_num']==1)
        if positives > 0:
            ratio = negatives / positives
            class_weight = {0: 1., 1: ratio}
        else:
            class_weight = {0: 1., 1: 1.}
        # Preliminary model evaluation using default parameters

        # Creating a dict of the models
        # set all to random_state to 3 if parameter exists
        # all other parameters are set to default
        model_dict = {'Linear SVC': LinearSVC(class_weight=class_weight),
                      'Ridge Classifier': RidgeClassifier(random_state=random_state, class_weight=class_weight),
                      'Perceptron': Perceptron(random_state=random_state, n_jobs=-1, class_weight=class_weight),
                      'Passive Aggressive Classifier': PassiveAggressiveClassifier(random_state=random_state, n_jobs=-1, class_weight=class_weight),
                      'Stochastic Gradient Descent': SGDClassifier(random_state=random_state, n_jobs=-1, class_weight=class_weight),
                      'Random Forest': RandomForestClassifier(random_state=random_state, n_jobs=-1, class_weight=class_weight),
                      'Decsision Tree': DecisionTreeClassifier(random_state=random_state, class_weight=class_weight),
                      'AdaBoost': AdaBoostClassifier(random_state=random_state),
                      'Gaussian Naive Bayes': GaussianNB(),
                      'Bernoulli Bayes': BernoulliNB(),
                      'Complement Bayes': ComplementNB(),
                      'Multinomial Bayes': MultinomialNB(),
                      'K Nearest Neighbor': KNeighborsClassifier(),
                      'Nearest Centroid': NearestCentroid()
                      }

        all_model_scores = self.model_score_df(model_dict, X_train, y_train, X_validation, y_validation)
        models_report = ""
        models_report += "All model performances with default parameters:\n"
        models_report += str(all_model_scores)
        models_report += "\n"
        models_report += "\n"
        models_report += str("Best 3 models with parameters for hyperparameter tuning:\n")
        models_report += str(self.format_params(self.model_params(model_dict, all_model_scores)))
        models_report += "\n"
        models_report += "\n"
        models_report += str("Pipeline Configuration:\n")
        models_report += "configID: %s\n" % self.configId
        for key in configs:
            models_report += "\t%s:" % str(key)
            x = len(str(key))
            while x < 35:
                x += 1
                models_report += " "
            models_report += "%s\n" % str(configs.get(key))

        # bar plot of all classifiers
        model_name = all_model_scores['model_name']
        precision = all_model_scores['precision_score']
        recall = all_model_scores['recall_score']
        f1 = all_model_scores['f1_score']
        indices = np.arange(len(all_model_scores))

        plt.figure(figsize=(12, 8))
        plt.title("Classifier-Comparison with config: %s" % self.configId)
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
    def model_score_df(self, model_dict, X_train, y_train, X_validation, y_validation):
        model_name, p_score_list, r_score_list, f1_score_list = [], [], [], []
        for k, v in model_dict.items():
            model_name.append(k)
            v.fit(X_train, y_train)
            y_pred = v.predict(X_validation)
            p_score_list.append(precision_score(y_validation, y_pred))
            r_score_list.append(recall_score(y_validation, y_pred))
            f1_score_list.append(f1_score(y_validation, y_pred))
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
