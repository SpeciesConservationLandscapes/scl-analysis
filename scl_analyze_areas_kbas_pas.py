# scl_analysis.5.py
# ews 7/14/2022

# Read object and summarize the nested JSON in the "areas" field of the SCL output format
# this script calculates the total area of KBAs and Protected areas in each landscape


# imports
import os
import geojson
import geopandas as gpd
import pandas as pd
import numpy as np
import json
from flatten_json import flatten
from pandas.io.json import json_normalize

# some set up

# the input data files organized by folder by time point are in this directory:
scl_dir = r"C:\proj\species\tigers\TCLs v3\TCL delineation\scl_stats_07032022"
# the type of datafile to analyze is
data_filename = "scl_species.geojson"
data_name_tuple = os.path.splitext(data_filename)
# the output file will go in this directory
#scl_analysis_dir = r"C:\proj\species\tigers\TCLs v3\TCL delineation\scl_stats_07032022\analysis"
# output file names
output_filename = "scl_kba_pa_areas.csv"

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
    
    kba_areas_list = []
    pa_areas_list = []
    kbas_list = []  # note plural
    pas_list = []   # note plural
    # iterate over rows in df
    for lsid, areas_str in zip(df['lsid'], df['areas']):
        areas_list = json.loads(areas_str)
        kba_areas_sum = 0
        pa_areas_sum = 0
        kba_list = []   # note singular
        pa_list = []    # note singular
        # iterate over items in areas, where each "item" represents a biome in that landscape/country combination
        for area in areas_list:
            kba_areas_sum = kba_areas_sum + area['kba_area']
            pa_areas_sum = pa_areas_sum + area['protected']
            # iterate over the list of kbas within the biome, appending name(s) if they exist
            for kba in area['kbas']:
                if kba:
                    kba_list.append(kba['kbaname'])
            # iterate over the list of pas within the biome, appending name(s)
            for pa in area['pas']:
                if pa:
                    pa_list.append(pa['paname'])        
            #print (lsid, area['biomename'], area['kba_area']+area['nonkba_area'])
            #for kba in area['kbas']:
            #    print (kba['kbaname'], kba['kbaarea'])
        kba_areas_list.append(kba_areas_sum)
        pa_areas_list.append(pa_areas_sum)
        
        # for kba_list find unique elements then sort them
        #print (lsid, kba_list)
        kba_list = set(kba_list)
        sorted_kba_list = sorted(kba_list)
        kbas_list.append(sorted_kba_list)
        
        # same for pa_list
        pa_list = set(pa_list)
        sorted_pa_list = sorted(pa_list)
        pas_list.append(sorted_pa_list)
        

    df['kba_area_sum'] = kba_areas_list
    df['pa_area_sum'] = pa_areas_list
    df['kbas_list'] = kbas_list
    df['pas_list'] = pas_list

    # Get column names from pandas df
    #print (df.head)
    #for col in df.columns:
    #    print (col)

    # Export df to csv
    output_file = (os.path.join(scl_dir, year, "analysis", output_filename))
    df.to_csv(output_file)
    print ("Sent output to... ", output_file)









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
    
