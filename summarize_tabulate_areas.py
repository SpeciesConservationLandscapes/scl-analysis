# summarize_tabulate_areas.py
# ews 7/30/2022

# objective:  run through the tabulate areas dbfs (see loop_over_tabulate_areas.py), apply a set of weights to define habitat, then summarize areas into a table

# for purposes of the tiger indigenous range, loop over the tabulate areas for each anthrome 12K year, apply anthrome based definition of tiger habitat,
# and sum up areas for each poly_id, then output to csv.  Note:  areas are in square meters.

# run in the "scl" environment at the conda prompt

# after you have run this, then run plot_tabulate_areas.py

# imports
import sys
import os
import zipfile
import csv
from dbfread import DBF
#from simpledbf import Dbf5
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import re


# note areas in the dbf files from ZonalHistogram are the number of cells
# with cellsize = 9637 * 9637 m = 92.87 km2
# as measured in Albers Equal Area map projection with following parameters:
#   central meridian = 125
#   standard parallel 1 = -9
#   standard parallel 2 = 53
#   latitude of origin = 15
#   datum = WGS84

# cellsize = 92.87

# set up

anthrome_areas = {}
years = []
poly_ids = []
tiger_habitat_areas = {}
# establish which anthromes are tiger habitat (=1) and not (=0) as below
# see: Ellis EC, Beusen AHW, Goldewijk KK. 2020. Anthropogenic Biomes: 10,000 BCE to 2015 CE. Land 9:129.
# see especially, Appendix A, Figure 2A
tiger_anthromes = {11: 0,  # Urban
                 12: 0,  # Mixed settlements
                 21: 0,  # Rice villages
                 22: 0,  # Irrigated villages
                 23: 0,  # Rainfed villages
                 24: 0,  # Pastoral villages
                 31: 0,  # Residential irrigated crops, "residential" = population density > 10 people/km2
                 32: 0,  # Residential rainfed crops
                 33: 1,  # Populated croplands, "populated" = population density < 10 people/km2, and abouve 1 person/km2
                 34: 1,  # Remote croplands, "remote" = population density < 1 people/km2
                 41: 0,  # Residential rangelands
                 42: 1,  # Populated rangelands
                 43: 1,  # Remote rangelands
                 51: 0,  # Residential woodlands
                 52: 1,  # Populated woodlands
                 53: 1,  # Remote woodlands
                 54: 0,  # Inhabited treeless & barren lands
                 61: 1,  # Wild woodlands
                 62: 0,  # Wild treeless & barren lands
                 63: 0,  # Wild ice
                 70: 0}  # Undefined


zonal_stats_dir = r'C:\proj\species\tigers\TCLs v3\historic range\anthrome analysis\tiger_zonal_stats'
anthromes_output = r'C:\proj\species\tigers\TCLs v3\historic range\anthrome analysis\tiger_habitat_stats'

# Loop over the projected anthrome dbf files (e.g. anthromes100ADprj.tif.vat.dbf)
for filename in os.listdir(zonal_stats_dir):
    if (filename.endswith(".dbf")):
        #filename = 'anthromes2000ADprj_area.dbf'
        print ("Working on ", filename)
        table = DBF(os.path.join(zonal_stats_dir, filename))
        year = re.findall(r'\d+', filename)
        year = int(year[0])
        #print (year, type(year))
        # if year is BC, make it negative
        if filename.find('BC') != -1:
            year = year * -1
        anthrome_areas[year] = {}
        tiger_habitat_areas[year] = {}
        # keep track of all the years
        years.append(year)

        # get anthrome values from the header
        anthrome_values = table.field_names
        anthromes_nums = []
        for anthrome in anthrome_values:
            if anthrome == 'POLY_ID': continue
            else:
                anthrome_num = int(re.findall(r'\d+', anthrome)[0])
            anthromes_nums.append(anthrome_num) 
        #print ("Anthrome_values: ", anthrome_values)
        #print ("Anthrome_nums: ", anthromes_nums)
        
        # loop over each record (poly_id) and calculate weighted sum, using weights above
        for record in table:
            poly_id = list(record.values())[0]
            poly_ids.append(poly_id)
            tiger_habitat_areas[year][poly_id] = 0
            col = 1
            for id in anthromes_nums:
                #print (year, poly_id, id, col, (list(record.values())[col]))
                tiger_habitat_areas[year][poly_id] = (list(record.values())[col] * tiger_anthromes[id]) + tiger_habitat_areas[year][poly_id]
                col = col+1
            #print (year, poly_id, tiger_habitat_areas[year][poly_id])
            
            
# output to csv 
csv_file = os.path.join(anthromes_output, "tiger_habitat_polys.csv")
unique_poly_ids = sorted(list(set(poly_ids)))
header = list(unique_poly_ids)
header.insert(0, 'Year')
#print (unique_poly_ids)
        
with open (csv_file, 'w', newline = '') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for year in sorted(years):
        row = []
        for id in unique_poly_ids:
            #print (year, id, tiger_habitat_areas[year][id])
            row.append(tiger_habitat_areas[year][id])
        row.insert(0, year)
        writer.writerow(row)
    


    
        