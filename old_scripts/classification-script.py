
# coding: utf-8

# In[1]:


import os, glob, pandas as pd, random


# In[2]:


os.chdir("C://Users//Ruben//Documents//GitHub//dhl-ads//test_ads")


# In[3]:


df = pd.read_csv('test-batch.csv', sep = '\t')
df = df.sample(n=200)
df = df.reset_index(drop=True)


# In[ ]:


df_oc = pd.DataFrame()

for i, ad in enumerate(df.ocr):
    print(ad)
	
    n = input("ad or something else?")
    if n == 'y':
        tmp = pd.DataFrame([ad])
        tmp['class'] = "ad"
        tmp['id'] = df.id[i]
        df_oc = df_oc.append(tmp)
        print(' ')
        print(' ')
    if n == 'n':
        tmp = pd.DataFrame([ad])
        tmp['class'] = "noad"
        tmp['id'] = df.id[i]
        df_oc = df_oc.append(tmp)
        print(' ')
        print(' ')


		
df_oc.to_csv('classified-ads.csv')