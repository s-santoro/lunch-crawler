#!/usr/bin/env python
# coding: utf-8

# Imports
from luigi.contrib.spark import PySparkTask
from luigi.parameter import IntParameter, DateSecondParameter
from luigi import LocalTarget, Task, WrapperTask
from luigi.format import UTF8
import datetime
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from RulebasedClassifier import RulebasedClassifier


class Evaluator(Task):

    # Date for Output-File prefix
    from datetime import date
    date = DateSecondParameter(default=datetime.datetime.now())
    
    # Method to declare the Output-File
    def output(self):
        prefix = self.date.strftime("%Y-%m-%dT%H%M%S")
        return LocalTarget("../data/%s_Evaluator_out.csv" % prefix, format=UTF8)
    
    # Method to define the required Task (Preprocessor)
    def requires(self):
        return RulebasedClassifier()


    # Classify the imported Data
    def run(self):
        df = pd.read_csv(self.input().path)
        print('TP: %s\tFP: %s\nFN: %s\tTN: %s'% self.calculateScore(df))
        print(classification_report(df['specified'].values, df['predicted'].values))
        
        # Write .csv-File
        with self.output().open("w") as out:
            df.to_csv(out, encoding="utf-8")
            
    def calculateScore(self, df):
        tp = 0
        tn = 0
        fp = 0
        fn = 0
        for index, document in df.iterrows():
            if document.specified == 1 and document.predicted == 1:
                tp+=1
            elif document.specified == 0 and document.predicted == 1:
                fp+=1
            elif document.specified == 1 and document.predicted == 0:
                fn+=1
            else:
                tn+=1
        
        return tp, fp, fn, tn



