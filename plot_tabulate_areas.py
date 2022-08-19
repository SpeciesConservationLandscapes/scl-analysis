# plot_tabulate_areas.py
# ews 7/30/2022

# for the tiger indigenous range analysis, this script reads two csv files 
#   eco_divide_names.csv = identifying the ecoregion/divide identities of poly_id (this is an export from TCL3_indigenous_range_07302022_ids_prj.shp)
#   tiger_habitat_polys.csv = the result of running summarize_tabulate_areas; in this case, the areas of tiger habitat for each poly_id at different points in time based on anthrome 12K analysis
# 
#  objective:  read back the csv, read in pandas df, then combine poly_ids by eco regions / divisions, then plot and analyze to find year of first significant human impact
#  the "first significant human impact" is defined as 10% change in habitat area compared to the amount of habitat 10,000 - 5000 years before present

#  note:  I'm sure there is a MUCH BETTER way to do this...

# imports
import sys
import os
import csv
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

# set up
anthromes_output = r'C:\proj\species\tigers\TCLs v3\historic range\anthrome analysis\tiger_habitat_stats'
anthromes_plots = r'C:\proj\species\tigers\TCLs v3\historic range\anthrome analysis\tiger_plots'
csv_file = os.path.join(anthromes_output, "tiger_habitat_polys.csv")
csv_file2 = os.path.join(anthromes_output, "eco_divide_names.csv")

# read in csv files to pandas df
df = pd.read_csv(csv_file)
df.set_index('Year', inplace=True, drop=True)
#print (df.head())
df_names = pd.read_csv(csv_file2)
df_names.fillna('-', inplace=True)
df_names.set_index('Poly_id')
#print (df_names.head())

# note that multiple polys have the same ecoregion and divide; these need to be grouped before plotting
df_groups = df_names.groupby(['ECO_NAME_1','Divide_1'])['Poly_id'].apply(list).reset_index(name='polys')
df_groups.to_csv(os.path.join(anthromes_plots, 'eco_divide_groups.csv'))
#print (display(df_groups.head))
#print (df_groups.iloc[0]['polys'], type(df_groups.iloc[0]['polys']))

# create a new df to hold group totals
df_group_totals = pd.DataFrame(index=df.index)
df_group_diffs = pd.DataFrame(index=df.index)
first_year_list = []
eco_list = []
divide_list = []
category_list = []

# cycle over rows plotting each with name and category
for group_id, row in df_groups.iterrows():

    # convert list of poly ids from int to strings
    poly_ids = [str(x) for x in row['polys']]

    # note some polys have effectively zero area (because of splinters) so don't appear in poly list; just set them to zero and keep goin
    for p in poly_ids:
       #print (group_id, p, type(p), df.iloc[0][p])
       if p in df.columns:
            #print ("poly ",p, " does exist")
            continue
       else:
            #print ("poly ",p, " does not exist")
            df[p] = 0
    # sum the areas in df by groups defined by list in df_groups['polys']
    df_group_totals[group_id] = df[poly_ids].sum(axis=1)
 
    # get eco name and divide
    econame = row['ECO_NAME_1']
    eco_list.append(econame)
    divide = row['Divide_1']
    divide_list.append(divide)
    category = df_names.iloc[row['polys'][0]]['Category_2']
    eco_divide = econame + "(" + divide + ")\n"
    plot_filename = str(group_id) + ".jpg"
    category_list.append(category)
    
    # get average of first five time points and then compare to other time points looking for threshold (e.g. 10%) change
    n = 5
    threshold = 0.1
    baseline_area = df_group_totals[group_id][:n].mean()
    df_group_diffs[group_id] = (df_group_totals[group_id]-baseline_area)/df_group_totals[group_id]
    matches = df_group_diffs.index[abs(df_group_diffs[group_id]) > threshold ].tolist()
    if not matches:
        year_first_significant_change = 'None'
    else:
        year_first_significant_change = matches[0]
    #print (group_id, max_value, year_first_significant_change)
    first_year_list.append(year_first_significant_change)
    

    # plot figure
    print ("Plotting: ", group_id, eco_divide)    
    plt.figure()
    plt.plot(df_group_totals[group_id]/1000000)  # if x axis isn't specified, pandas uses index; divide by a million to get km2
    plt.axvline(x = year_first_significant_change, color = 'r', linestyle = 'dashed')
    plt.title(eco_divide + category)
    plt.xlabel('Year')
    plt.ylabel('Tiger habitat area - km2')
    plot_file = os.path.join(anthromes_plots, plot_filename)
    plt.savefig(plot_file)
    plt.close()

# outputs
df_first_years = pd.DataFrame(
    {'econame': eco_list,
     'divide': divide_list,
     'first_year': first_year_list,
     'category': category_list
     },
     index=df_groups.index)

df_group_diffs.to_csv(os.path.join(anthromes_plots, 'ecoregion_divide_grouped_percent_diffs.csv'))
df_group_totals.to_csv(os.path.join(anthromes_plots, 'ecoregion_divide_grouped_results.csv'))
df_first_years.to_csv(os.path.join(anthromes_plots, 'first_year_significant_impact.csv'))