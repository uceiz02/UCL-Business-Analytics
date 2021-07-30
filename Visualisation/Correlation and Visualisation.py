#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np


# In[59]:


import matplotlib.ticker as plticker


# ### Comments:
# 
# ### the following codes will create series of visualisation on the director dataset, as well as generating a correlation matrix of the director centrality score

# In[2]:


correlation_df = pd.read_csv("/project/centralityxfinalv2.csv")


# In[3]:


correlation_df


# In[4]:


correlation_df = correlation_df[["Name","BW","EG","Harmonic","Degree","Days"]]


# In[5]:


#correlation_df.set_index('Betweenness (not reduced node)', inplace=True)


# In[6]:


# create a correlation table
correlation = correlation_df.corr()
# Generate a custom diverging colormap
cmap = sn.diverging_palette(230, 20, as_cmap=True)
# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(correlation, dtype=bool))


# In[7]:


# generating the correlation matrix
f, ax = plt.subplots(figsize=(16, 12))
ax = plt.axes()
sn.heatmap(correlation, annot=True,mask=mask, cmap=cmap, ax = ax)
#f.suptitle = "Correlation Matrix"
ax.set(title = "Correlation Matrix")
sn.set(font_scale=2)
plt.show()


# In[71]:


# for each correlation test, we create a sub-plot for more in-depth analysis
fig, axs = plt.subplots(3,4, figsize=(50,25))
fig.suptitle('Correlation subplots')
plt. subplots_adjust(left=0.2, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
axs[0,0].plot(correlation_df["BW"], correlation_df["EG"],"o")
axs[0,0].set_xlabel('Betweenness')
axs[0,0].set_ylabel('Eigenvector')
axs[0,1].plot(correlation_df["BW"], correlation_df["Harmonic"],"o")
axs[0,1].set_xlabel('Betweenness')
axs[0,1].set_ylabel('Harmonic')
axs[0,2].plot(correlation_df["BW"], correlation_df["Degree"],"o")
axs[0,2].set_xlabel('Betweenness')
axs[0,2].set_ylabel('Degree')
axs[0,3].plot(correlation_df["BW"], correlation_df["Days"],"o")
axs[0,3].set_xlabel('Betweenness')
axs[0,3].set_ylabel('Days')
#axs[1,0].sharex(axs[0,0])
axs[1,0].plot(correlation_df["Harmonic"], correlation_df["EG"],"o")
axs[1,0].set_xlabel('Harmonic')
axs[1,0].set_ylabel('Eigenvector')
axs[1,1].plot(correlation_df["Harmonic"], correlation_df["Degree"],"o")
axs[1,1].set_xlabel('Harmonic')
axs[1,1].set_ylabel('Degree')
axs[1,2].plot(correlation_df["Harmonic"], correlation_df["Days"],"o")
axs[1,2].set_xlabel('Harmonic')
axs[1,2].set_ylabel('Days')
axs[1,3].plot(correlation_df["EG"], correlation_df["Degree"],"o")
axs[1,3].set_xlabel('Eigenvector')
axs[1,3].set_ylabel('Degree')
axs[2,0].plot(correlation_df["EG"], correlation_df["Days"],"o")
axs[2,0].set_xlabel('Eigenvector')
axs[2,0].set_ylabel('Days')
axs[2,1].plot(correlation_df["Degree"], correlation_df["Days"],"o")
axs[2,1].set_xlabel('Degree')
axs[2,1].set_ylabel('Days')
axs[2,2].set_axis_off()
axs[2,3].set_axis_off()


# ## Visualisation

# In[9]:


import matplotlib.pyplot as plt


# In[10]:


vis = pd.read_csv("/project/crossjoin_new.csv")


# In[11]:


vis = vis.drop_duplicates(subset=["DirectorNumber"])


# In[12]:


type(vis["isDirector_x"][0])


# In[13]:


vis["isDirector_x"] = vis["isDirector_x"].astype(int)


# In[14]:


vis


# In[ ]:


#create a visualisation of the percentage of director within the dataset


# In[15]:


labels = ["Director", "Secretary/Other"]
explode = (0.05,0.1) 
vis.isDirector_x.value_counts().plot(kind='pie', labels = labels, explode=explode,autopct='%1.1f%%', figsize = (7,7), ylabel = "", title = "Director role comparison", fontsize = 25)


# In[16]:


#create a visualisation of the percentage of director who is currently active within the dataset
labels1 = ["Resigned", "Active"]
explode = (0.05,0.1) 
vis.isActive_x.value_counts().plot(kind='pie', labels = labels1, ylabel = "", explode=explode,autopct='%1.1f%%', figsize = (7,7),  title = "Active / Resigned Director comparison", fontsize = 25)


# In[72]:


# creating a plot to see the number of appointments and resignation occured within the dataset
vis['Appointed on'] =  pd.to_datetime(vis['Appointed on'], format='%Y%m%d')
vis['Resignation Date'] =  pd.to_datetime(vis['Resignation Date'], format='%Y%m%d')


# In[18]:


# take only the year as a year variable
vis["Year"]= vis['Appointed on'].dt.year


# In[19]:


vis["Year_y"] = vis["Resignation Date"].dt.year


# In[60]:


# use value_count to get the number of occurance in years
x = pd.DataFrame(vis.Year.value_counts())
x = x.sort_index(ascending = True)


# In[70]:


x.plot(figsize = (7,7), title = "Appointment Frequency against time", xlabel = "Year of Appointment", ylabel = "Frequency")


# In[69]:


y = pd.DataFrame(vis.Year_y.value_counts())
y = y.sort_index(ascending = True)
y= y.drop(2021)
y.plot(figsize = (7,7), title = "Resignation Frequency against time", xlabel = "Year of Resignation", ylabel = "Frequency")


# In[ ]:





# In[ ]:




