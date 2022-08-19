# tiger_anthrome12k_analysis.py
# ews 11/15/2021

# strategy:
# goal:
#   calculate how tiger habitat has changed over the last 6500 years in each ecoregion
#
# inputs:
#   anthrom12k data set from Ellis et al.
#   indigenous range file subdivided by ecoregions / portions of ecoregions
# loop over directory of anthrome12k time points
#   unzip the time point
#   convert asc file to tiff
#   clip area of tiger indigenous range - resident - likely
#   reclass to tiger habitat
#   project to 2d projection
#   calculate zonal histogram to get number cells tiger habitat / not tiger habitat for tha time point for each ecoregion in indigenous range
#   store estimate of tiger habitat area for each ecoregion for each time point
#   write out values to csv for further analysis
#   clean up ... delete clip, tiger habitat reclass, and projected reclass grids (leave tiff)


# say hello
print ('Hello world!')

# imports
import sys
import os
import zipfile
import csv
from dbfread import DBF
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import re
#import arcpy
#from arcpy.sa import *


"""

# set-up
anthrome_dir = r'C:\proj\landscapes\Anthromes 12K\anthromes'
anthromes_prj_dir = r'C:\proj\landscapes\Anthromes 12K\anthromes_tiger_projected'
anthromes_output = r'C:\\Users\esanderson\Documents\anthromes_tigers'
zone_path = r'C:\proj\species\tigers\TCLs v3\historic range\historic range for TCL 3'
zone_file = 'TCL3_indigenous_range_06222022_ids_prj.shp'
#WGS84_d#Custom_prj_dataset = r'C:\proj\species\tigers\TCLs v3\historic range\historic range for TCL 3\tiger_historic_range_12-04-2021_prj.shp'



# Unzipping anthrome data
for filename in os.listdir(anthrome_dir):
    if (filename.endswith(".zip")):
       print('Unzipping: ', filename)
       with zipfile.ZipFile(os.path.join(anthrome_dir, filename), 'r') as zip_ref:
            zip_ref.extractall(os.path.join(anthrome_dir))
    else:
        print('Trouble unzipping: ', filename)
        continue


# Converting to tiff
for filename in os.listdir(anthrome_dir):
    if (filename.endswith(".asc")):
        print('Converting to tiff: ', filename)
        rasterType = 'INTEGER'
        outRaster = os.path.splitext(os.path.join(anthrome_dir, filename))[0] + '.tif'
        arcpy.ASCIIToRaster_conversion(os.path.join(anthrome_dir, filename), outRaster, rasterType)


# Project to WGS84
for filename in os.listdir(anthrome_dir):
    if (filename.endswith(".tif")):
        print('Defining projection: ', filename)
        coord_sys = arcpy.Describe(WGS84_dataset).spatialReference
        arcpy.DefineProjection_management(os.path.join(anthrome_dir, filename), coord_sys)


# Project to Custom tiger project 
for filename in os.listdir(anthrome_dir):
    if (filename.endswith(".tif")):
        print('Reprojecting: ', filename)
        outRaster = os.path.splitext(os.path.join(anthrome_dir, filename))[0] + 'prj.tif'
        coord_sys = arcpy.Describe(Custom_prj_dataset).spatialReference
        arcpy.ProjectRaster_management(os.path.join(anthrome_dir, filename), os.path.join(anthrome_prj_dir, outRaster), coord_sys)
        #print os.path.join(anthrome_prj_dir, outRaster)


"""

# just a comment, only a comment

"""


# Run zonal histograms
output_dir = r'C:\proj\species\tigers\TCLs v3\historic range\anthrome analysis\tiger_zonal_stats'
zone_path = r'C:\proj\species\tigers\TCLs v3\historic range\historic range for TCL 3'
zone_file = 'TCL3_indigenous_range_06222022_ids_prj.shp'
zoneField = 'Poly_id'        # note:  zone field needs to be an integer for zonal stats
valueField = 'Value'
anthromes_prj_dir = r'C:\proj\landscapes\Anthromes 12K\anthromes_tiger_projected'


# Note:  I was having a lot of trouble setting up the environment so in the end ran the Arcpy dependent parts in the python window of ArcMap 10.7.1


for filename in os.listdir(anthromes_prj_dir):
    if (filename.endswith("prj.tif")):
        print 'Tabulate Areas analysis: ', filename
        # zones = tiger ecoregions
        inZoneData = os.path.join(zone_path, zone_file)
        # projected anthromes
        inValueRaster = os.path.join(anthromes_prj_dir, filename)
        # output
        outTable = os.path.splitext(os.path.join(output_dir, filename))[0] + '_area.dbf'
        #print outTable
        arcpy.CheckOutExtension("Spatial")
        # note zonalHistograms failed after 254 zones
        # arcpy.sa.ZonalHistogram(inZoneData, zoneField, inValueRaster, outTable)
        # try instead, TablulateAreas:  https://gis.stackexchange.com/questions/172748/too-many-zones-for-zonal-histogram
        TabulateArea(inZoneData, zoneField, inValueRaster, valueField, outTable)

"""


# note areas in the dbf files from ZonalHistogram are the number of cells
# with cellsize = 9637 * 9637 m = 92.87 km2
# as measured in Albers Equal Area map projection with following parameters:
#   central meridian = 125
#   standard parallel 1 = -9
#   standard parallel 2 = 53
#   latitude of origin = 15
#   datum = WGS84



cellsize = 92.87

# set up

anthrome_areas = {}
years = []
tiger_habitat_areas = {}
# establish which anthromes are tiger habitat (=1) and not (=0) as below
tiger_anthromes = {11: 0,  # Urban
                 12: 0,  # Mixed settlements
                 21: 0,  # Rice villages
                 22: 0,  # Irrigated villages
                 23: 0,  # Rainfed villages
                 24: 0,  # Pastoral villages
                 31: 0,  # Residential irrigated crops
                 32: 0,  # Residential rainfed crops
                 33: 1,  # Populated croplands
                 34: 1,  # Remote croplands
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
anthrome_areas = {}
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

        # get labels
        eco_labels = table.field_names
        #print ("Eco_labels: ", eco_labels)
        #print (type(eco_labels))



        # load values from dbf into a nested dictionary, key'ed by year and anthrome_id
        for record in table:
            # when using zonal histograms
            #anthrome_id = int(list(record.values())[0].encode())    # record.values are unicode, so convert to string, then integer
            # when using tabulate areas
            poly_id = list(record.values())[0]   # record.values are unicode, so convert to string
            # when using zonal histogram
            #anthrome_areas[year][anthrome_id] = dict(zip(table.field_names, list(record.values())))
            # when using tabulate areas
            anthrome_areas[year][poly_id] = dict(zip(table.field_names, list(record.values())))

        # initialize dictionary to hold tiger_habitat_areas by year and ecoregion
        tiger_ecoregions = []
        # when using zonal histogram
        #for id in anthrome_areas[year].keys():
        # when using tabulate areas
        for id in anthrome_areas[year].values():
            for eco in eco_labels:
                tiger_habitat_areas[year][eco] = 0
                

        # loop over those anthrome_ids, and then each ecoregion, to calculate tiger habitat areas
        # also get a list of the eco labels
        # when using zonal histogram
        #for id in anthrome_areas[year].keys():
        for id_label in anthrome_areas[year].keys():
            print (id_label, type(id_label))
            for eco in eco_labels:
                # print eco, id, anthrome_areas[year][id][eco], tiger_anthromes[id]
                # when using zonal histogram
                #if eco == 'LABEL':
                # when using Tabulate Areas
                if eco == 'POLY_ID':
                    continue
                else:
                    id = re.findall(r'\d+', id_label)
                    tiger_habitat_areas[year][eco] = (anthrome_areas[year][id_label][eco] * tiger_anthromes[id]) + tiger_habitat_areas[year][eco]
        #print filename, year
        #print tiger_habitat_areas.keys()


        file_headers = []
        passes = 0

        # output to csv after creating header and set of rows
        csv_file = os.path.join(anthromes_output, "tiger_habitat_ecoregions.csv")
        file_headers = eco_labels
        if passes == 0:
            with open(csv_file, 'a', newline ='') as myfile:
                wr = csv.writer(myfile)
                file_headers.insert(0, 'Year')
                wr.writerow(file_headers)
            passes = passes + 1
        else:
            continue

        with open(csv_file, 'a', newline ='') as myfile:
            wr = csv.writer(myfile)
            data = []
            #print eco_labels
            for eco in eco_labels:
                #print eco_labels
                if eco == 'LABEL' or eco == 'Year':
                    continue
                else:
                    data.append(tiger_habitat_areas[year][eco])
            data.insert(0, year)
            wr.writerow(data)





# read back the csv and plot using pandas
# note:  I used Excel to get rid of the unnecessary headers in tiger_habitat_ecoregions.csv
"""

import sys
import os
import csv
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

anthromes_output = r'C:\proj\species\tigers\TCLs v3\historic range\anthrome analysis\tiger_habitat_stats'
anthromes_plots = r'C:\proj\species\tigers\TCLs v3\historic range\anthrome analysis\tiger_plots'


### Check what happened to Poly_1157 which doesn't seem to be listd in "tiger_habitat_ecoregions2.csv"
### see C:\proj\species\tigers\TCLs v3\historic range\anthrome analysis\tiger_zonal_stats, where only first 420 polys calculated
# "tigers_habitat_ecoregions2.csv" is the result of the steps above calculating amount of tiger habitat (defined in terms of anthromes) at each year

csv_file = os.path.join(anthromes_output, "tiger_habitat_ecoregions2.csv")
df = pd.read_csv(csv_file)
df.set_index('Year', inplace=True, drop=True)
print (df.head())

# read in list of names for each poly -- not that some are different portions of same ecoregion/divide... to be combined
csv_file2 = os.path.join(anthromes_output, "eco_divide_names.csv")
df_names = pd.read_csv(csv_file2)
df_names.fillna('-', inplace=True)
df_names.set_index('Poly_id')
#print (df_names.head())

# note that multiple polys have the same ecoregion and divide; these need to be grouped before plotting
df_groups = df_names.groupby(['ECO_NAME_1','Divide_1'])['Poly_id'].apply(list).reset_index(name='polys')
print (df_groups.head())
#print (df_groups.iloc[0]['polys'], type(df_groups.iloc[0]['polys']))

#for col in df_groups.iloc[0]['polys']:
#    print ("Poly__" + str(col))


# cycle over rows plotting each with name and category
for poly_id, row in df_groups.iterrows():

    df['total'] = 0

    # sum the areas in df by groups defined by list in df_groups['polys']
    print (poly_id, row['polys'])
    polys_to_sum = []
    for p in row['polys']:
        polys_to_sum.append("Poly__" + str(p))
    df['total'] = df.apply(lambda x: sum(x[c] for c in x[polys_to_sum]), axis=1)
    print (df['total'].head())
 

    # get eco name and divide
    econame = df_names.iloc[poly_id]['ECO_NAME_1']
    divide = df_names.iloc[poly_id]['Divide_1']
    category = df_names.iloc[poly_id]['Category_2']
    eco_divide = econame + "{" + divide + ")\n"

    # plot figure
    print ("Plotting: ", poly_id, eco_divide)    
    plt.figure()
    plt.plot(df[i])  # if x axis isn't specified, pandas uses index
    plt.title(eco_divide + category)
    filename = i + '.jpg';
    plot_file = os.path.join(anthromes_plots, filename)
    #plt.savefig(plot_file)
    plt.close()
"""




















# OLD code

#print (df_names.head())
#df_names_t = df_names.set_index('Poly_id').T
#print (df_names_t.head())


#for idx, val in enumerate(df.columns):
#    ymax_value = df[df.columns[idx]].max();
    #type(val)
    #eco_code = list(names_dict.keys())[idx];
    #econame = names_dict[eco_code][1];
    #divide = names_dict[eco_code][2];
    #name = econame + "(" + str(divide) + ")"
    #print (econame, divide)
    #print ("Plotting ", name)
#    ax = df.plot(y=df.columns[idx],xlim=(-6500,2020), ylim = (0,ymax_value*1.1), style='-+', title='val');
#    ax.set_xlabel("Year");
#    ax.set_ylabel("Area");
#    filename = val + '.jpg';
#    plot_file = os.path.join(anthromes_plots, filename)
    #ax.figure.savefig(filename);


#fig = plt.figure(1)
#fig.add_subplot(1,1)
#df.plot(y='ECO_I_222', use_index=True)
#plt.subplot(212)
#plt.plot(y='ECO_I_223',use_index=True)


#for eco in df.columns:
#    plt.plot(y=eco, use_index=True)
#    plt.show()

