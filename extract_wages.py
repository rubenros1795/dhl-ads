import os, glob, pandas as pd
import string, re
import numpy as np
from collections import Counter
import numbers
from string import ascii_lowercase
import pandas as pd
import time
from operator import itemgetter
from functions_2 import ExtractOccupations
from functions_2 import hasNumbers
from functions_2 import ExtractQual
from functions_2 import GetNum
from functions_2 import NumberCandidateClass
from functions_2 import ExtractNum
from functions_2 import NonNumbClass
from functions_2 import NormalizeNumbers
from functions_2 import Subset
import pickle
from nltk import ngrams
from flashtext import KeywordProcessor
from tqdm import tqdm

path_base = os.getcwd()

path_data = path_base + '/data'
os.chdir(path_data)

list_csv = glob.glob('*occupations.csv')

df = pd.read_csv(list_csv[0],sep = ',')
df['clean'] = [i.split(' ') for i in df.clean]

for c,i in enumerate(df['oc']):

    string = df['clean'][c]
    list_oc_ind = i
    processed_occupations = []
        if occupation_index in processed_occupations:
            continue
        processed_occupations.append(occupation_index)
        occupation = occupation_index.split('_')[0]
        occupations.append(occupation)
        index = int(occupation_index.split('_')[1])
        window = string[index-12:index+40]
        qual = ExtractQual(" ".join(window), qual_words)
        quan = ExtractNum(" ".join(window), qual_words)


df['clean'] = [" ".join(i) for i in df.clean]
fn = list_csv[0][:-4] + "_extracted_wages.csv"
df.to_csv(fn,index=False)
