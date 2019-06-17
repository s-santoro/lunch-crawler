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
        return LocalTarget("../output/%s_configID_%s_Classifier_out.csv" % (prefix, self.configId), format=UTF8)

    # Method to define the required Task (Preprocessor)
    def requires(self):
        return Preprocessor(self.configId)


    # Classify the imported Data
    def run(self):
        # use configID from commandline
        configs = Configurations().configs[self.configId]

        df = pd.read_csv(self.input().path)
        output_df = pd.DataFrame(columns=('specified', 'predicted', 'url'))
        output_df['specified'] = df['class'].values

        # Bag of Words Method
        if configs.get("classifyBagOfWords"):
            output_df = self.runBoWRules(df)
        # Whitelisting and Price-Tagger Method
        if configs.get("classifyCombinedRules"):
            for index, document in df.iterrows():
                value = self.runCombinedRules(document)
                output_df['predicted'].iloc[index] = value
                output_df['url'].iloc[index] = df['url'].iloc[index]

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
            dataParameter = "cleaned_text"
        else:
            dataParameter = "title"
        from sklearn.model_selection import train_test_split
        trainData, testData, trainLabels, testLabels = train_test_split(data[dataParameter].values, data['class'].values,
                                                                        test_size=Configurations().configs[self.configId].get("testSizeSplit"),
                                                                        random_state=0)
        output_df = pd.DataFrame(columns=('specified', 'predicted', 'url'))
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
            output_df['url'].iloc[index2]=data['url'].iloc[index2]
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
        text = document.cleaned_text
        posValueCounter = 100
        negValueCounter = 100
        # Whitelisting
        whitelist = pd.read_csv('../food_white_list_no_umlaute.txt', header=None)
        whitelist.columns = ['word']
        whitelistWords = Preprocessor().stemText(" ".join(whitelist.word))
        whitelistSet = set(whitelistWords)
        whitelistDict = dict.fromkeys(whitelistSet, 0)
        for word in text.split("'"):
            if word in whitelistSet:
                whitelistDict[word] += 1
        for key, value in whitelistDict.items():
            posValueCounter+=value

        # Blacklisting
        blacklist = pd.read_csv('../blacklist.txt', header=None)
        blacklist.columns = ['word']
        blacklistWords = Preprocessor().stemText(" ".join(blacklist.word))
        blacklistSet = set(blacklistWords)
        blacklistDict = dict.fromkeys(blacklistSet, 0)
        for word in text.split("'"):
            if word in blacklistSet:
                blacklistDict[word] += 1
        for key, value in blacklistDict.items():
            negValueCounter+=value
        #posValueCounter = posValueCounter/Configurations().configs[self.configId].get("treshold")
        #if posValueCounter > negValueCounter:
        ratio = posValueCounter/negValueCounter
        if ratio > Configurations().configs[self.configId].get("treshold"):
            return 1
        else:
            return 0