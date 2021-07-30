#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'


# In[2]:


df = pd.read_csv('/project/finalcleanv2.csv')


# In[3]:


df["Integration_ID"]=""


# In[4]:


df["NumberRole_Inte"]=""


# In[5]:


df["NumberRole"] = df["DirectorNumber"]+"," + df["Role"]


# In[6]:


df = df.rename(columns = {"CompanyNumber" : "Companynumber","Appointed on": "Appointedon", "Resignation Date":"ResignationDate"})


# ### comments:
# 
# ### The following codes will create a new row of data representing director to another director who has worked within the same company (company number)
# 
# ### for example director_x -[company123] - director_y 
# 
# 
# ### director_x -[company123] - director_z

# In[8]:


#group data using company number 
df2 = df.groupby(['Companynumber'])['NumberRole'].apply(';'.join).reset_index()


# In[9]:


for x in range(0,len(df2)):
    for y in df["Companynumber"]:
            if df2["Companynumber"][x] == y:
                df["NumberRole_Inte"].loc[df["Companynumber"] == y] = df2["NumberRole"][x]


# In[10]:


for x in range(0,len(df)):
    df["NumberRole_Inte"][x]= df["NumberRole_Inte"][x].replace((df["NumberRole"][x]+";"),"")


# In[11]:


for x in range(0,len(df)):
    df["NumberRole_Inte"][x]= df["NumberRole_Inte"][x].replace((df["NumberRole"][x]),"")


# In[12]:


for x in range(0,len(df)):
    if df["NumberRole_Inte"][x] == df["NumberRole"][x]:
        df["NumberRole_Inte"][x] = "o"


# In[14]:


#df.to_csv("leedshealthtech1.csv", index = False)


# In[15]:


df3 = df.assign(NumberRole_Inte=df.NumberRole_Inte.str.split(";")).explode('NumberRole_Inte')


# In[16]:


# to make sure director x does not create a row with themselves
df5 = df3[df3['NumberRole'] != df3['NumberRole_Inte']]


# In[17]:


#Reformat into a new dataframe 
df5 = df5[["DirectorNumber","Fullname","Role","NumberRole","Appointedon", "ResignationDate","Companynumber","Companyname","NumberRole_Inte"]]


# In[18]:


df5 = df5.reset_index()
df5 = df5.drop(["index"], axis = 1)


# In[19]:


crossjoin = df5.loc[df5['NumberRole_Inte'] != '']


# In[21]:


#crossjoin.to_csv("integration_id.csv", index = False)


# In[22]:


#get the start date of the secondary director, Director_y
crossjoin["StartDate_y"]= ""


# In[23]:


crossjoin["EndDate_y"]=""


# In[24]:


crossjoin=crossjoin.reset_index()


# In[25]:


for i in range(0,len(crossjoin)):
    for j in df["NumberRole"]:
        if crossjoin["NumberRole_Inte"][i]==j:
            z=df.loc[df["NumberRole"] == str(crossjoin["NumberRole_Inte"][i])]
            crossjoin["StartDate_y"][i]=z.iloc[0]["Appointedon"]
            crossjoin["EndDate_y"][i]=z.iloc[0]["ResignationDate"]
            


# In[28]:


# a current director will not have a reisgnation, therefore we assume they will resignation on the deadline of this project
crossjoin=crossjoin.fillna(20210802)


# In[29]:


crossjoin = crossjoin.reset_index()
crossjoin = crossjoin.drop(crossjoin[["level_0","index"]],axis = 1)


# In[30]:


formatting = pd.DataFrame(crossjoin["NumberRole_Inte"].str.split(',', expand=True).values,
             columns=['DirectorNumber_y', 'Role_y'])


# In[31]:


crossjoin = crossjoin.drop(crossjoin[["NumberRole","NumberRole_Inte"]],axis = 1)


# In[32]:


crossjoin = crossjoin.merge(formatting, left_index=True, right_index=True)


# In[ ]:


# provides director with weighting score 


# In[33]:


crossjoin["isDirector_x"]=""
crossjoin["isDirector_y"]=""
crossjoin["isActive_x"]=""
crossjoin["isActive_y"]=""


# In[34]:


for i in range(0,len(crossjoin)):
    if crossjoin["Role"][i].endswith("DIRECTOR"):
        crossjoin["isDirector_x"][i] = 1
    else:
        crossjoin["isDirector_x"][i] = 0.5


# In[35]:


for i in range(0,len(crossjoin)):
    if crossjoin["Role_y"][i].endswith("DIRECTOR"):
        crossjoin["isDirector_y"][i] = 1
    else:
        crossjoin["isDirector_y"][i] = 0.5


# In[36]:


for i in range(0,len(crossjoin)):
    if crossjoin["Role"][i].startswith("CURRENT"):
        crossjoin["isActive_x"][i] = 1
    else:
        crossjoin["isActive_x"][i] = 0.5


# In[37]:


for i in range(0,len(crossjoin)):
    if crossjoin["Role_y"][i].startswith("CURRENT"):
        crossjoin["isActive_y"][i] = 1
    else:
        crossjoin["isActive_y"][i] = 0.5


# In[38]:


#crossjoin.to_csv("crossjoin_new.csv",index = False)


# # Overlapping

# ### The following code will calculate the days director_x has worked with director_y based on their start and end dates

# In[39]:


from datetime import datetime
from collections import namedtuple


# In[40]:


#crossjoin=pd.read_csv("/project/crossjoin_new.csv")


# In[41]:


crossjoin["overlap"]=""


# In[42]:


crossjoin.astype({'StartDate_y':"float","Appointedon":"float"}).dtypes


# In[43]:


#convert data into a datetime format
crossjoin['Appointedon'] =  pd.to_datetime(crossjoin['Appointedon'], format='%Y%m%d')
crossjoin['ResignationDate'] =  pd.to_datetime(crossjoin['ResignationDate'], format='%Y%m%d')
crossjoin['StartDate_y'] =  pd.to_datetime(crossjoin['StartDate_y'], format='%Y%m%d')
crossjoin['EndDate_y'] =  pd.to_datetime(crossjoin['EndDate_y'], format='%Y%m%d')


# In[44]:


# Range = namedtuple('Range', ['start', 'end'])

# r1 = Range(start=datetime(2012, 1, 15), end=datetime(2012, 5, 10))
# r2 = Range(start=datetime(2012, 3, 20), end=datetime(2012, 9, 15))
# latest_start = max(r1.start, r2.start)
# earliest_end = min(r1.end, r2.end)
# delta = (earliest_end - latest_start).days + 1
# overlap = max(0, delta)
# overlap


# In[45]:


# apply the calculation for each row
for i in range(0,len(crossjoin)):
    r1 = Range(start=crossjoin['Appointedon'][i], end=crossjoin['ResignationDate'][i])
    r2 = Range(start=crossjoin['StartDate_y'][i], end=crossjoin['EndDate_y'][i])
    latest_start = max(r1.start, r2.start)
    earliest_end = min(r1.end, r2.end)
    delta = (earliest_end - latest_start).days + 1
    overlap = max(0, delta)
    crossjoin["overlap"][i] = overlap


# In[46]:


crossjoin=crossjoin[crossjoin["overlap"] != 0]


# In[47]:


overlap = crossjoin


# In[48]:


overlap["weight"]=overlap["isActive_x"]*overlap["overlap"]


# In[49]:


overlap["Day_x"]=overlap["ResignationDate"]-overlap["Appointedon"]
overlap["Day_y"]=overlap["EndDate_y"]-overlap["StartDate_y"]
overlap["Day_x"] = overlap["Day_x"].dt.days
overlap["Day_y"] = overlap["Day_y"].dt.days


# In[50]:


overlap.to_csv("overlap_finalv2.csv", index = False)


# # Appointment date comparison

# ### This code will delete the row if director_x was employed after director_y (using start date)

# In[51]:


time_compare = pd.read_csv("/project/overlap_final.csv")


# In[52]:


time_compare["is_early"]=""


# In[53]:


for i in range(0,len(time_compare)):
    if time_compare["Appointedon"][i]<time_compare["StartDate_y"][i] or time_compare["Appointedon"][i] == time_compare["StartDate_y"][i]:
        time_compare["is_early"][i]=True
    else:
        time_compare["is_early"][i]=False


# In[54]:


time_compare["is_early"].value_counts()


# In[55]:


earliest_d = time_compare.loc[time_compare["is_early"]==True]


# In[56]:


#earliest_d.to_csv("earliest_leedstech.csv", index = False)


# In[ ]:




