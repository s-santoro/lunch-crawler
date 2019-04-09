#!/usr/bin/env python
# coding: utf-8

# Imports
from luigi.contrib.spark import PySparkTask
from luigi.parameter import IntParameter
from luigi.format import UTF8
from luigi import LocalTarget, Task, WrapperTask
import datetime
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from Preprocessor import Preprocessor
from configs.Configurations import Configurations


class RulebasedClassifier(Task):

    # Date for Output-File prefix
    from datetime import date
    date = datetime.datetime.now()
    configId = IntParameter(default=0)

    # sum of rules must exceed the threshold for a positive classification
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

        # Bag of Words Method
        if configs.get("classifyBagOfWords"):
            output_df = self.runBoWRules(df)
        # Whitelisting and Price-Tagger Method
        if configs.get("classifyCombinedRules"):
            for index, document in df.iterrows():
                value = self.runCombinedRules(document)
                output_df['predicted'].iloc[index] = value

        # show how many documents had white list entries
        # maybe for later eval-output interesting
        # print("pos: %s"%self.printPosCounter)
        # print("neg: %s"%self.printNegCounter)
        # print(len(output_df['predicted']))

        # Write .csv-File
        with self.output().open("w") as out:
            output_df.to_csv(out, encoding="utf-8")

    def runBoWRules(self, data):
        # Split Data into Train Files (for generating BoW) and Test Files
        if Configurations().configs[self.configId].get("useText"):
            dataParameter = "text"
        else:
            dataParameter = "title"
        from sklearn.model_selection import train_test_split
        trainData, testData, trainLabels, testLabels = train_test_split(data[dataParameter].values, data['class'].values,
                                                                        test_size=Configurations().configs[self.configId].get("testSizeSplit"),
                                                                        random_state=0)
        output_df = pd.DataFrame(columns=('specified', 'predicted'))
        output_df['specified'] = testLabels
        # Sort Train Data
        posExamples = []
        negExamples = []
        for index in range(len(trainData)):
            if trainLabels[index] == 1:
                posExamples.append(trainData[index])
            else:
                negExamples.append(trainData[index])
        # Create Bag of Words
        posWords = self.BagOfWords(posExamples)
        negWords = self.BagOfWords(negExamples)
        # Filter for Words occuring in positive and negative Examples
        for i in range(len(posWords)):
            for j in range(len(negWords)):
                if posWords[i] == negWords[j]:
                    posWords[i] = 'remove'
                    negWords[j] = 'remove'
        while 'remove' in posWords: posWords.remove('remove')
        while 'remove' in negWords: negWords.remove('remove')
        # Classify
        for index2 in range(len(testData)):
            score = Configurations().configs[self.configId].get("decisionLimit")
            for word in posWords:
                if word in testData[index2]:
                    score = score + 1
            for word in negWords:
                if word in testData[index2]:
                    score = score - 1
            if score > 0:
                output_df['predicted'].iloc[index2] = 1
            else:
                output_df['predicted'].iloc[index2] = 0
        return output_df

    def BagOfWords(self, data):
        vectorizer = CountVectorizer(max_features=Configurations().configs[self.configId].get("numberOfFeatures"), binary=True)
        BagofWords = vectorizer.fit_transform(data).toarray()
        features = vectorizer.get_feature_names()
        return features

    def runCombinedRules(self, document):
        title = document.title
        text = document.text
        appliedRules = []
        # check if title is a string
        if type(title) is str and Configurations().configs[self.configId].get("menuInTitle") == True:
            if Preprocessor().stemWord('menu') in title:
                appliedRules.append(1)

            if Preprocessor().stemWord('tagesmenu') in title:
                appliedRules.append(1)

        # check if text is a string
        if type(text) is str:
            if Preprocessor().stemWord('priceentity') in text and Configurations().configs[self.configId].get("priceEntity") == True:
                appliedRules.append(1)
            if Configurations().configs[self.configId].get("whiteList"):
                appliedRules.append(self.whitelisting(text, document))

        # check if threshold exceeded
        if appliedRules.count(1) > 0:
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
        if hasPosValues:
            return 1
        else:
            return 0
