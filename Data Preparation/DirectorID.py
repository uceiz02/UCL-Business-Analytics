#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import uuid


# In[13]:


director = pd.read_csv("/project/final-director.csv")
#cl = pd.read_csv("/project/companieslist_financialsColumnLayout_Health_Tech.csv")


# In[19]:


# Filter directors who are from Leeds using Post town
director = director.loc[director["Post Town"] == "LEEDS"]


# In[21]:


director =director.rename(columns = {"Column1":"Companynumber"})


# In[22]:


director["Address Line1"] = director["Address Line1"].fillna("no address")
director["Forenames"] = director["Forenames"].fillna("no forename")
director["DOB"] = director["DOB"].fillna("no DOB")
director["Surname"] = director["Surname"].fillna("no surname")


# ### Creating unique string identifier

# In[23]:


director["Fullname"] = director["Surname"] + " " + director["Forenames"]


# In[24]:


#director["Duplicates"] = director["Fullname"] + " " + str(director["Address Line1"]) + " " + str(director["DOB"])


# In[25]:


director["nameaddress"] = director["Fullname"] + " " + str(director["Address Line1"])


# In[26]:


director["namedob"] = director["Fullname"] + " " + str(director["DOB"])


# In[27]:


len(director)


# ### Removing duplicates (stage 1)

# In[29]:


stage_1 = director.drop_duplicates(subset=["Person Number"])
stage_1 = stage_1.reset_index()
stage_1 = stage_1.drop(["index"], axis = 1)


# In[30]:


len(stage_1)


# In[31]:


#now: duplicated person number is removed, only remain will be same director, different person number 


# ### Removing duplicates (stage 2)

# In[32]:


stage_2 = stage_1.drop_duplicates(subset=["nameaddress"])
stage_2 = stage_2.reset_index()
stage_2 = stage_2.drop(["index"], axis = 1)


# In[33]:


len(stage_2)


# In[34]:


# now: people with different person number are removed, and we removed any duplicated address


# ### Removing duplicates (stage 3)

# In[35]:


stage_3 = stage_2.drop_duplicates(subset=["namedob"])
stage_3 = stage_3.reset_index()
stage_3 = stage_3.drop(["index"], axis = 1)


# In[36]:


#duplicate checker
# duplicateRowsDF = stage_3[stage_3.duplicated(["Fullname"])]
# print(duplicateRowsDF)


# In[39]:


stage_3["DirectorNumber"] = ""


# In[40]:


# Now we generate our unqiue director number
for i in range(0,len(stage_3)):
    directorid = uuid.uuid4().hex[:8]
    stage_3["DirectorNumber"][i]= directorid


# In[41]:


len(stage_3)


# ### Formatting

# In[23]:


unique_director = director.copy()


# In[24]:


#unique_director["Fullname"] = unique_director["Surname"] + " " + unique_director["Forenames"]


# In[25]:


alist = stage_3[["Fullname","DirectorNumber"]]


# In[26]:


df = pd.merge(unique_director, alist, on='Fullname', how='outer')


# In[27]:


#df[df["DirectorNumber"].isna()]
#df[df["DirectorNumber"].isna()]["Person Number"]


# In[ ]:





# In[28]:


len(df["DirectorNumber"].unique())


# In[29]:


cols = list(df)
cols.insert(0, cols.pop(cols.index('DirectorNumber')))
df = df.loc[:, cols]


# ### COMPANY FILTER

# In[30]:


# the following code will classify if a director is a company 
df["isCompany"]=""


# In[31]:


# alternatively a row without forenames can be another rule to identify director 
for i in range(0,len(df)):
    if df["Surname"][i].endswith("LIMITED") or df["Surname"][i].endswith("LTD") or df["Surname"][i].endswith("LLP") or df["Surname"][i].endswith("LTD.") or df["Surname"][i].endswith("INC") or df["Surname"][i].endswith("SL"):
        df["isCompany"][i] = 1
    else:
        df["isCompany"][i] = 0


# In[32]:


df["isCompany"].value_counts()


# ### Active director filter

# In[33]:


# the following code will classify if a director is currently active or resigned 
df["isActive"]=""


# In[34]:


for i in range(0,len(df)):
    if df["Role"][i].startswith("CURRENT"):
        df["isActive"][i] = 1
    else:
        df["isActive"][i] = 0.5


# In[35]:


df["isActive"].value_counts()


# In[36]:


df = df.drop(["nameaddress","namedob"], axis = 1)


# # Director/Secretary

# In[37]:


# the following code will classify if a director is a director or secretary 
df["isDirector"]=""


# In[38]:


for i in range(0,len(df)):
    if df["Role"][i].endswith("DIRECTOR"):
        df["isDirector"][i] = 1
    else:
        df["isDirector"][i] = 0.5


# In[39]:


df = df[df.isCompany !=1]


# In[40]:


df = df.loc[df["Post Town"] == "LEEDS"]


# In[47]:


df


# In[48]:


df.to_csv("finalcleanv2.csv", index = False)


# In[41]:


#cl = cl[["Companynumber","Companyname"]]


# In[42]:


#dl = cl.merge(df, left_on="Companynumber", right_on="CompanyNumber")


# In[43]:


#dl = dl.drop(["CompanyNumber"],axis = 1)


# In[45]:


# if unique_director["Fullname"] == stage_3["Fullname"]:
#     unique_director["DirectorNumber"] = stage_3["DirectorNumber"]


# In[46]:


# for i in stage_3["DirectorNumber"]:
#     for x in range(0,len(unique_director["Fullname"])):
#         for y in range(0,len(stage_3["Fullname"])):
#             if unique_director["Fullname"][x] == stage_3["Fullname"][y]:
#                 unique_director["DirectorNumber"] = i

