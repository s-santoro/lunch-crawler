#!/usr/bin/env python
# coding: utf-8

# Imports
from luigi.contrib.spark import PySparkTask
from luigi.parameter import IntParameter
from luigi.format import UTF8
from luigi import LocalTarget, Task, WrapperTask
import datetime
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from nltk.stem.cistem import Cistem
from Preprocessor import Preprocessor
from configs.Configurations import Configurations


class RulebasedClassifier(Task):

    # Date for Output-File prefix
    from datetime import date
    date = datetime.datetime.now()
    configId = IntParameter(default=0)

    # sum of rules must exceed the threshold for a positive classification
    threshold = 1
    keyAmount = 1
    keyValTreshold = 1
    printPosCounter = 0
    printNegCounter = 0

    # Method to declare the Output-File
    def output(self):
        prefix = self.date.strftime("%Y-%m-%dT%H%M%S")
        return LocalTarget("../data/%s_configID_%s_Classifier_out.csv" % (prefix, self.configId), format=UTF8)

    # Method to define the required Task (Preprocessor)
    def requires(self):
        return Preprocessor(self.configId)


    # Classify the imported Data
    def run(self):
        # use configID from commandline
        configs = Configurations().configs[self.configId]

        df = pd.read_csv(self.input().path)
        output_df = pd.DataFrame(columns=('specified', 'predicted'))
        output_df['specified'] = df['class'].values

        for index, document in df.iterrows():
            value = self.runRules(document)
            output_df['predicted'].iloc[index] = value

        # show how many documents had white list entries
        # maybe for later eval-output interesting
        # print("pos: %s"%self.printPosCounter)
        # print("neg: %s"%self.printNegCounter)
        # print(len(output_df['predicted']))

        # Write .csv-File
        with self.output().open("w") as out:
            output_df.to_csv(out, encoding="utf-8")

    def runRules(self, document):
        title = document.title
        text = document.text
        appliedRules = []
        # check if title is a string
        if type(title) is str:
            if Preprocessor().stemWord('menu') in title:
                pass
                #appliedRules.append(1)

            if Preprocessor().stemWord('tagesmenu') in title:
                pass
                #appliedRules.append(1)

        # check if text is a string
        if type(text) is str:
            if Preprocessor().stemWord('priceentity') in text:
                appliedRules.append(1)

            appliedRules.append(self.whitelisting(text, document))

        # check if threshold exceeded
        if appliedRules.count(1) > self.threshold:
            return 1
        else:
            return 0
        # threshold = 1 and rules = priceDetector, whitelisting => score of 1


    # whitelist with common ingredient and dish names
    # return histogram which shows how many whitelist entries where found in given text
    def whitelisting(self, text, document):
        # use own white list (contains ingredients and dishes)
        food = pd.read_csv('../food_white_list_no_umlaute.txt', header=None)
        food.columns = ['word']
        # convert list to set for word comparison and stem words
        # length is length of food list without first entries=indexes
        whitelistWords = Preprocessor().stemText(" ".join(food.word))
        foodSet = set(whitelistWords)
        foodDict = dict.fromkeys(foodSet, 0)
        # split text which is a string in list presentation with seperator=' in order to get each element
        # ['elem1', 'elem2', 'elem3']
        for word in text.split("'"):
            # check if word is in foodSet
            if word in foodSet:
                # increment value of key=word
                foodDict[word] += 1

        return self.evalHistValues(foodDict, document["class"])

    def evalHistValues(self, dictionary, classValue):

        temp = ""
        hasValues = False
        hasPosValues = False
        hasNegValues = False
        for key in dictionary:
            if dictionary[key] >= self.keyValTreshold:
                hasValues = True
                temp += ("key: %s\t\tvalue: %s\n"%(key, dictionary[key]))

        if hasValues and classValue == 0 and len(temp.split("\n")) >= self.keyAmount:
            hasNegValues = True
            self.printNegCounter += 1
        if hasValues and classValue == 1 and len(temp.split("\n")) >= self.keyAmount:
            hasPosValues = True
            self.printPosCounter += 1
        #print(temp)
        #print("pos: %s\tneg: %s"%(hasPosValues, hasNegValues))
        if hasPosValues:
            return 1
        else:
            return 0

