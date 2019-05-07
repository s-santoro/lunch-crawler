#!/usr/bin/env python
# coding: utf-8

# Imports
from luigi.contrib.spark import PySparkTask
from luigi.parameter import IntParameter
from luigi import LocalTarget, Task, WrapperTask
from luigi.format import UTF8
import datetime
import pandas as pd
import re
from nltk.stem.cistem import Cistem
from Importer import Importer
from configs.Configurations import Configurations


class Preprocessor(Task):

    # Date for Output-File prefix
    from datetime import date
    date = datetime.datetime.now()
    configId = IntParameter(default=0)

    # Method to declare the Output-File
    def output(self):
        prefix = self.date.strftime("%Y-%m-%dT%H%M%S")
        return LocalTarget("../data/%s_configID_%s_Preprocessor_out.csv" % (prefix, self.configId), format=UTF8)
    
    # Method to define the required Task (Importer)
    def requires(self):
        return Importer(self.configId)


    # Preprocess the imported Data
    def run(self):
        # use configID from commandline
        configs = Configurations().configs[self.configId]

        df = pd.read_csv(self.input().path)
        output_df = pd.DataFrame(columns=('text', 'url', 'title', 'class'))

        for index, document in df.iterrows():
            # Text Preprocessing
            text = str(document.text)
            if configs.get("textToLowerCase"):
                text = self.toLowerCase(str(document.text))
            if configs.get("textReplaceUmlaut"):
                text = self.replaceUmlaut(text)
            if configs.get("textPriceTagger"):
                text = self.priceTagger(text)
            if configs.get("textRemoveSpecialCharacters"):
                text = self.removeSpecialCharacters(text)
            if configs.get("textRemoveSingleCharacters"):
                text = self.removeSingleCharacters(text)
            if configs.get("textRemoveMultiSpaces"):
                text = self.removeMultiSpaces(text)
            if configs.get("textStemText"):
                text = self.stemText(text)
            if configs.get("textRemoveStopWords"):
                text = self.removeStopWords(text)
            
            # Title Preprocessing
            title = str(document.title)
            if configs.get("titleToLowerCase"):
                title = self.toLowerCase(str(document.title))
            if configs.get("titleReplaceUmlaut"):
                title = self.replaceUmlaut(title)
            if configs.get("titlePriceTagger"):
                title = self.priceTagger(title)
            if configs.get("titleRemoveSpecialCharacters"):
                title = self.removeSpecialCharacters(title)
            if configs.get("titleRemoveSingleCharacters"):
                title = self.removeSingleCharacters(title)
            if configs.get("titleRemoveMultiSpaces"):
                title = self.removeMultiSpaces(title)
            if configs.get("titleStemText"):
                title = self.stemText(title)
            if configs.get("titleRemoveStopWords"):
                title = self.removeStopWords(title)

            # Write rows for Output-File
            row = [text, document.url, title, document.Class]
            output_df.loc[index] = row
        
        # Write .csv-File
        with self.output().open("w") as out:
            output_df.to_csv(out, encoding="utf-8")
            
    
    # External Methods for preprocessing
    def toLowerCase(self, text):
        return text.lower()
    
    def priceTagger(self, text):
        # match patterns with decimalpoint or comma, real rappen-values and chf,sfr,fr or .-:
        # whitespaces inside () are optional
        # characters inside [] are prohibited
        # x => number
        # a => letter
        #   [x or a or , or .]xxx.xx( )chf[x or a]
        text = re.sub(r'[^0-9a-z\.\,][0-9]{1,3}(\.|\,)[0-9](5|0) {0,1}(chf|sfr|fr|\.\-)[^0-9a-z]', ' priceentity ', text)
        # match following patterns with chf,sfr,fr or .-:
        # characters inside () are optional
        # characters inside [] are prohibited
        # x => number
        # a => letter
        #   [x or a or , or .]xxx( )chf[x or a]
        text = re.sub(r'[^0-9a-z\.\,][0-9]{1,3} {0,1}(chf|sfr|fr|\.\-)[^0-9a-z]', ' priceentity ', text)
        # match following patterns with decimalpoint or comma, real rappen-values and chf,sfr,fr or .-:
        # characters inside () are optional
        # characters inside [] are prohibited
        # x => number
        # a => letter
        #   [x or a or , or .]chf(.)( )xxx.xx[x or a]
        text = re.sub(r'[^0-9a-z\.\,](chf|sfr|fr)\.{0,1} {0,1}[0-9]{1,3}(\.|\,)[0-9](5|0)[^0-9a-z]', ' priceentity ', text)
        # match following patterns with decimalpoint or comma and real rappen-values:
        # characters inside () are optional
        # characters inside [] are prohibited
        # x => number
        # a => letter
        #   [x or a or , or .]xxx.xx[x or a]
        # to avoid detecting day times or dates the regex only detects
        # prices with values after decimalpoint over 59 (i.e 12.60 or 1.65)
        text = re.sub(r'[^0-9a-z\.\,][0-9]{1,3}(\.|\,)[6-9](0|5)[^0-9\.a-z]', ' priceentity ', text)
        return text
        
    def removeSpecialCharacters(self, text):
        return re.sub(r'[^éàèÉÀÈäöüÄÖÜa-zA-Z]+', ' ', str(text))
    
    def removeSingleCharacters(self, text):
        return re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
    
    def removeMultiSpaces(self, text):
        return re.sub(r'\s+', ' ', text, flags=re.I)
    
    def stemText(self, text):
        stemmer = Cistem()
        return [stemmer.stem(word) for word in text.split()]

    def stemWord(self, word):
        stemmer = Cistem()
        return stemmer.stem(word)
    
    def removeStopWords(self, words):
        # use own stopword list
        stop = pd.read_csv('../stopwords_no_umlaute.txt', header=None)
        stop.columns = ['word']
        # convert list to set for word comparison
        stopwordSet = set(stop.word)
        wordsFiltered = []
        wordsRemoved = []
        for w in words:
            if w not in stopwordSet:
                wordsFiltered.append(w)
            if w in stopwordSet:
                wordsRemoved.append(w)

        #print("Removed words: %s" % wordsRemoved)
        #print("Percentage of removed words: %s" % (len(wordsRemoved)/len(words)*100))
        return wordsFiltered
    
    def replaceUmlaut(self, text):
        text = re.sub(r'ä', 'a', text)
        text = re.sub(r'ö', 'o', text)
        text = re.sub(r'ü', 'u', text)
        return text
        


# Preis-Regex werden verwendet, um effektive Preise auf das Wort 'preis' zu mappen.
# Dies ist nützlich, indem bei der späteren Klassifizierung nach dem Wort 'preis' und nicht nach
# effektiven Frankenbeträgen gesucht werden kann.  
# 
# Die unteren Muster von Preisen wurden mit den Regex formuliert
# - _xxx.xx chf
# - _xxx.xxchf
# - _xxx chf
# - _xxxchf
# - _xxx.xx
# - Die Muster folgen folgender Konvention:
#     - Es kann entweder ein Dezimalpunkt oder ein Komma als Separator verwendet werden
#     - Die Preise gehen von 00.00 bis 999.95
#     - Es werden nur Preise erkannt, die einen realen Rappenbetrag präsentieren
#     - Es können chf, sfr, fr oder .- als Abkürzungen für Geldbeträge verwendet werden
#     - Preise ohne Abkürzungen sind auch möglich, sofern sie die anderen Konventionen berücksichtigen
#     - Der Bodenstrich soll ein Leerzeichen präsentieren

# ## Anpassungen
# - Anpassung von Regex "preis" auf "priceentity", da diese mit hoher Wahrscheinlichkeit nicht vorkommt
# 
#pre = Preprocessor()
#pre.run()