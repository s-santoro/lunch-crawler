#!/usr/bin/env python
# coding: utf-8

# Imports
from luigi.contrib.spark import PySparkTask
from luigi.parameter import IntParameter
from luigi import LocalTarget, Task, WrapperTask
from luigi.format import UTF8
import datetime
import os
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

        confMatrix = "------------------------------------------------------\n"
        confMatrix += "Pipeline executed on: %s\n" % self.date
        confMatrix += "Confusion Matrix\n"
        confMatrix += '\tTP: %s\tFP: %s\n\tFN: %s\tTN: %s\n'% self.calculateScore(df)
        confMatrix += "\n"

        report = "Classification Report\n"
        report += classification_report(df['specified'].values, df['predicted'].values)
        report += "\n"

        configOverview = "------------------------------------------------------\n"
        configOverview += "Pipeline Configuration\n"
        configOverview += "configID: %s\n" % self.configId
        for key in configs:
            configOverview += "\t%s:" % key
            x = len(str(key))
            while x < 35:
                x += 1
                configOverview += " "
            configOverview += "%s\n" % configs.get(key)
        configOverview += "------------------------------------------------------\n"

        evalReport = confMatrix+report+configOverview

        values = self.calculateScore(df)
        tp = values[0]
        fp = values[1]
        fn = values[2]
        tn = values[3]
        if (tp+fp) != 0:
            precision = round(tp/(tp+fp), 2)
        else:
            precision = 0
        if (tp+fn) != 0:
            recall = round(tp/(tp+fn), 2)
        else:
            recall = 0
        if (2*tp+fp+fn) != 0:
            f1=round((2*tp)/(2*tp+fp+fn), 2)
        else:
            f1=0

        # write report to file
        prefix = self.date.strftime("%Y-%m-%dT%H%M%S")
        filename = "../data/evaluation_report/F1_%s_Pre_%s_Rec_%s_configID_%s_%s.txt" % (f1, precision, recall, self.configId, prefix)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        f = open(filename, "w")
        f.write(evalReport)
        f.close()

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



