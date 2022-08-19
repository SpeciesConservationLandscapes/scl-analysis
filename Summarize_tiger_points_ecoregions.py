#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import csv
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


# In[2]:


# working directory
wdir = r'C:\Users\esanderson\Documents\jupyter_notebooks\tiger_obs_ecoregions'


# In[3]:


# read spatial join of historical points into indigenous range into a dataframe (df)
csv_path_file = os.path.join(wdir, "union3_points_range_export_editted.csv")
df = pd.read_csv(csv_path_file)
df.set_index('FID_1', inplace=True, drop=True)


# In[5]:


with open(csv_path_file, newline='') as csvfile:
    ecoregion_source1 = {}
    ecoregion_allsources = {}
    reader = csv.DictReader(csvfile)
    for row in reader:
        #print (row)
        if row['Category_2'] == 'Indigenous range - resident - likely':
            # if the ecoregion already exists, append to the list in the dictionary
            if row['ECO_NAME_1'] in ecoregion_source1:
                ecoregion_source1[row['ECO_NAME_1']].append(row['Source1'])
                ecoregion_allsources[row['ECO_NAME_1']].append(row['Source1'])
                # append all the other source rows
                ecoregion_allsources[row['ECO_NAME_1']].append(row['Source2'])
                ecoregion_allsources[row['ECO_NAME_1']].append(row['Source3'])
                ecoregion_allsources[row['ECO_NAME_1']].append(row['Source4'])
                ecoregion_allsources[row['ECO_NAME_1']].append(row['Source5'])
                ecoregion_allsources[row['ECO_NAME_1']].append(row['Source6'])
                #checking everybody is in the list
                #print(row['ECO_NAME_1'], ecoregion_allsources[row['ECO_NAME_1']])
            else:
                ecoregion_source1[row['ECO_NAME_1']] = [row['Source1']]
                ecoregion_allsources[row['ECO_NAME_1']] = [row['Source1']]

ecoregion_unique_sources = {}
for key in ecoregion_allsources:
    ecoregion_unique_sources[key] = sorted(set(ecoregion_allsources[key]))
    print (key, len(ecoregion_allsources[key]), ecoregion_unique_sources[key])

    


# In[ ]:




