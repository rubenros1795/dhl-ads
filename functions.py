
###     PREPARATION     ####
from string import ascii_lowercase
import pandas as pd
import re
import pickle
import itertools
from nltk import ngrams
import string

##      SUBSETTING   ##
def Subset(df):
    lines_count = len(df)
    def clean_and_split_str(txt):
        #strip_special_chars = re.compile("[^A-Za-z0-9#]+")
        translator = str.maketrans('', '', string.punctuation)
        txt = txt.translate(translator)
        txt = re.sub('\s+', ' ', txt).strip()
        txt = txt.lower()
        txt = txt.split(' ')
        return txt

    df['clean'] = [clean_and_split_str(i) for i in df.ocr]


    df['clean'] = [" ".join(i) for i in df.clean]
    df = df[df['clean'].str.contains("|".join(["gevraagd","men verlangt","verlangt men","gelegenheid ter plaatsing","getuigen voorzien","loon","salaris","jaarwedde","franco"]))]
    df = df.reset_index(drop=True)
    print("wage advertisement subsetted:  {} ads = {}% of total ads in data".format(len(df),round(len(df) / lines_count * 100, 3)))
    df['clean'] = [i.split(" ") for i in df.clean]
    lines_count = len(df)

    return df


def ExtractOccupations(string, list_words):
    #extracted_occupations = keyword_processor.extract_keywords(" ".join(string))
    extracted_occupations = [w for w in string if w in list_words]

    if len(extracted_occupations) == 0:
        occupations_indices = "na"

    else:
        occupations_indices = []

        for oc in extracted_occupations:

            # check if there is only one:
            if len([o for o in string if o == oc]) == 1:
                oc_ind = oc + '_' + str(string.index(oc))
                occupations_indices.append(oc_ind)

            if len([o for o in string if o == oc]) > 1:

                indices = [index for index, c in enumerate(string) if c == oc]
                oc_ind = zip([o for o in string if o == oc], indices)
                oc_ind = [k + "_" + str(v) for k,v in oc_ind]

                for oc_instance in oc_ind:
                    occupations_indices.append(oc_instance)

    return occupations_indices

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


##      CLASSIFICATION  ##
## Check Qualitative Indcators
def ExtractQual(string, qual_words):
    s= string.split(' ')
    loon = 'na'

    list_qualitative_wage_indicators=qual_words

    s_unigrams = s
    s_bigrams = ["_".join(list(i)) for i in ngrams(s, 2)]
    s_trigrams = ["_".join(list(i)) for i in ngrams(s, 3)]
    s_fourgrams = ["_".join(list(i)) for i in ngrams(s, 4)]

    uni_bi= s_unigrams + s_bigrams + s_trigrams + s_fourgrams

    if any(x in uni_bi for x in list_qualitative_wage_indicators):

        qualitative_wage = list([i for i in uni_bi if i in list_qualitative_wage_indicators])

        if len(qualitative_wage) > 0:
            loon = [loon for loon in list(set(qualitative_wage))]
            loon = " ".join(loon)
            loon = loon.replace("_"," ")
            if loon is None:
                loon = "na"
            return loon

        else:
            loon = "na"
            return loon
    else:
        loon = "na"
        return loon

## Extract Numbers
def GetNum(string, wage_words):
    s = string.split(' ')
    all_numbers = []

    for i,w in enumerate(s):
        if hasNumbers(w) == True or w in wage_words:
            all_numbers.append([i, w])

    nonnum = NonNumbClass(string)

    if nonnum != "na":
        all_numbers.append(nonnum)
    else:
        pass
    return all_numbers

## Classify Numbers
def NumberCandidateClass(string, index, number_candidate):
    string = string.split(' ')
    ## Set Variables
    score = 0
    weights = 0
    features = []
    len_string = len(string) - 1
    number_candidate = str(number_candidate)

    # Negative
    if len(number_candidate) > 4:
        score += -1
        weights += 1
        features.append('n1')
    if number_candidate[0:2] == "18" and len(number_candidate) == 4:
        score += -1
        weights += 1
        features.append('n2')
    try:
        for n in [-3,-2,-1,1,2,3,4]:
            if string[index+n] in ['januari', 'februari', 'februarij', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november', 'december']:
                score += -1
                weights += 1
                features.append('n3')
    except IndexError:
        pass

    try:
        for n in [1,2,3,4]:
            if string[index+n][0:2] == "18" and len(string[index+n]) == 4:
                score += -1
                weights += 1
                features.append('n4')
    except IndexError:
        pass

    # Positive
    if string[index-1] == "f" or string[index-1] == 'ƒ':
        score += 1
        weights += 1
        features.append('p1')
    if number_candidate[0] == "f" or number_candidate[0] == 'ƒ':
        score += 1
        weights += 1
        features.append('p2')
    if string[index-1] == "van":
        score += 1
        weights += 1
        features.append('p3')
    if string[index-1] == "Æ’" or string[index-1] == 'Æ’':
        score += 1
        weights += 1
        features.append('p4')
    if number_candidate[0:2] == "Æ’" or number_candidate[0] == 'Æ':
        score += 1
        weights += 1
        features.append('p5')
    try:
        if string[index+1] == "gulden" or string[index+2] == "gulden":
            score += 2
            weights += 1
            features.append('p6')
    except IndexError:
        pass

    try:
        for n in [1,2,3,4]:
            if string[index-n] in ['loon', 'salaris','beloning','jaarwedde', 'provisie'] or string[index-n] in ['loon', 'salaris','beloning','jaarwedde', 'provisie']:
                score += 2
                weights += 1
                features.append('p7')
    except IndexError:
        pass

    try:
        if string[index-1] == 'tegen' or string[index-2] == 'tegen':
            score += 1
            weights += 1
            features.append('p7')
    except IndexError:
        pass

    try:
        if string[index+1] == "per" or string[index+2] == "per":
            weights += 1
            score += 1
            features.append('p8')
    except IndexError:
        pass

    try:
        if string[index+1] == "ongeveer":
            score += 1
            weights += 1
            features.append('p9')
    except IndexError:
        pass

    try:
        if "jaar" in string[index+1]:
            score += 1
            weights += 1
            features.append('p10')
    except IndexError:
        pass

    try:
        for n in [-4,-3,-2,-1,1,2,3,4]:
            if string[index+n] in ['loon', 'salaris','beloning','jaarwedde']:
                score += 1
                weights += 1
                features.append('p1')
    except IndexError:
        pass

    #print(features)
    return score

def ExtractNum(string, wage_words):
    list_numbers = GetNum(string, wage_words)
    list_scores = list(zip([number for ind,number in list_numbers], [NumberCandidateClass(string, ind, number) for ind, number in list_numbers]))
    if len(list_scores) > 0 and max([score for loon,score in list_scores]) > 0:
        winning_number = max([score for loon,score in list_scores])
        loon =  [loon for loon,score in list_scores if score == winning_number][0]
    else:
        loon = "na"
    return loon

## Detect Non-Numerical
def NonNumbClass(string):
    s = string.split(' ')
    candidates = []

    f_instances = [w for w in s if "ƒ" in w and hasNumbers(w) == False]

    for f in f_instances:

        if len(f) > 1 and f[0] == 'ƒ':
            candidates.append(f)

        if len(f) == 1:
            f_index = s.index(f)

            try:
                if "o" in s[f_index + 1]:
                    candidates.append(" ".join(s[f_index:f_index + 1]))
            except IndexError:
                pass
    if len(candidates) == 0:
        candidates = "na"
        return candidates
    else:
        index_candidate = s.index(candidates[0])
        return [index_candidate,candidates[0]]

##      NORMALIZING      ##
## Confert Numerical and Non-Numerical Wages in Integers

def NormalizeNumbers(df):
    dfa = df
    for i in range(len(dfa)):
        if dfa['ex_num'][i] != "na":
            s = dfa['ex_num'][i]
            s = s.replace("o", "0")
            s = s.replace("l", "1")
            s = s.replace("—", "")
            s = ''.join([i for i in s if not i.isalpha()])
            s = re.sub(r'\W+', '', s)

            if len(s) > 0:
                dfa['ex_num'][i] = int(s)
            else:
                continue
        else:
            continue

    for i in range(len(dfa)):
        if dfa['ex_nonnum'][i] != "na":
            s = dfa['ex_nonnum'][i]
            s = s.replace("o", "0")
            s = s.replace("l", "1")
            s = s.replace("b", "10")
            s = s.replace("ƒ", "")
            s = ''.join([i for i in s if not i.isalpha()])
            s = re.sub(r'\W+', '', s)

            if len(s) > 0:
                dfa['ex_nonnum'][i] = int(s)
            else:
                continue
        else:
            continue

    return dfa
