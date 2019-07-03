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
import pickle
from configs.Configurations import Configurations
from Preprocessor import Preprocessor

class Classifier(Task):
    # Date for Output-File prefix
    from datetime import date
    date = datetime.datetime.now()
    configId = IntParameter(default=0)

    # Method to declare the Output-File
    def output(self):
        prefix = self.date.strftime("%Y-%m-%dT%H%M%S")
        return LocalTarget("./logs/%s_Classifier_out.csv" % (prefix), format=UTF8)

    # Method to define the required Task (Importer)
    def requires(self):
        return Preprocessor(self.configId)

    # run classification
    def run(self):
        # use configID from commandline
        configs = Configurations().configs[self.configId]

        prefix = self.date.strftime("%Y-%m-%dT%H%M%S")
        input_df = pd.read_csv(self.input().path)
        cleaned_df = pd.DataFrame(columns=('text', 'cleaned_text', 'url', 'title'))
        output_df = pd.DataFrame(columns=('prediction', 'url', 'text', 'cleaned_text', 'filename'))

        # convert document['cleaned_text'] from string to list of words
        for index, document in input_df.iterrows():
            text = document['cleaned_text']
            text = re.sub(r"[',\[\]]", "", text)
            wordlist = text.split(" ")
            row = [document.text, wordlist, document.url, document.title]
            cleaned_df.loc[index] = row

        # Feature Extraction
        X = cleaned_df['cleaned_text'].astype('str')

        # load the model from disk
        #vectorizer = pickle.load(open('./pickled_objects/bow_randomForest.sav', 'rb'))
        vectorizer = pickle.load(open('./pickled_objects/bow_perceptron.sav', 'rb'))

        X = vectorizer.transform(X).toarray()

        # load the model from disk
        #lsa = pickle.load(open('./pickled_objects/lsa_randomForest.sav', 'rb'))
        lsa = pickle.load(open('./pickled_objects/lsa_perceptron.sav', 'rb'))

        X = lsa.transform(X)
        
        # load the model from disk
        #scaler = pickle.load(open('./pickled_objects/scaler_randomForest.sav', 'rb'))
        scaler = pickle.load(open('./pickled_objects/scaler_perceptron.sav', 'rb'))

        X = scaler.transform(X)

        # load the model from disk
        #clf = pickle.load(open('./pickled_objects/clf_randomForest.sav', 'rb'))
        clf = pickle.load(open('./pickled_objects/clf_perceptron.sav', 'rb'))    
        prediction = clf.predict(X)

        output_df['prediction'] = prediction
        output_df['url'] = input_df['url']
        output_df['text'] = input_df['text']
        output_df['cleaned_text'] = input_df['cleaned_text']
        output_df['filename'] = input_df['filename']

        pos = "./output/menu/"
        neg = "./output/no_menu/"
        os.makedirs(pos, exist_ok=True)
        os.makedirs(neg, exist_ok=True)

        for index, row in output_df.iterrows():
            file = row.to_json()
            if(row['prediction'] == 1):
                f = open(pos + row['filename'], "w")
                f.write(file)
                f.close()
            else:
                f = open(neg + row['filename'], "w")
                f.write(file)
                f.close()

        # Write .csv-File
        with self.output().open("w") as out:
            output_df.to_csv(out, encoding="utf-8")

