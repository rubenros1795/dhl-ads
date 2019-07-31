## Mining Job Advertisements in 19th Century Newspapers


This repository contains the code for the project 'Mining Job Advertisements in 19th Century Newspapers'. The goal of the project is to extract information on wages in digitized newspaper advertisements. The data is acquired through the API of the National Library. Given the copyright restrictions of part of the data, the original data is not included in this repository.

Two .py scripts are necessary for the extraction of the wages:

`functions.py` contains several functions that are used to extract numerical and non-numerical information on wages. A classifier is used to extract relevant tokens. 

`process.py` loops over the .csv files that contains the original data. Based on a list of occupations, a new file is created that includes 'windows' around occupations. These windows (sequences of 62 tokens around the occupations) are used to delimit the range of text in which the classifier looks for wages. 

The data has to be stored in the `data` folder, while resources, such as lists of occupations and stopwords, are located in the `resources` folder. The folder `old_scripts` contains the scripts used for earlier attempts and the `analysis` folder includes scripts used to investigate the output. 

The classification is evaluated by the manual annotation of 1050 advertisements. The original .csv sample is found in the `data` folder (and can be used to replicate the result), while the annotated windows are found in the `evaluation/txt` folder.
