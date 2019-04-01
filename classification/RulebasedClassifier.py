#!/usr/bin/env python
# coding: utf-8

# In[17]:


# Imports
from luigi.contrib.spark import PySparkTask
from luigi.parameter import IntParameter, DateSecondParameter
from luigi.format import UTF8
from luigi import LocalTarget, Task, WrapperTask
import datetime
import pandas as pd
import re
from Preprocessor import Preprocessor
#get_ipython().magic(u'run Preprocessor.ipynb')

class RulebasedClassifier(Task):

    # Date for Output-File prefix
    from datetime import date, timedelta
    date = DateSecondParameter(default=datetime.datetime.now())
    
    # Method to declare the Output-File
    def output(self):
        prefix = self.date.strftime("%Y-%m-%dT%H%M%S")
        return LocalTarget("data/%s_Classifier_out.csv" % prefix, format=UTF8)
    
    # Method to define the required Task (Preprocessor)
    def requires(self):
        return Preprocessor()


    # Classify the imported Data
    def run(self):
        df = pd.read_csv(self.input().path)
        output_df = pd.DataFrame(columns=('specified', 'predicted'))
        output_df['specified'] = df['class'].values
        
        for index, document in df.iterrows():
            value = self.simpleTitleMenuFinder(document.text)
            output_df['predicted'].iloc[index] = value            
        
        # Write .csv-File
        with self.output().open("w") as out:
            output_df.to_csv(out, encoding="utf-8")
            
    def simpleTitleMenuFinder(self, text):
        if 'priceentity' in text:
            return 1
        else:
            return 0
    
#rbclassifier = RulebasedClassifier()
#rbclassifier.run()


# In[ ]:




