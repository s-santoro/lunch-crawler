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
from Preprocessor import Preprocessor

'''Features'''
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MaxAbsScaler

'''Classifiers'''
from sklearn.linear_model import SGDClassifier, Perceptron
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

'''Metrics/Evaluation'''
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from scipy import interp
from itertools import cycle

'''Plotting'''
import matplotlib.pyplot as plt
import seaborn as sns

class MLTuningSGD(Task):
    # Date for Output-File prefix
    from datetime import date
    date = datetime.datetime.now()
    configId = IntParameter(default=0)

    # Method to declare the Output-File
    def output(self):
        prefix = self.date.strftime("%Y-%m-%dT%H%M%S")
        return LocalTarget("../data/%s_configID_%s_MLTuningSGD.csv" % (prefix, self.configId), format=UTF8)

    # Method to define the required Task (Importer)
    def requires(self):
        return Preprocessor(self.configId)

    # Prepare prprocessed data for ML evaluation
    def run(self):
        # use configID from commandline
        configs = Configurations().configs[self.configId]
        eval_dict = {}

        # parameters for config
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

        # holdout is only used to have same scores as previously measured
        # without holdout scores are not identical to excel-table
        # Holding out 10 articles from each class for prediction at the end
        df_menu_holdout = df_menu.iloc[:20]
        df_no_menu_holdout = df_no_menu.iloc[:20]

        # the rest is used for ML evaluation
        df_menu = df_menu.iloc[20:]
        df_no_menu = df_no_menu.iloc[20:]

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

        # https://stackoverflow.com/questions/48692500/fit-transform-on-training-data-and-transform-on-test-data/48692740
        #
        # Centering and scaling happens independently on each feature by computing the
        # relevant statistics on the samples in the training set. Mean and standard deviation
        # are then stored to be used on later data using the transform method. - sklearn.StandardScaler
        #

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


        params = configs.get("params")

        gridsearch = GridSearchCV(
            SGDClassifier(random_state=random_state, n_jobs=-1, class_weight=class_weight),
            params,
            cv = 5, 
            n_jobs = -1,
            scoring="f1")
        gridsearch.fit(X_train, y_train)

        before_tuning = SGDClassifier(random_state=random_state, n_jobs=-1, class_weight=class_weight)
        before_tuning.fit(X_train, y_train)
        pred_not_tuned = before_tuning.predict(X_validation)

        best_model = gridsearch.best_estimator_
        pred_tuned = best_model.predict(X_validation)

        models_report = "Stochastic Gradient Descent"
        models_report += "\n"
        models_report += "----------------------------------------------------"
        models_report += "\n"
        models_report += "Default parameters:"
        models_report += "\n"
        models_report += str(before_tuning.get_params)
        models_report += "\n"
        models_report += "----------------------------------------------------"
        models_report += "\n"
        models_report += str("f1 score before hyperparameter-tuning: %s" % str(f1_score(y_validation, pred_not_tuned)))
        models_report += "\n"
        models_report += str("precision score before hyperparameter-tuning: %s" % str(precision_score(y_validation, pred_not_tuned)))
        models_report += "\n"
        models_report += str("recall score before hyperparameter-tuning: %s" % str(recall_score(y_validation, pred_not_tuned)))
        models_report += "\n"
        models_report += "----------------------------------------------------"
        models_report += "\n"

        models_report += "\n"
        models_report += "Best parameters set found:"
        models_report += "\n"
        models_report += str(gridsearch.best_params_)
        models_report += "\n"
        models_report += "----------------------------------------------------"
        models_report += "\n"
        models_report += str("f1 score after hyperparameter-tuning: %s" % str(f1_score(y_validation, pred_tuned)))
        models_report += "\n"
        models_report += str("precision score after hyperparameter-tuning: %s" % str(precision_score(y_validation, pred_tuned)))
        models_report += "\n"
        models_report += str("recall score after hyperparameter-tuning: %s" % str(recall_score(y_validation, pred_tuned)))
        models_report += "\n"
        models_report += "\n"
        models_report += "config:\n"
        for key in configs:
            models_report += "\t%s:" % str(key)
            x = len(str(key))
            while x < 35:
                x += 1
                models_report += " "
            models_report += "%s\n" % str(configs.get(key))

        
        
        # # Confusion Matrix
        
        # # Fit the training data
        # best_model.fit(X_train, y_train)
        
        # # Predict the testing data
        # y_pred = sgd_best_model.predict(X_validation)
        
        # # Get the confusion matrix and put it into a df
        # cm = confusion_matrix(y_validation, y_pred)
        
        # cm_df = pd.DataFrame(cm,
        #                      index=['menu', 'no_menu'],
        #                      columns=['menu', 'no_menu'])
        
        # # Plot the heatmap
        # plt.figure(figsize=(12, 8))
        
        # sns.heatmap(cm_df,
        #             center=0,
        #             cmap=sns.diverging_palette(220, 15, as_cmap=True),
        #             annot=True,
        #             fmt='g')
        
        # plt.title('SGD (loss = log) \nF1 Score (avg = macro) : {0:.2f}'.format(f1_score(y_validation, y_pred, average='macro')),
        #           fontsize=13)
        # plt.ylabel('True label', fontsize=13)
        # plt.xlabel('Predicted label', fontsize=13)
        # plt.show()

        # write report to file
        filename = "../data/parameter_tuning/sgd_%s.txt" % (prefix)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        f = open(filename, "w")
        f.write(models_report)
        f.close()
        #fig.savefig("../data/models_report/models-comparison_%s_%s.png" % (self.configId, prefix))

        # Write .csv-File
        with self.output().open("w") as out:
            cleaned_df.to_csv(out, encoding="utf-8")

