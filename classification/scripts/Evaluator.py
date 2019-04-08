#!/usr/bin/env python
# coding: utf-8

# Imports
from luigi.contrib.spark import PySparkTask
from luigi.parameter import IntParameter
from luigi import LocalTarget, Task, WrapperTask
from luigi.format import UTF8
import datetime
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from RulebasedClassifier import RulebasedClassifier
from configs.Configurations import Configurations


class Evaluator(Task):

    # Date for Output-File prefix
    from datetime import date
    date = datetime.datetime.now()
    configId = IntParameter(default=0)

    # Method to declare the Output-File
    def output(self):
        prefix = self.date.strftime("%Y-%m-%dT%H%M%S")
        return LocalTarget("../data/%s_configID_%s_Evaluator_out.csv" % (prefix, self.configId), format=UTF8)
    
    # Method to define the required Task (Preprocessor)
    def requires(self):
        return RulebasedClassifier(self.configId)


    # Classify the imported Data
    def run(self):
        # use configID from commandline
        configs = Configurations().configs[self.configId]

        df = pd.read_csv(self.input().path)
        print('TP: %s\tFP: %s\nFN: %s\tTN: %s'% self.calculateScore(df))
        print(classification_report(df['specified'].values, df['predicted'].values))

        configOverview = "------------------------------------------------------\n"
        configOverview += "configID:%s\n" % self.configId
        for key in configs:
            configOverview += "\t%s:\t\t\t\t%s\n" % (key, configs.get(key))
        configOverview += "------------------------------------------------------\n"
        print(configOverview)
        
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



