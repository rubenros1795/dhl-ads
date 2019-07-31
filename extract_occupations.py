import os, glob, pandas as pd
import string, re
import numpy as np
from collections import Counter
import numbers
from string import ascii_lowercase
import pandas as pd
import time
from operator import itemgetter
from functions import ExtractOccupations
from functions import hasNumbers
from functions import ExtractQual
from functions import GetNum
from functions import NumberCandidateClass
from functions import ExtractNum
from functions import NonNumbClass
from functions import NormalizeNumbers
from functions import Subset
import pickle
from nltk import ngrams
from flashtext import KeywordProcessor
from tqdm import tqdm

path_base = os.getcwd()

##### Import resources
path_resources = path_base + '//resources'
os.chdir(path_resources)

## Create List of Occupations
with open('list_occupations.txt', encoding = 'utf-8') as f:
    list_words = list(set(f.read().splitlines()))

with open('stopwords-nl.txt', encoding = 'utf-8') as f:
    stopwords = f.read().splitlines()

with open('qualitative_indicators.txt', encoding = 'utf-8') as f:
    qual_words = f.read().splitlines()

with open('wage_indicators.txt', encoding = 'utf-8') as f:
    wage_words = f.read().splitlines()

with open('negatives.txt', encoding = 'latin1') as f:
    negatives = f.read().splitlines()

print("resources imported: occupations, stopwords, qualitative indicators, wage indicators & negatives")

############# DATA PROCESSING #####
# After importing the resources, we loop over de data and extract occupations for every ad
# Then, we subset the dataframe and discard all ads that do not contain advertisements
# set path_data to 'data' folder where raw csvs are stored

path_data = path_base + '/data'
os.chdir(path_data)

list_csv = glob.glob('*.csv')

for csv in list_csv:
    df = pd.read_csv(csv,sep = '\t')
    df = df.sample(n=10)
    df = df.reset_index(drop=True)
    lines_count = len(df)
    print("dataframe imported: {} lines (ads)".format(lines_count))

    ## Clean Raw OCR and split, bind again for subsetting, subset based on job ad indicators
    df = Subset(df)

    ## Extract Occupations from ads and subset only ads w/occupations
    vocab = set([item for sublist in df['clean'] for item in sublist])
    list_words = [w for w in list_words if w not in negatives + stopwords]
    list_words = [w for w in list_words if len(w.split(' ')) == 1]
    list_words = list(set(list_words).intersection(vocab))
    print('{} keywords used'.format(len(list_words)))

    df['oc'] = ""
    for c,i in tqdm(enumerate(df['clean'])):
        df['oc'][c] = ExtractOccupations(i,list_words)

    df = df[(df['oc'] != "na")]
    df = df[df.oc.map(len)>0]
    df = df.reset_index(drop=True)
    print("occupation-containing ads subsetted: {} ads = {}% of subsetted ads".format(len(df),round(len(df) / lines_count * 100, 3)))

    #df.to_csv('test.csv',index=False)

    ## Loop over subsetted ads and extract wage information
    ## The windows are stored in a new dataframe


    lid = []
    ldate = []
    limg = []
    lpapt = []
    lwindow = []
    loccupation = []
    lqual = []
    lquan = []

    for c,list_oc_ind in enumerate(df['oc']):

        for c2,occupation_index in enumerate(list_oc_ind):
            id = df['id'][c].replace(":","") + '_' + str(c2)

            string = df['clean'][c]

            processed_occupations = []
            if occupation_index in processed_occupations:
                continue
            processed_occupations.append(occupation_index)

            occupation = occupation_index.split('_')[0]

            index = int(occupation_index.split('_')[1])

            window = string[index-12:index+40]
            qual = ExtractQual(" ".join(window), qual_words)
            quan = ExtractNum(" ".join(window), qual_words)

            lid.append(id)
            ldate.append(df['date'][c])
            limg.append(df['image_url'][c])
            lpapt.append(df['paper_title'][c])
            lwindow.append(" ".join(window))
            loccupation.append(occupation)
            lqual.append(qual)
            lquan.append(quan)

    df_windows = {"id":lid,"date":ldate,"image_url":limg,"paper_title":lpapt,"window":lwindow,'occupation':loccupation, "extracted_qual":lqual,"extracted_quan":lquan}
    df_windows = pd.DataFrame(df_windows)

    fn = csv[:-4] + "_windows.csv"
    df_windows.to_csv(fn,index=False,sep = "\t")
