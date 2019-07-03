#!/usr/bin/env python
# coding: utf-8

# Imports
from luigi.contrib.spark import PySparkTask
from luigi.parameter import IntParameter
from luigi import LocalTarget, Task, WrapperTask
from luigi.format import UTF8
from os import listdir
import pandas as pd
import datetime

class Importer(Task):
    
    # Date for Output-File prefix
    from datetime import date
    date = datetime.datetime.now()
    configId = IntParameter(default=0)


    # Method to declare the Output-File
    def output(self):
        prefix = self.date.strftime("%Y-%m-%dT%H%M%S")
        return LocalTarget("./logs/%s_Importer_out.csv" % (prefix), format=UTF8)
    
    # Method to generate the Output-File
    def run(self):
        # Load all Files into Array
        filenames = [f for f in listdir("./input")]
        files = []
        for filename in filenames:
            filepath = "./input/"+filename
            files.append(pd.read_json(filepath, typ="series", encoding='utf-8-sig'))
        
        # Load Array into Dataframe
        df = pd.DataFrame.from_dict(files)
        df['filename'] = filenames
        
        # Write .csv-File
        with self.output().open("w") as out:
            df.to_csv(out, encoding="utf-8")
