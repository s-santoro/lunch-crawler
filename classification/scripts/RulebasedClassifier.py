#!/usr/bin/env python
# coding: utf-8

# Imports
from luigi.contrib.spark import PySparkTask
from luigi.parameter import IntParameter
from luigi.format import UTF8
from luigi import LocalTarget, Task, WrapperTask
import datetime
import re
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
        cleaned_df = pd.DataFrame(columns=('text', 'cleaned_text', 'url', 'title', 'class'))
        output_df = pd.DataFrame(columns=('specified', 'predicted', 'url'))
        output_df['specified'] = df['class'].values

        # Change Text String to List
        for index, document in df.iterrows():
            text = document['cleaned_text']
            text = re.sub(r"[',\[\]]", "", text)
            wordlist = text.split(" ")
            row = [document.text, wordlist, document.url, document.title, document['class']]
            cleaned_df.loc[index] = row

        # Menu in Title
        if configs.get("classifyMenuInTitle"):
            for index, document in cleaned_df.iterrows():
                value = self.runMenuInTitle(document)
                output_df['predicted'].iloc[index] = value
                output_df['url'].iloc[index] = df['url'].iloc[index]
        # Pricedetector
        if configs.get("classifyPricedetector"):
            for index, document in cleaned_df.iterrows():
                value = self.runPricedetector(document)
                output_df['predicted'].iloc[index] = value
                output_df['url'].iloc[index] = df['url'].iloc[index]
        # Menu and Price combined
        if configs.get("classifyPriceMenuCombined"):
            for index, document in cleaned_df.iterrows():
                value = self.runMenuPriceCombined(document)
                output_df['predicted'].iloc[index] = value
                output_df['url'].iloc[index] = df['url'].iloc[index]
        # Bag of Words Method
        if configs.get("classifyBagOfWords"):
            output_df = self.runBoWRules(df)
        # Blacklisting/Whitelisting Method
        if configs.get("classifyListing"):
            for index, document in df.iterrows():
                value = self.runListing(document)
                output_df['predicted'].iloc[index] = value
                output_df['url'].iloc[index] = df['url'].iloc[index]

        # Write .csv-File
        with self.output().open("w") as out:
            output_df.to_csv(out, encoding="utf-8")

    def runMenuInTitle(self, document):
        if Preprocessor().stemWord("menu") in document["title"]:
            return 1
        else:
            return 0
        

    def runPricedetector(self, document):
        value = 0
        limit = Configurations().configs[self.configId].get("priceLimit")
        for word in document["cleaned_text"]:  
            if Preprocessor().stemWord('twodigitprice') == word:       
                value+=1
        if value >= limit:
            return 1
        else:
            return 0
    
    def runMenuPriceCombined(self, document):
        if Preprocessor().stemWord("menu") in document["title"]:
            return 1
        else:
            return self.runPricedetector(document)

    def runBoWRules(self, data):
        output_df = pd.DataFrame(columns=('specified', 'predicted', 'url'))
        # Decision to use Text or Title
        if Configurations().configs[self.configId].get("useText"):
                dataParameter = "cleaned_text"
        else:
            dataParameter = "title"
        # Check if Lists should be created dynamically or static
        if(Configurations().configs[self.configId].get("dynamic")):
            
            from sklearn.model_selection import train_test_split
            # Split Data into Train Files (for generating BoW) and Test Files
            trainData, testData, trainLabels, testLabels = train_test_split(data[dataParameter].values, data['class'].values,
                                                                            test_size=Configurations().configs[self.configId].get("testSizeSplit"),
                                                                            random_state=0)
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
        else:
            # Use Static word lists generated out of test data of Gold Standard
            posWords = ['abholung', 'aglio', 'ai', 'aktivier', 'al', 'alkoholfrei', 'alkoholisch', 'alla', 'allerg', 'anana', 'antipasti', 'apero', 'arrabbiata', 'artikelnr', 'artikelnumm', 'artischock', 'au', 'aubergi', 'balsamico', 'basilikum', 'beilag', 'beleg', 'beschreibung', 'bewertung', 'blattsala', 'bleu', 'bolog', 'bra', 'bro', 'broccoli', 'bun', 'burg', 'butt', 'cak', 'calzo', 'capr', 'casa', 'champigno', 'chef', 'cherry', 'cherrytoma', 'chick', 'chili', 'chocola', 'cm', 'cocktail', 'cordo', 'crevett', 'curry', 'delivery', 'ei', 'eier', 'enthal', 'erdbeer', 'erstell', 'extra', 'fil', 'focaccia', 'formaggi', 'fri', 'fruch', 'full', 'funghi', 'gang', 'garnier', 'glac', 'glacé', 'gnocchi', 'gorgonzola', 'gramm', 'grand', 'grill', 'grillier', 'gru', 'gurk', 'hawaii', 'hinzufug', 'hit', 'honig', 'hot', 'imbiss', 'ingw', 'insalata', 'italia', 'italienisch', 'joghur', 'kalb', 'kalbfleisch', 'kaper', 'karott', 'kartoffel', 'kas', 'kass', 'kategorie', 'kinderpizza', 'klassik', 'knoblauch', 'knusprig', 'krau', 'krauterbutt', 'kurier', 'lach', 'lamm', 'lasag', 'lieferzei', 'mar', 'margherita', 'marinier', 'mascarpo', 'meeresfruch', 'meng', 'menukar', 'mini', 'misch', 'mouss', 'mozzarella', 'mus', 'mws', 'napoli', 'normal', 'nudel', 'oliv', 'olivenol', 'oregano', 'panier', 'panna', 'parma', 'parmaschink', 'parmesa', 'penn', 'peperoncini', 'peperoni', 'pesto', 'pilz', 'pizz', 'pizzakurier', 'pizzeria', 'pollo', 'pomm', 'porcini', 'portio', 'poul', 'pouletbru', 'pouletfleisch', 'prosciutto', 'quattro', 'rahmsauc', 'registrier', 'registrierung', 'riesencrevett', 'rind', 'rindfleisch', 'rindsfil', 'risotto', 'rohschink', 'rot', 'rucola', 'rustica', 'saiso', 'salami', 'sandwich', 'sardell', 'sauc', 'scharf', 'schink', 'schnitzel', 'schwei', 'skip', 'softdrink', 'sortier', 'spaghetti', 'spargel', 'speck', 'spezial', 'spina', 'spirituo', 'stagioni', 'steinpilz', 'stuck', 'supp', 'suss', 'tagliatell', 'te', 'teigwar', 'tell', 'thai', 'tho', 'thunfisch', 'tiramisu', 'toma', 'tomatensauc', 'tonno', 'tortellini', 'uberback', 'us', 'vanill', 'vega', 'vegetarisch', 'vegi', 'verd', 'versa', 'versandko', 'vorbehal', 'vorspei', 'with', 'wunschli', 'wunschpizza', 'wurz', 'zigarett', 'zitro', 'zuck', 'zusatzstoff', 'zuta', 'zwiebel', 'zzgl']
            negWords = ['abend', 'abmeld', 'ag', 'aktivita', 'allgemei', 'alt', 'ambie', 'anfahr', 'anmeldung', 'anrei', 'april', 'arbei', 'archiv', 'at', 'atmosphar', 'augu', 'bad', 'basel', 'bearbei', 'befi', 'bekann', 'ber', 'berei', 'bereich', 'beso', 'betrieb', 'bild', 'bildergalerie', 'bistro', 'bleib', 'buch', 'burtstag', 'business', 'club', 'cookie', 'dami', 'datenschutzerklarung', 'datum', 'desig', 'detail', 'deutsch', 'dezemb', 'dien', 'dienstleistung', 'doppelzimm', 'download', 'dritt', 'druck', 'durf', 'eign', 'einzelzimm', 'end', 'entdeck', 'erfahr', 'erfolg', 'erklar', 'erleb', 'erlebni', 'erreich', 'fahr', 'feiertag', 'fes', 'folg', 'foto', 'frag', 'fruhstuck', 'fuhr', 'fuhrung', 'gastgeb', 'gastronomie', 'geh', 'grund', 'grupp', 'herz', 'herzlich', 'heu', 'hinwei', 'hochzei', 'hor', 'hotel', 'http', 'idee', 'impressio', 'individuell', 'inter', 'it', 'jeweil', 'juli', 'juni', 'junior', 'kauf', 'klick', 'komm', 'kontaktformular', 'kontaktier', 'kostenlo', 'kulinarisch', 'kultur', 'kund', 'kur', 'lad', 'lagepla', 'land', 'lauf', 'leb', 'les', 'letz', 'lieb', 'lieg', 'lokal', 'loung', 'luzer', 'manag', 'map', 'marz', 'media', 'miet', 'mitarbei', 'mitglied', 'moch', 'moder', 'moglichkei', 'mona', 'musik', 'mutlich', 'nachrich', 'nah', 'neb', 'nehm', 'obe', 'of', 'offentlich', 'oktob', 'organisatio', 'ort', 'packag', 'party', 'pass', 'perfek', 'philosophie', 'pla', 'platz', 'press', 'priva', 'programm', 'raum', 'raumlichkei', 'rech', 'rechtlich', 'regio', 'reservierung', 'richtlinie', 'ruhetag', 'saal', 'sam', 'schenk', 'schutz', 'see', 'selb', 'sellschaf', 'seminar', 'seminarraum', 'send', 'setz', 'sitemap', 'somm', 'sond', 'spa', 'speziell', 'spiel', 'spor', 'sprach', 'st', 'stad', 'steh', 'ster', 'stund', 'sui', 'swiss', 'terrass', 'thi', 'threedigitpric', 'tischreservatio', 'tor', 'tour', 'ubernachtung', 'ubersich', 'unternehm', 'unterstutz', 'veranstaltung', 'verei', 'verfugung', 'verkauf', 'verw', 'video', 'voll', 'vornam', 'wand', 'web', 'webcam', 'webdesig', 'websei', 'wechsel', 'wel', 'welch', 'wett', 'win', 'wiss', 'woh', 'woll', 'you', 'zimm', 'zug', 'zusamm', 'zwisch']
            output_df['specified'] = data['class'].values
            # Classify      
            for index in range(len(data[dataParameter].values)):
                output_df['url'].iloc[index]=data['url'].iloc[index]
                score = Configurations().configs[self.configId].get("decisionLimit")
                for word in posWords:
                    if word in data[dataParameter].iloc[index]:
                        score = score + 1
                for word in negWords:
                    if word in data[dataParameter].iloc[index]:
                        score = score - 1
                if score > 0:
                    output_df['predicted'].iloc[index] = 1
                else:
                    output_df['predicted'].iloc[index] = 0
        return output_df

    def BagOfWords(self, data):
        vectorizer = CountVectorizer(max_features=Configurations().configs[self.configId].get("numberOfFeatures"), binary=True)
        BagofWords = vectorizer.fit_transform(data).toarray()
        features = vectorizer.get_feature_names()
        return features

    def runListing(self, document):
        text = document.cleaned_text
        posValueCounter = 1
        negValueCounter = 1
        # Whitelisting
        whitelist = pd.read_csv('../whitelist.txt', header=None)
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
        # Classify
        if negValueCounter > Configurations().configs[self.configId].get("negLimit"):
            return 0
        elif posValueCounter > Configurations().configs[self.configId].get("posLimit"):
            return 1
        else:
            return 0
