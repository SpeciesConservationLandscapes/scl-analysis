# Convert SCL geojson files to shapefiles
# ews 8/15/2022

# imports
import os
import geojson
import geopandas as gpd
import pandas as pd
import numpy as np
import csv

# Set up

# data files organized by folder by time point are in this directory:
scl_dir = r"C:\proj\species\tigers\TCLs v3\TCL delineation\scl_stats_07032022"
# the years to analyze are:
years = ['2020-01-01','2019-01-01','2018-01-01','2017-01-01','2016-01-01','2015-01-01','2014-01-01','2013-01-01','2012-01-01','2011-01-01','2010-01-01','2009-01-01','2008-01-01','2007-01-01','2006-01-01','2005-01-01','2004-01-01','2003-01-01','2002-01-01','2001-01-01']
# a single year for testing purposes
#years = ['2001-01-01']

problem_list = []

# convert all to shapefile
for year in years:
    shp_dir = os.path.join(scl_dir, year, "shp")
    if not os.path.exists(shp_dir):
        os.makedirs(shp_dir)
    #print (shp_dir)
    for filename in os.listdir(os.path.join(scl_dir, year)):
        filename_tuple = os.path.splitext(filename)
        if filename_tuple[1] == '.geojson':
            shapefile = filename_tuple[0] + "_" + year + ".shp"
            # Get the type, dropping first four characters (i.e. "scl_restoration" becomes "restoration")
            type = filename_tuple[0][4:]
            print ("Converting", filename, "to", shapefile)
            try:
                gdf = gpd.read_file(os.path.join(scl_dir, year, filename))
                # while going through, add fields identifying species, date and landscape type
                gdf['Species'] = 'Panthera tigris'
                gdf['Date'] = year
                gdf['Type'] = type
                gdf.to_file(os.path.join(scl_dir, year, "shp", shapefile))
            except:
                problem = os.path.join(scl_dir, year, "shp", shapefile)
                problem_list.append(problem)
                print ("Problem with ", os.path.join(scl_dir, year, "shp", shapefile))
                

# write out problems to csv
print ("Save out problem cases")
with open(os.path.join(scl_dir, 'problems_during_conversion_to_shp.txt'), 'w') as f: 
    for prob in problem_list:
        print (prob)
        f.write("%s\n" % prob)