#!/usr/bin/env python
# coding: utf-8

# ## Comment:
# 
# This script will convert Json files to a panda format.
# 
# In the Json format each row company contains a list of directors which needs to be divided into director records 
# 
# We then convert the Panda Data frame and export the file as a CSV file 

# In[1]:


import json

with open('/project/HealthTechDirectors.json') as f:
    data = json.load(f)


# In[2]:


import pandas as pd


# In[3]:


df = pd.read_json('/project/HealthTechDirectors.json', orient='records')


# In[4]:


df


# In[5]:


# splitting all individual direcotrs into individual records 
officer = df["Officers"]
individual = officer[0][1]
d = pd.DataFrame.from_dict(individual, orient='index')
d = d.T
d


# In[6]:


sum(df["NumberOfCurrentOfficers"])


# In[7]:


# a for loop is used to create individual records 
individual_directors = pd.DataFrame()
for i in range(0,len(df)):
    officer = df["Officers"][i]
    d = pd.DataFrame(officer)
    company_number = df["_id"][i]
    d["CompanyNumber"] = company_number
    individual_directors = pd.concat([individual_directors,d], axis=0)
    individual_directors = individual_directors.reset_index()
    individual_directors = individual_directors.drop(["index"], axis = 1)
    


# In[8]:


cols = list(individual_directors)
cols.insert(0, cols.pop(cols.index('CompanyNumber')))
individual_directors = individual_directors.loc[:, cols]


# In[9]:


individual_directors


# In[11]:


individual_directors.to_csv("individual_directors.csv", index = False)

