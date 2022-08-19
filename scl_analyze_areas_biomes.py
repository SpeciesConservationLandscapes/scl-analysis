# scl_analysis.6.py
# scl_analyze_areas_biomes.py
# ews 7/14/2022

# Read object and summarize the nested JSON in the "areas" field of the SCL output format
# this script calculates the total area of biomes in each landscape


# imports
import os
import geojson
import geopandas as gpd
import pandas as pd
import numpy as np
import json
from flatten_json import flatten
from pandas.io.json import json_normalize
import csv

# some set up

# the input data files organized by folder by time point are in this directory:
scl_dir = r"C:\proj\species\tigers\TCLs v3\TCL delineation\scl_stats_07032022"
# the type of datafile to analyze is
data_filename = "scl_species.geojson"
data_name_tuple = os.path.splitext(data_filename)
# the output file will go in this directory
#scl_analysis_dir = r"C:\proj\species\tigers\TCLs v3\TCL delineation\scl_stats_07032022\analysis"
# output file names
output_filename = "scl_biome_areas.csv"

# the years to analyze are:
#years = ['2020-01-01','2019-01-01','2018-01-01','2017-01-01','2016-01-01','2015-01-01','2014-01-01','2013-01-01','2012-01-01','2011-01-01','2010-01-01','2009-01-01','2008-01-01','2007-01-01','2006-01-01','2005-01-01','2004-01-01','2003-01-01','2002-01-01','2001-01-01']
# a single year for testing purposes
years = ['2020-01-01']


# Loop over years to generate a pandas df for each data_filename
for year in years:

    # Get filename for this year
    data_file = (os.path.join(scl_dir, year, data_filename))
    print ("Working on...", data_file)
    
    # Load file into Geopandas data frame
    data_gdf = gpd.read_file(data_file)
    # then drop the geometry part
    df_attributes = data_gdf.drop('geometry', axis=1)
    # and pick just the desired columns
    df = df_attributes[['id','areas','lscountry_area','lscountry','lsid']].copy()
    
    # Iterate over areas making a new df
    # see areas json structure EXPLAINED.txt for explanation of the structure of areas
    
    # set up an empty dictionary and list 
    biome_areas = {}
    biomes_list = []
    
    # iterate over rows in df
    for id, areas_str in zip(df['id'], df['areas']):
        areas_list = json.loads(areas_str)
        biome_areas[id] = {}
        # iterate over items in areas, where each "item" represents a biome in that landscape/country combination
        # read the biome info into a dictionary key'd by biomename
        for area in areas_list:
            biome_areas[id][area['biomename']] = area['kba_area'] + area['nonkba_area']
            biomes_list.append(area['biomename'])
    
    # Converting dictionary to df, borrowed from following though don't really understand how or why it works
    # https://stackoverflow.com/questions/24988131/nested-dictionary-to-multiindex-dataframe-where-dictionary-keys-are-column-label
    # creates a multi-indexed df
    df1 = pd.DataFrame.from_dict(biome_areas, orient="index").stack().to_frame()
    # reset df indexes to columns
    df2 = df1.reset_index()
    # rename columns
    df2.columns = ['id','biomename','biomearea']
    
    # Create a pivot table to summarize
    df3 = pd.pivot_table(df2, 
                        values = 'biomearea',
                        index = 'id',
                        columns = 'biomename',
                        aggfunc = np.sum)
    
    # Join back to the original df on 'id'
    df.set_index('id', inplace=True)
    df4 = pd.merge(df, df3, left_index = True, right_index = True)
    
    # Export df to csv
    output_file = (os.path.join(scl_dir, year, "analysis", output_filename))
    df4.to_csv(output_file)
    print ("Sent output to... ", output_file)

    output_filename2 = "scl_biome_areas_not_pivot.csv"
    output_file2 = (os.path.join(scl_dir, year, "analysis", output_filename2))
    df2.to_csv(output_file2)
    print ("Sent output to... ", output_file2)



    # make df from dictionary
    # https://stackoverflow.com/questions/13575090/construct-pandas-dataframe-from-items-in-nested-dictionary
    # not grokking how this works but it does...
    #user_dict = biome_areas
    #df1 = pd.DataFrame.from_dict({(i,j): user_dict[i][j] 
    #                       for i in user_dict.keys() 
    #                       for j in user_dict[i].keys()},
    #                       orient='index',
    #                       names=['id','biomename'])

    #df2 = df1.reset_index()
    #print (df2.head)
    #print (df2.iloc[0,:])
    #for col in df1.columns:
    #    print ("df1",col)
    #for col in df2.columns:
    #    print ("df2",col)
 #   print (df2.head)
 #   for col in df2.columns:
 #       print ("df2",col)
    #print (df3.index)
    #for col in df3.columns:
        #print ("df3",col)  
    #print (df.index)
    #for col in df4.columns:
        #print ("d4",col)
        
    # I tried making the dictionary into a new df and then join it back to the original df for output, but just can't grok it
    # see various failed attempts in the #old code section below
    # so just looping over dictionary to create output then will do join in Excel
    
    # Export biome_areas dictionary to csv
    #output_file = (os.path.join(scl_dir, year, "analysis", output_filename))
    #data = []
    #header = ['id','biomename','area']
    #with open(output_file, 'w', encoding = 'UTF8', newline='') as f:
    #    writer = csv.writer(f)
    #    writer.writerow(header)
    #    for id in biome_areas.keys():
    #        for biome in biome_areas[id].keys():
    #            #print (id, biome, biome_areas[id][biome])
    #            row = [id, biome, biome_areas[id][biome]]
    #            writer.writerow(row)
    #print ("Sent output to... ", output_file)





# Old code    
    #an_area = df.loc[[0],['areas']]
    #an_area = df._get_value(0,'areas')
    #print (type(an_area), an_area)
    #print ("id: ", df._get_value(0,'id'))
    #print ("lsid: ", df._get_value(0,'lsid'))
    #print ("Country: ", df._get_value(0,'lscountry'))
    #print ("Area: ", df._get_value(0,'lscountry_area'))
    
    
    # Flatten data
    # https://stackoverflow.com/questions/39899005/how-to-flatten-a-pandas-dataframe-with-some-columns-as-json
    # I don't really understand how / why this works but B seems closer to what we need
    #import ast
    #def only_dict(d):
    #    '''
    #    Convert json string representation of dictionary to a python dict
    #    '''
    #    return ast.literal_eval(d)

    #def list_of_dicts(ld):
    #    '''
    #    Create a mapping of the tuples formed after 
    #    converting json strings of list to a python list   
    #    '''
    #    return dict([(list(d.values())[1], list(d.values())[0]) for d in ast.literal_eval(ld)])

    #A = pd.json_normalize(df['areas'].apply(only_dict).tolist()).add_prefix('columnA.')
    #B = pd.json_normalize(df['areas'].apply(list_of_dicts).tolist()).add_prefix('columnB.pos.') 
    
    
    #json_struct = json.loads(df_areas.to_json(orient="records"))   
    #df_flat = pd.json_normalize(json_struct) 
    
   
    # Get column names from pandas df
    #print (df.head)
    #for col in df.columns:
    #    print (col)
    #for col in B.columns:
    #    print (col)
    #print (B.head)
    
        #df1 = pd.DataFrame.from_dict(biome_areas, orient = 'index', columns = ['id','biomename'])
    #print (df1.head)
    
    # make a new df from the filled dictionary

    #row = 0
    #for id in biome_areas.keys():
    #    df1.loc['row','id'] = id
    #    for biome in biome_areas[id].keys():
    #        df1['biome'] = biome_areas[id][biome]

    
    # merge two dataframes back together using 
    #df2 = pd.DataFrame()
    #df.join(df, on='id')
    
    # go back through the dictionary and write columns to df    

    #df['kba_area_sum'] = kba_areas_list
    #df['pa_area_sum'] = pa_areas_list
    #df['kbas_list'] = kbas_list
    #df['pas_list'] = pas_list

    # Get column names from pandas df
    #print (type(df['id'].iat[0]))
    #print (type(df1['id'].iat[0]))
    #print (df.head)
    #for col in df1.columns:
    #    print (col)
    
    
    # make df from dictionary
    # https://stackoverflow.com/questions/13575090/construct-pandas-dataframe-from-items-in-nested-dictionary
    # not grokking how this works but it does...
    # user_dict = biome_areas
    # df1 = pd.DataFrame.from_dict({(i,j): user_dict[i][j] 
    #                       for i in user_dict.keys() 
    #                       for j in user_dict[i].keys()},
    #                       orient='index')
    # df2 = df1.reset_index()
    # d2.columns = ['id-bioname']
    
    # Get areas
    #print (data_gdf._get_value(0,'areas'))
    #an_area = data_gdf._get_value(0,'areas')
    #an_area_list = json.loads(an_area)
    #an_area_dict = an_area_list[0]
    #print (an_area)
    #print (type(an_area), type(an_area_list), type(an_area_dict))
    #print (an_area_dict.keys())
    
    
    #print (an_area_dict)
    #print (flatten(an_area_dict))
    #areas_df = data_gdf[["areas"]].copy
    
