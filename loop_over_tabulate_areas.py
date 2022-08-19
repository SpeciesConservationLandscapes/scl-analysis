# loop_over_zonal_stats.py
# ews 7/30/2022
#
# Goal:  loop over a set of polygons and run tabulate areas against a raster file 
#
# Tiger anthrome analysis:
# In this case the polygons are ecoregions (or parts of ecoregions) that are part of the indigenous range of the tiger as defined in polygon source data
# polygon source data:  C:\proj\species\tigers\TCLs v3\historic range\ecoregion analysis\tiger_indigenous_range_GS_07302022.shp
# --select only not "not tiger range" polygons, see C:\proj\species\tigers\TCLs v3\historic range\historic range for TCL 3\TCL3_indigenous_range_07302022.shp
# --add id (just copy FID into "Poly_id", then project using custom projection in C:\proj\species\tigers\TCLs v3\historic range\historic range for TCL 3\Custom Tiger Asia Albers Equal Area.prj
# -- see inputs below

# After this has been run, then see summarize_tabulate_areas.py to summarize the results of the dbfs produced by this script

# Note:  I was having a lot of trouble setting up the environment to use Python 2.7 with ArcMaps arcpy installation 
# so in the end ran the arcpy dependent parts in the python window of in blank mxd using ArcMap 10.7.1 by copying code below into Python window

# imports
import sys
import os
import arcpy
from arcpy.sa import *

# Run zonal histograms
output_dir = r'C:\proj\species\tigers\TCLs v3\historic range\anthrome analysis\tiger_zonal_stats'
zone_path = r'C:\proj\species\tigers\TCLs v3\historic range\historic range for TCL 3'
zone_file = 'TCL3_indigenous_range_07302022_ids_prj.shp'
zoneField = 'Poly_id'        # note:  zone field needs to be an integer for zonal stats
valueField = 'Value'
anthromes_prj_dir = r'C:\proj\landscapes\Anthromes 12K\anthromes_tiger_projected'

# loop over list of anthromes files (one per anthrome 12K year) and run zonal stats or tabulate areas
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
