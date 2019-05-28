#!/usr/bin/env python
# coding: utf-8

# Imports
from luigi.parameter import IntParameter
from luigi import LocalTarget, Task
from luigi.format import UTF8
import datetime
import pandas as pd
import re
import os
from configs.Configurations import Configurations

'''bigrams'''
from gensim.models import Phrases
from collections import Counter
from Preprocessor import Preprocessor

'''Plotting'''
import matplotlib.pyplot as plt

class DataVisualizer(Task):
    # Date for Output-File prefix
    from datetime import date
    date = datetime.datetime.now()
    configId = IntParameter(default=0)

    # Method to declare the Output-File
    def output(self):
        prefix = self.date.strftime("%Y-%m-%dT%H%M%S")
        return LocalTarget("../data/%s_configID_%s_DataVisualizer.csv" % (prefix, self.configId), format=UTF8)

    # Method to define the required Task (Importer)
    def requires(self):
        return Preprocessor(self.configId)

    # Prepare preprocessed data for data evaluation
    def run(self):
        # use configID from commandline
        configs = Configurations().configs[self.configId]
        # default values if not set otherwise in configs
        n_most_freq_words = 20
        n_most_freq_words_per_class = 15
        n_most_freq_bigrams_per_class = 15

        # set values according to configs
        if ("n_most_freq_words" in configs):
            n_most_freq_words = configs.get("n_most_freq_words")
        if ("n_most_freq_words_per_class" in configs):
            n_most_freq_words_per_class = configs.get("n_most_freq_words_per_class")
        if ("n_most_freq_bigrams_per_class" in configs):
            n_most_freq_bigrams_per_class = configs.get("n_most_freq_bigrams_per_class")

        # dictionary holding all data_reports
        eval_dict = {}

        input_df = pd.read_csv(self.input().path)
        cleaned_df = pd.DataFrame(columns=('text', 'cleaned_text', 'url', 'title', 'class'))

        # convert document['cleaned_text'] from string to list of words
        for index, document in input_df.iterrows():
            text = document['cleaned_text']
            text = re.sub(r"[',\[\]]", "", text)
            wordlist = text.split(" ")
            row = [document.text, wordlist, document.url, document.title, document['class']]
            cleaned_df.loc[index] = row

        # Top n most frequent words for all the articles
        cl_text_list = cleaned_df['cleaned_text']
        wf = self.word_freq(cl_text_list, n_most_freq_words)
        eval_dict['n_frequent_words'] = wf.head(n_most_freq_words)

        # Avg word count by category
        cleaned_df['word_count'] = cleaned_df['cleaned_text'].apply(self.word_count)
        avg_wc = cleaned_df.groupby('class').mean().reset_index()
        eval_dict['avg_word_count_per_class'] = avg_wc[['class', 'word_count']]

        # Preparing the dataframes
        # Splitting the df into the different classes
        df_menu = cleaned_df.loc[cleaned_df['class'] == 1]
        df_no_menu = cleaned_df.loc[cleaned_df['class'] == 0]

        # Top n words by category. Taking bigrams into account
        text_menu = df_menu['cleaned_text']
        text_no_menu = df_no_menu['cleaned_text']
        menu = self.word_freq_bigrams(text_menu, top_n=n_most_freq_words_per_class)
        no_menu = self.word_freq_bigrams(text_no_menu, top_n=n_most_freq_words_per_class)
        df_wf = pd.concat([menu, no_menu], axis=1)
        cols = ['menu', 'count', 'no menu', 'count']
        df_wf.columns = cols
        eval_dict['n_top_words_per_class'] = df_wf

        # Top n bigrams by category
        menu_bigrams = self.bigram_freq(text_menu, top_n=n_most_freq_bigrams_per_class)
        no_menu_bigrams = self.bigram_freq(text_no_menu, top_n=n_most_freq_bigrams_per_class)

        df_bigram_wf = pd.concat([menu_bigrams, no_menu_bigrams], axis=1)
        df_bigram_wf.columns = cols
        eval_dict['n_top_bigrams_per_class'] = df_bigram_wf

        #
        # Plot the distribution of word count by article
        fig, ax = plt.subplots(1, 2, figsize=(12, 10))
        fig.suptitle('Distribution of Word Count by Category', fontsize=15)

        bins = 200
        ax[0].hist(df_menu['word_count'], bins=bins, color='#41924F')
        ax[0].set_title('Menu Category', fontsize=13)
        ax[0].set_xlim(0, 150)

        ax[1].hist(df_no_menu['word_count'], bins=bins, color='#FFC300')
        ax[1].set_title('No Menu Category', fontsize=13)
        ax[1].set_xlim(0, 150)

        # create data report
        data_report = "Data report\n\n"
        data_report += "configID: %s\n" % self.configId
        #
        data_report += "\n"
        data_report += "Average word count per class\n"
        data_report += str(eval_dict['avg_word_count_per_class'].head())
        data_report += "\n"
        #
        data_report += "\n"
        data_report += "Top %s frequent words\n" % n_most_freq_words
        data_report += str(eval_dict['n_frequent_words'].head(n_most_freq_words))
        data_report += "\n"
        #
        data_report += "\n"
        data_report += "Top %s words by category (Taking bigrams into account)\n" % n_most_freq_words_per_class
        data_report += str(eval_dict['n_top_words_per_class'].head(n_most_freq_bigrams_per_class))
        data_report += "\n"
        #
        data_report += "\n"
        data_report += "Top %s bigrams by category\n" % n_most_freq_words_per_class
        data_report += str(eval_dict['n_top_bigrams_per_class'].head(n_most_freq_bigrams_per_class))
        data_report += "\n"

        # write report to file
        prefix = self.date.strftime("%Y-%m-%dT%H%M%S")
        filename = "../data/data_report/configID_%s_%s.txt" % (self.configId, prefix)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        f = open(filename, "w")
        f.write(data_report)
        f.close()
        plt.savefig("../data/data_report/word_dist_by_class_%s.png" % prefix)
        plt.close(fig)

        # Write .csv-File
        with self.output().open("w") as out:
            input_df.to_csv(out, encoding="utf-8")

    def word_count(self, text):
        return len(str(text).split(' '))

    def word_freq(self, clean_text_list, top_n):
        """
        Word Frequency
        """
        flat = [item for sublist in clean_text_list for item in sublist]
        with_counts = Counter(flat)
        top = with_counts.most_common(top_n)
        word = [each[0] for each in top]
        num = [each[1] for each in top]
        return pd.DataFrame([word, num]).T

    def bigram_freq(self, clean_text_list, top_n):
        bigram_model = Phrases(clean_text_list, min_count=2, threshold=1)
        w_bigrams = bigram_model[clean_text_list]
        flat_w_bigrams = [item for sublist in w_bigrams for item in sublist]
        bigrams = []
        for each in flat_w_bigrams:
            if '_' in each:
                bigrams.append(each)
        counts = Counter(bigrams)
        top = counts.most_common(top_n)
        word = [each[0] for each in top]
        num = [each[1] for each in top]
        return pd.DataFrame([word, num]).T

    def word_freq_bigrams(self, clean_text_list, top_n):
        """
        Word Frequency With Bigrams
        """
        bigram_model = Phrases(clean_text_list, min_count=2, threshold=1)
        w_bigrams = bigram_model[clean_text_list]
        flat_w_bigrams = [item for sublist in w_bigrams for item in sublist]
        with_counts = Counter(flat_w_bigrams)
        top = with_counts.most_common(top_n)
        word = [each[0] for each in top]
        num = [each[1] for each in top]
        return pd.DataFrame([word, num]).T


