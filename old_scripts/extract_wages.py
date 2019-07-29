import os, glob, pandas as pd
import string, re
import numpy as np
from collections import Counter
import numbers
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from string import ascii_lowercase
import requests
import shutil
import pandas as pd
import time
from nltk import ngrams
from operator import itemgetter
from functions import ExtractWindows
from functions import hasNumbers
from functions import ExtractQual
from functions import GetNum
from functions import NumberCandidateClass
from functions import ExtractNum
from functions import NonNumbClass
from functions import NormalizeNumbers
import pickle
from flashtext import KeywordProcessor

print("libraries imported")

##### Import resources
os.chdir("C://Users//Ruben//Documents//Artikelen//Joris")
with open('stopwords-nl.txt', encoding = 'utf-8') as f:
    stopz = f.read().splitlines()

os.chdir("C://Users//Ruben//Documents//GitHub//dhl-ads//resources")
with open('occupations_dictionary.pkl', 'rb') as handle:
    occ_dict = pickle.load(handle)

list_words = []
for k,v in occ_dict.items():
    k = k
    v = [x for x in v if x not in stopz and len(x) > 3]

    for x in v:
        list_words.append(x)
    list_words.append(k)

keyword_processor = KeywordProcessor()
for w in list_words:
    keyword_processor.add_keyword(w)

# Import QUAL Indicator list
os.chdir("C://Users//Ruben//Documents//GitHub//dhl-ads//resources")
with open('qualitative_indicators.txt', encoding = 'utf-8') as f:
    qual_words = f.read().splitlines()

# Import QUAL Indicator list
os.chdir("C://Users//Ruben//Documents//GitHub//dhl-ads//resources")
with open('wage_indicators.txt', encoding = 'utf-8') as f:
    wage_words = f.read().splitlines()

print("resources imported")
####


os.chdir("C://Users//Ruben//Downloads//metadata//ads_all_1880s//split")

list_csv = glob.glob('*.csv')
for csv in list_csv:
    print(csv)
    df = pd.read_csv(csv, sep = '\t')

    def clean_and_split_str(txt):
        #strip_special_chars = re.compile("[^A-Za-z0-9#]+")
        translator = str.maketrans('', '', string.punctuation)
        txt = txt.translate(translator)
        txt = re.sub('\s+', ' ', txt).strip()
        txt = txt.lower()
        txt = txt.split(' ')
        return txt
    df['clean'] = [clean_and_split_str(i) for i in df.ocr]
    print("data cleaned")

    dfa = ExtractWindows(df, list_words,qual_words, keyword_processor)
    print("windows extracted")

    dfa['ex_qual'] = ""
    dfa['ex_num'] = ""

    for i in range(len(dfa)):

        dfa['ex_qual'][i] = ExtractQual(dfa['window'][i], qual_words)
        dfa['ex_num'][i] = ExtractNum(dfa['window'][i], wage_words)

    #NormalizeNumbers(dfa)

    fn = csv[:-4] + "_processed.csv"
    dfa.to_csv(fn, index = False)
