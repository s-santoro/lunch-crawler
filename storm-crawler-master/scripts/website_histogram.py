#!/usr/bin/env python
# coding: utf-8

# # Notebook Websites-Histogramm
# 
# Mit diesem Notebook kann ein Histogramm erstellt werden.  
# Das Histogramm zeigt auf, wie viele Webpages eine Website beinhaltet.  
# Dieses Notebook soll die spätere Entscheidung für das allfällige Entfernen von Websites unterstützen.

# In[12]:


from os import listdir
from os import remove
import pandas as pd
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import tkinter # all fine
import operator
import collections
import re
pathToGermanFiles = "./Output"
pathToNonGermanFiles = "./Output_non_german"
n = 0


# Load all Files into Array
germanFilenames = [f for f in listdir(pathToGermanFiles)]
files = []
websiteHisto = {}
for filename in germanFilenames:
    filepath = pathToGermanFiles+"/"+filename
    file = pd.read_json(filepath, typ="series", encoding='utf-8-sig')
    url = file['url']
    url = re.sub(r'(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)', '', url)
    url = re.sub(r'(\/|\?).*$', '', url)

    if url in websiteHisto:
        websiteHisto[url] += 1
    else:
        websiteHisto[url] = 1

nonGermanFilenames = [f for f in listdir(pathToNonGermanFiles)]
for filename in nonGermanFilenames:
    filepath = pathToNonGermanFiles+"/"+filename
    file = pd.read_json(filepath, typ="series", encoding='utf-8-sig')
    url = file['url']
    url = re.sub(r'(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)', '', url)
    url = re.sub(r'(\/|\?).*$', '', url)

    if url in websiteHisto:
        websiteHisto[url] += 1
    else:
        websiteHisto[url] = 1  

filteredFiles = []
listHist = []

print("Anzahl von Webpages pro Website:")
for key, value in sorted(websiteHisto.items(), reverse=True, key=lambda item: item[1]):
    listHist.append(value)
    if value > n:
        #filteredFiles.append(key)
        print("\t%s: %s" % (key, value))

# create histo-plot
y_pos = np.arange(1, len(listHist)+1)

# LINE PLOT
fig, ax = plt.subplots()
ax.plot(y_pos, listHist)
ax.set(xlabel="Seed", ylabel="Anzahl Webpages")
ax.grid()
fig.savefig("histo.png")

# BAR PLOT
#plt.bar(y_pos, listHist, align='center', alpha=0.5)
#plt.ylabel('Anzahl Webpages')
#plt.title('Histogramm Anzahl Webpages pro Website')
#plt.savefig('histogramm.png')

print(len(y_pos))
print(listHist)
print(len(listHist))

# for filename in filenames:
#     filepath = pathToFiles+"/"+filename
#     file = pd.read_json(filepath, typ="series", encoding='utf-8-sig')
#     url = file['url']
#     for filteredFile in filteredFiles:
#         #print(filteredFile)
#         if filteredFile in url:
#                 try:
#                         remove(filepath)
#                 except FileNotFoundError:
#                         print("failed to delete: %s" % filepath)
            
    

