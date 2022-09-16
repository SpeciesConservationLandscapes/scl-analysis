# scl_analyze_hab_by_country2.py
# ews 9/15/2022
#
# Based on scl_analyze_ls_by_country2.py 

# Read attributes of ls_stats scl_states.geojson files for each habitat type for each year
# Create pivot table of attributes, summarizing by country (e.g. country)
# Save out the results to csv to be assembled into formatted tables and plotted

# assumes the data have been downloaded locally into scl_dir from Google Cloud Storage (see scl_download_google_cloud.py)
# data are organized into folders  by time point
# within each folder are seven geojson files; see scl_data_defnitions.txt for the field names and meanings

# Note there are four habitat types to show:  indigenous range, structural habitat, effective potential habitat, known occupied habitat

# areas of these calculated by GEE in km2 are in the scl_states.geojson file for each year

# imports
import os
import geojson
import geopandas as gpd
import pandas as pd
import numpy as np
from dbfread import DBF

# Set up

# data files organized by folder by time point are in this directory:
scl_dir = r"C:\proj\species\tigers\TCLs v3\TCL delineation\scl_stats_09142022"
# subdirectory for pivot tables outputs
pivot_subdir = "pivot_tables\habitat_areas"
# data file
datafile = "scl_states.geojson"

# the years to analyze are:
years = ['2020-01-01','2019-01-01','2018-01-01','2017-01-01','2016-01-01','2015-01-01','2014-01-01','2013-01-01','2012-01-01','2011-01-01','2010-01-01','2009-01-01','2008-01-01','2007-01-01','2006-01-01','2005-01-01','2004-01-01','2003-01-01','2002-01-01','2001-01-01']
# a single year for testing purposes
#years = ['2020-01-01']
# habitat types to analyze are:
types = ['indigenous_range_area','str_hab_area','eff_pot_hab_area','occupied_eff_pot_hab_area']
# a single habitat type for testing purposes
#types = ['indigenous_range_area']

# loop over years and calculate pivot tables 
for year in years:
    
    # create empty dictionary to hold df
    df_dict = {}
    
    # load gejson files into df
    df = gpd.read_file(os.path.join(scl_dir, year, datafile))
    
    #for col in df.columns:
    #   print (col)
    #print(df.head)
    
    # for each habitat type, create pivot table using pandas summing areas by country
    for type in types:
        print ("Working on", year, type)
        pivot_areas_df = pd.pivot_table(df, 
            values = [type],       
            index = ['countrynam'],
            aggfunc = 'sum')
        df_dict[type] = pivot_areas_df
    
    # concatenate the df iterating over the different landscape types
    hab_df = pd.DataFrame()
    for type in types:
        hab_df = pd.concat([hab_df, df_dict[type]], axis=1)
    
    #for col in df2.columns:
    #    print (col)
    #print(df2.head)
    
    # create pivot table using pandas counting areas by landscape type and country
    #pivot_count_df = pd.pivot_table(df, 
    #    values = ['eff_pot_hab_area'],       
    #    index = ['country'],
    #    columns = ['type'],
    #    aggfunc = 'count') 
    #pivot_count_df.rename(columns={'eff_pot_hab_area': 'count'}, level=0, inplace=True)        
    #print (pivot_count_df)
 
    #concatenate the two dataframes horizonatally
    #pivot_ls_df = pd.concat([pivot_areas_df, pivot_count_df], axis=1)
   
    # save out to csv
    csvfilename = "hab_pivot." + year + ".csv"
    print("Saving to ", csvfilename)
    hab_df.to_csv(os.path.join(scl_dir, pivot_subdir, csvfilename))

       
print ("That's all folks!")