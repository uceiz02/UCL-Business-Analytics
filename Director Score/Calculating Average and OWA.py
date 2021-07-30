#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from sklearn import preprocessing
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'


# In[2]:


pd.set_option('display.max_rows', 10)


# In[3]:


#health tech
#df = pd.read_csv("/project/centralityxcorrelation.csv",index_col=False)
#leeds tech
df = pd.read_csv("/project/centralityxfinalv2.csv", index_col=False)
owa = pd.read_csv("/project/weight_score.csv",index_col=False)


# In[4]:


# The following calculation will normalised the centrality score 
#df["normalized_BW"] = preprocessing.normalize(df["BW"])
df["normalized_BW"]=(df["BW"]-df["BW"].min())/(df["BW"].max()-df["BW"].min())
df["normalized_EG"]=(df["EG"]-df["EG"].min())/(df["EG"].max()-df["EG"].min())
df["normalized_Degree"]=(df["Degree"]-df["Degree"].min())/(df["Degree"].max()-df["Degree"].min())
df["normalized_Harmonic"]=(df["Harmonic"]-df["Harmonic"].min())/(df["Harmonic"].max()-df["Harmonic"].min())
#df["normalized_EG"] = preprocessing.normalize(df["EG"])
#df["normalized_Degree"] = preprocessing.normalize(df["Degree"])


# In[5]:


df


# In[6]:


df = df.rename(columns = {"Name":"name"})


# In[7]:


# df["IsDirector"].replace(0,0.5)
# df["IsActive"].replace(0,0.5)


# # Average
# 
# ### calculate the average using the normalized score

# In[8]:


df["Average"]=""


# In[9]:


df["Average"]=(df["normalized_BW"] + df["normalized_EG"] + df["normalized_Harmonic"] + df["normalized_Degree"])/4


# In[10]:


df['Average_rank'] = df['Average'].rank(method = "max",ascending = False)


# In[11]:


df[["name","Average","Average_rank"]]


# In[12]:


#df.loc[df["Average_rank"]==181.0]


# # Weight by active and role (not used in analysis)

# In[13]:


df["weight"]=df["IsDirector"]*df["IsActive"]*(df["Days"]/sum(df["Days"]))


# In[14]:


df["weighted_average"]=df["weight"]*df["Average"]


# In[15]:


df["weighted_rank"]=df["weighted_average"].rank(method ="max", ascending = False)


# In[16]:


df[["name","weighted_average","weighted_rank"]]


# # Rank (not used in analysis)

# In[18]:


#df["by_rank"] = (df['rank_BW'] + df['rank_EG'] + df['rank_Harmonic'] + df['rank_Degree'])/4


# In[19]:


#df["order"] = df["by_rank"].rank(method ="max", ascending = True)


# In[20]:


#df[["name","by_rank","order"]]


# # Order Weighted Average
# 
# ### the following code will use a for loop to provide each ranking a different weighting score 
# 

# In[17]:


# using the rank function to give each score a ranking 
df['rank_BW'] = df['BW'].rank(method = "max",ascending = False)
df['rank_EG'] = df['EG'].rank(method = "max",ascending = False)
df['rank_Harmonic'] = df['Harmonic'].rank(method = "max",ascending = False)
df['rank_Degree'] = df['Degree'].rank(method = "max",ascending = False)
df['rank_Days'] = df['Days'].rank(method = "max",ascending = False)


# In[21]:


df["sBW"]=""
df["sEG"]=""
df["sHarmonic"]=""
df["sD"]=""
df["sDays"]=""


# In[22]:


df["weighted_days"] = df["Days"]/sum(df["Days"])


# In[23]:


# for i in range(0,len(df)):
#     for j in owa["Rank"]:
#         if df["rank_Days"][i]==j:
#             z = owa["wDays"].loc[owa["Rank"]==df["rank_Days"][i]]
#             x = z.iloc[0]
#             df['sDays'][i] = df['Days'][i]*x


# In[24]:


# for each centarlity score, each ranking is given a different weighting. We then multiple the weighting with the original centrality
for i in range(0,len(df)):
    for j in owa["Rank"]:
        if df["rank_BW"][i]==j:
            z = owa["wBW"].loc[owa["Rank"]==df["rank_BW"][i]]
            x = z.iloc[0]
            df['sBW'][i] = df['BW'][i]*x


# In[25]:


for i in range(0,len(df)):
    for j in owa["Rank"]:
        if df["rank_EG"][i]==j:
            z = owa["wEG"].loc[owa["Rank"]==df["rank_EG"][i]]
            x = z.iloc[0]
            df['sEG'][i] = df['EG'][i]*x


# In[26]:


for i in range(0,len(df)):
    for j in owa["Rank"]:
        if df["rank_Harmonic"][i]==j:
            z = owa["wH"].loc[owa["Rank"]==df["rank_Harmonic"][i]]
            x = z.iloc[0]
            df['sHarmonic'][i] = df['Harmonic'][i]*x


# In[27]:


for i in range(0,len(df)):
    for j in owa["Rank"]:
        if df["rank_Degree"][i]==j:
            z = owa["wD"].loc[owa["Rank"]==df["rank_Degree"][i]]
            x = z.iloc[0]
            df['sD'][i] = df['Degree'][i]*x


# In[38]:


df["normalized_BW"]=(df["sBW"]-df["sBW"].min())/(df["sBW"].max()-df["sBW"].min())
df["normalized_EG"]=(df["sEG"]-df["sEG"].min())/(df["sEG"].max()-df["sEG"].min())
df["normalized_Degree"]=(df["sD"]-df["sD"].min())/(df["sD"].max()-df["sD"].min())
df["normalized_Harmonic"]=(df["sHarmonic"]-df["sHarmonic"].min())/(df["sHarmonic"].max()-df["sHarmonic"].min())


# In[44]:


#generate a new average with a new centrality score
df["OWA"]=(df["sBW"]+df["sEG"]+df["sHarmonic"]+df["sD"])/4
#df["OWAv2"]=(df["sBW"]+df["sEG"]+df["sHarmonic"]+df["sD"]+df["sDays"])/5


# In[40]:


df["OWA_rank"] = df["OWA"].rank(method ="max", ascending = False)
#df["OWA_rankv2"] = df["OWAv2"].rank(method ="max", ascending = False)


# In[41]:


df[["name","OWA","OWA_rank"]]


# # Weighted OWA

# In[42]:


# add further weighting into the OWA score
df["weighted_OWA"]=df["OWA"]*df["weighted_days"]*df["IsActive"]*df["IsDirector"]
df["weighted_OWA_rank"] = df["weighted_OWA"].rank(method ="max", ascending = False)


# In[43]:


df[["name","weighted_OWA","weighted_OWA_rank"]]


# In[34]:


#df["weighted_OWAv2"]=df["OWAv2"]*df["IsActive"]*df["IsDirector"]


# In[35]:


#df["weighted_OWA_rankv2"] = df["weighted_OWAv2"].rank(method ="max", ascending = False)


# In[36]:


df.to_csv("final-averagev5.csv", index = False)


# In[ ]:




