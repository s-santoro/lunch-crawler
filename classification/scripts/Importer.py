#!/usr/bin/env python
# coding: utf-8

# Imports
from luigi.contrib.spark import PySparkTask
from luigi.parameter import IntParameter, DateSecondParameter
from luigi import LocalTarget, Task, WrapperTask
from luigi.format import UTF8
from os import listdir
import pandas as pd
import datetime


class Importer(Task):
    
    # Date for Output-File prefix
    from datetime import date
    date = DateSecondParameter(default=datetime.datetime.now())

    # Method to declare the Output-File
    def output(self):
        prefix = self.date.strftime("%Y-%m-%dT%H%M%S")
        return LocalTarget("../data/%s_Importer_out.csv" % prefix, format=UTF8)
    
    # Method to generate the Output-File
    def run(self):

        # Load all negative Files into Array
        neg_filenames = [f for f in listdir("../files/neg")]
        neg_files = []
        for filename in neg_filenames:
            filepath = "../files/neg/"+filename
            neg_files.append(pd.read_json(filepath, typ="series", encoding='utf-8-sig'))
            
        # Load all positive Files into Array
        pos_filenames = [f for f in listdir("../files/pos")]
        pos_files = []
        for filename in pos_filenames:
            filepath = "../files/pos/"+filename
            pos_files.append(pd.read_json(filepath, typ="series", encoding='utf-8-sig'))
        
        # Load negative Array into Dataframe and add Column with "0" for beeing negative Example
        neg_df = pd.DataFrame.from_dict(neg_files)
        neg_df['Class']='0'
        
        # Load positive Array into Dataframe and add Column with "1" for beeing positive Example
        pos_df = pd.DataFrame.from_dict(pos_files)
        pos_df['Class']='1'
        
        # Merge the Dataframes from above
        df = pd.concat([neg_df, pos_df])
        
        # Write .csv-File
        with self.output().open("w") as out:
            df.to_csv(out, encoding="utf-8")





