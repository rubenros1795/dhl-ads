import os, glob, pandas as pd, random
from operator import itemgetter


os.chdir('C:\\Users\\Ruben\\Documents\\GitHub\\dhl-ads\\evaluation\\txt')

list_txt = glob.glob('*.txt')
list_integers = [int(i.split("_")[0]) for i in list_txt]

list_tuples = zip(list_txt,list_integers)
list_tuples = sorted(list_tuples, key=lambda tup: tup[1])

print(list_tuples[0])
for txt,count in list_tuples:

    occupation = txt.split("_")[0]
    with open(txt) as fp:
        window = fp.readline()

    print(txt)
    print(occupation)
    print(window)
    occupation_annotation = input("occupation:    ")
    wage_annotation = input("wage:    ")
    print('==================================================')

    list_results = [occupation_annotation, wage_annotation, window]

    fn = txt[:-4] + "_annotation.txt"
    with open(fn, 'w', encoding = 'utf-8') as the_file:
        the_file.write("\n".join(list_results))
