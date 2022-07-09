# Processing SCL geojson files using pivot
# ews 7/8/2022

# imports
import os
import geojson
import geopandas as gpd
import pandas as pd
import numpy as np

# Set up

# data files organized by folder by time point are in this directory:
scl_dir = r"C:\proj\species\tigers\TCLs v3\TCL delineation\scl_stats_07032022"
# the years to analyze are:
#years = ['2020-01-01','2019-01-01','2018-01-01','2017-01-01','2016-01-01','2015-01-01','2014-01-01','2013-01-01','2012-01-01','2011-01-01','2010-01-01','2009-01-01','2008-01-01','2007-01-01','2006-01-01','2005-01-01','2004-01-01','2003-01-01','2002-01-01','2001-01-01']
# a single year for testing purposes
years = ['2020-01-01']
# the type of datafile to analyze is
data_filename = "scl_states.geojson"
data_name_tuple = os.path.splitext(data_filename)
# the output file will go in this directory
scl_analysis_dir = r"C:\proj\species\tigers\TCLs v3\TCL delineation\scl_stats_07032022\analysis\pivot_tables\states"

# specify areas fields to summarize in pivot table (these will be columns)
summary_areas_list = ['indigenous_range_area','str_hab_area','eff_pot_hab_area','occupied_eff_pot_hab_area']
# specify over what field to summarize data 
summary_index_list = ['countrynam']

# Loop over years to generate a pivot table for each data_filename
# set up dictionary to hold the pivot table df
frames = {}
for year in years:

    # Get filename for this year
    data_file = (os.path.join(scl_dir, year, data_filename))
    print ("Working on...", data_file)
    
    # Load file into Geopandas data frame
    data_gdf = gpd.read_file(data_file)
    
    # Uncomment this to get column heads (i.e. fieldnames)
    #for col in states_gdf.columns:
    #    print (col)
    
    # Create a pivot table to add up various habitat area by countrynam
    pivot_df = pd.pivot_table(data_gdf, 
                        values = summary_areas_list,
                        index = summary_index_list,
                        aggfunc = np.sum)
    
    # Uncomment this if you want to see pivot table on standard output
    #print (pivot_df)
    
    # for graphing purposes
    # save each year's dataframes into a dictionary of dataframes, keyed by year
    frames[year] = pivot_df
                        
    # Generate output file name with year                       
    output_filename = data_name_tuple[0] + "." + year + ".csv"
    output_file = (os.path.join(scl_analysis_dir, output_filename))
    
    # Write pivot_df to csv, note: columns argument dictates order of columns in output
    #pivot_df.to_csv(output_file, columns = summary_areas_list)


# Do something with the dictionary of pivot df
# get first five rows
for year in years:
    print (year)
    print (frames[year].head)




# old code

# this works to load the geojson file using geojson module:  https://pypi.org/project/geojson/
# note UTF encoding

#with open(states_file, encoding = 'utf-8') as f:
#    states_gj = geojson.load(f)
#for feature in states_gj["features"]:
#    selected_feature = 3
    #print (feature["properties"])
    #print (feature["properties"]["countrynam"],feature["properties"]['gadm1name'],feature["properties"]['indigenous_range_area'])

# get first five rows
#print (states_gdf.head)



# set index to gad1name (the names of the states/provinces)
#states_gdf = states_gdf.set_index("gadm1name")
#print (states_gdf.indigenous_range_area)


#print("Hello world!")