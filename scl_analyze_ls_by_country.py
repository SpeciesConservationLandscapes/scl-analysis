# scl_analyze_ls_by_country.py
# ews 8/16/2022

# Read attributes of merged landscape files for each year (e.g. scl_ALL_2001_01_01.shp)
# Create pivot table of attributes, summarizing by country (e.g. lscountry)
# Calulate two forms of pivot table, one summarizing areas of each landscape type;
# the other the count of each landscape type, acknowledging that some landscapes are transboundary
# Dump out the results to be assembled into formatted tables and plotted

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
scl_dir = r"C:\proj\species\tigers\TCLs v3\TCL delineation\scl_stats_07032022"
# the years to analyze are:
years = ['2020-01-01','2019-01-01','2018-01-01','2017-01-01','2016-01-01','2015-01-01','2014-01-01','2013-01-01','2012-01-01','2011-01-01','2010-01-01','2009-01-01','2008-01-01','2007-01-01','2006-01-01','2005-01-01','2004-01-01','2003-01-01','2002-01-01','2001-01-01']
# a single year for testing purposes
#years = ['2020-01-01']

# create dictionary to hold dataframes
ls_dict = {}


# loop over years and calculate pivot tables
for year in years:
    print ("Working on", year)
    # note replacement in the second "year" to maintain compatibility with filename convention
    all_filename = os.path.join(scl_dir, year, "shp", "scl_ALL_" + year.replace("-","_") + ".dbf")
    print (all_filename)
    # load dbf file
    table = DBF(all_filename, encoding='utf-8')
    # convert to pandas dataframe
    df = pd.DataFrame(iter(table))
    

    
    # create pivot table using pandas summing areas by landscape type and country
    pivot_areas_df = pd.pivot_table(df, 
                    values = ['lscountry_'],       # this field holds the area of the landscape in the country, as measured by effective potential habitat in km2
                    index = ['lscountry'],
                    columns = ['Type'],
                    aggfunc = 'sum')
    pivot_areas_df.rename(columns={'lscountry_': 'area'}, level=0, inplace=True)
    #print (pivot_areas_df)
    
    #for col in pivot_areas_df.columns:
    #    print (col)

    # create pivot table using pandas counting areas by landscape type and country
    pivot_count_df = pd.pivot_table(df, 
                    values = ['lscountry_'],       
                    index = ['lscountry'],
                    columns = ['Type'],
                    aggfunc = 'count')              # this field calculates the count of the landscapes in the country, recognizing that some landscapes cross national boundaires
    pivot_count_df.rename(columns={'lscountry_': 'count'}, level=0, inplace=True)
    #print (pivot_count_df)
 
    #for col in pivot_count_df.columns:
    #    print (col)
        
    #concatenate the two dataframes horizonatally
    pivot_ls_df = pd.concat([pivot_areas_df, pivot_count_df], axis=1)
    
    #for col in pivot_ls_df.columns:
    #    print (col)
        
    #write df to dictionary, keyed by year
    ls_dict[year] = pivot_ls_df
 
    # save out to csv
    #area_count_csv = os.path.join(scl_dir, year, "shp", "scl_ALL_areas_counts_" + year.replace("-","_") + ".csv")
    area_count_csv = os.path.join(r"C:\proj\species\tigers\TCLs v3\TCL delineation\scl_stats_07032022\analysis - all 20 years\pivot_tables\landscapes", "scl_ALL_areas_counts_" + year.replace("-","_") + ".csv")
    pivot_ls_df.to_csv(area_count_csv)






print ("That's all folks!")