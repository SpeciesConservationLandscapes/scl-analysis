# scl_analyze_areas_biomes.py
# ews 7/15/2022

# Read object and summarize the nested JSON in the "areas" field of the SCL output format
# this script calculates the total area of biomes in each landscape/country combination, key'd by id
# I'm sure there's a better way to do this!


# imports
import os
import geojson
import geopandas as gpd
import pandas as pd
import numpy as np
import json

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
    # see "areas json structure EXPLAINED.txt" for explanation of the structure of "areas" json
    
    # set up an empty dictionary 
    biome_areas = {}
    
    # iterate over rows in df
    for id, areas_str in zip(df['id'], df['areas']):
        areas_list = json.loads(areas_str)
        biome_areas[id] = {}
        # iterate over items in areas, where each "item" represents a biome in that landscape/country combination
        # read the biome info into a dictionary key'd by biomename
        for area in areas_list:
            biome_areas[id][area['biomename']] = area['kba_area'] + area['nonkba_area']
    
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


