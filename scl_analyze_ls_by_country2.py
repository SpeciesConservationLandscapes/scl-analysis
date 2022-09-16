# scl_analyze_ls_by_country2.py
# ews 9/15/2022
#
# Based on scl_analyze_ls_by_country.py by ews 8/16/2022

# Read attributes of geojson files for each landscape type for each year
# Create pivot table of attributes, summarizing by country (e.g. country)
# Calulate two forms of pivot table, one summarizing areas of each landscape type;
# the other the count of each landscape type, acknowledging that some landscapes are transboundary
# Dump out the results to be assembled into formatted tables and plotted

# assumes the data have been downloaded locally into scl_dir from Google Cloud Storage (see scl_download_google_cloud.py)
# data are organized into folders  by time point
# within each folder are seven geojson files; see scl_data_defnitions.txt for the field names and meanings

# Note there are six landscape types:  restoration, restoration_fragment, survey, survey_fragment, species, species_fragment
# "species" are tiger conservation landscapes, in the case of tigers

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
# subdirectory for pivot tables
pivot_subdir = "pivot_tables\landscape_areas"

# the years to analyze are:
years = ['2020-01-01','2019-01-01','2018-01-01','2017-01-01','2016-01-01','2015-01-01','2014-01-01','2013-01-01','2012-01-01','2011-01-01','2010-01-01','2009-01-01','2008-01-01','2007-01-01','2006-01-01','2005-01-01','2004-01-01','2003-01-01','2002-01-01','2001-01-01']
# a single year for testing purposes
#years = ['2014-01-01']
# landscape types to analyze are:
types = ['scl_restoration','scl_restoration_fragment','scl_species','scl_species_fragment','scl_survey','scl_survey_fragment']
# a single landscape type for testing purposes
#types = ['scl_survey_fragment']

# loop over years and calculate pivot tables 
for year in years:
    
    # create empty dictionary to hold df
    df_dict = {}
    
    # load gejson files into df
    for type in types:
        lsfile = type + ".geojson"
        print ("Working on", year, lsfile)
        # load geojson into pandas dataframe
        df = gpd.read_file(os.path.join(scl_dir, year, lsfile))
        df['type'] = type
        df_dict[type] = df
        
        #for col in df_type.columns:
        #    print (col)
    
    # concatenate the df iterating over the different landscape types
    df = pd.DataFrame()
    for type in types:
        df = pd.concat([df, df_dict[type]])
    
    #for col in df.columns:
    #    print (col)
    #print(df.head)
    
    # create pivot table using pandas summing areas by landscape type and country
    pivot_areas_df = pd.pivot_table(df, 
        values = ['eff_pot_hab_area'],       
        index = ['country'],
        columns = ['type'],
        aggfunc = 'sum')
    #pivot_areas_df.rename(columns={'eff_pot_hab_area': 'area'}, level=0, inplace=True)
    #print (pivot_areas_df)
    
    # create pivot table using pandas counting areas by landscape type and country
    pivot_count_df = pd.pivot_table(df, 
        values = ['eff_pot_hab_area'],       
        index = ['country'],
        columns = ['type'],
        aggfunc = 'count') 
    pivot_count_df.rename(columns={'eff_pot_hab_area': 'count'}, level=0, inplace=True)        
    #print (pivot_count_df)
 
    #concatenate the two dataframes horizonatally
    pivot_ls_df = pd.concat([pivot_areas_df, pivot_count_df], axis=1)
   
    # save out to csv
    csvfilename = "ls_pivot." + year + ".csv"
    pivot_ls_df.to_csv(os.path.join(scl_dir, pivot_subdir, csvfilename))

       
print ("That's all folks!")