# scl_analysis.4.py
# scl_pivot_table_plots.py
# ews 7/9/2022

# Objective:  read in pivot tables generated by scl_pivot_table_analysis.py and create a plot of how areas change over time

# pivot table output comes from scl_pivot_table_analysis.py
# pivot table names in csv format have date embedded in filename (e.g.) scl_states_2020-01-01.csv
# pivot tables have a header row with fieldnames, expected in this order: geography, indigenous_range_area, str_hab_area, eff_pot_hab_area, occupied_eff_pot_hab_area)

# I'm sure there is a **much** better way to do this but I can't puzzle it out so apologies in advance for brute force approach
# trying to build dictionary like this
# dict['Afghanistan']['time']['indigenous_range_area'] = 10
# then make lineplots using matplotlib

# some imports
import os
import pandas as pd
import matplotlib.pyplot as plt
import csv

# some set up
#pivot_dir = r"C:\proj\species\tigers\TCLs v3\TCL delineation\scl_stats_07032022\analysis\pivot_tables\states"
#initial_pivot_filename = "scl_states.2020-01-01.csv"
#figure_dir = r'C:\proj\species\tigers\TCLs v3\TCL delineation\scl_stats_07032022\analysis\pivot_tables\states_plots'

# alternative set up
pivot_dir = r"C:\proj\species\tigers\TCLs v3\TCL delineation\scl_stats_07032022\analysis - all 20 years\pivot_tables\landscapes"
initial_pivot_filename = "scl_ALL_areas_counts.2020_01_01.csv"
figure_dir = r"C:\proj\species\tigers\TCLs v3\TCL delineation\scl_stats_07032022\analysis - all 20 years\pivot_tables\landscapes"

# loop through all the filenames to get the list of times
times_list = []
for filename in os.listdir(pivot_dir):
    filename_parts_list = filename.split(".")
    pivot_type = filename_parts_list[0]
    time = filename_parts_list[1]
    times_list.append(time) 

# import one csv file to initialize of geographies and fields
# this assumes all pivot tables have same list of geographies (rows) and same areas (fields)
geo_names_list = []
fields_list = []
initial_file = os.path.join(pivot_dir, initial_pivot_filename)
with open(initial_file, 'r') as csv_file:    
    csv_reader = csv.reader(csv_file, delimiter = ',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            data_type = row[1]
            print (data_type)
        if line_count == 1:
            #get field names into a list then start building pivot_dict to hold data
            print(f'Field names are {", ".join(row)}')
            fields_list = row
            line_count += 1
        elif line_count > 1:
            geo_name = row[0]
            geo_names_list.append(geo_name)
            #print(f'{", ".join(row)}')

# drop field name for geography
fields_list.pop(0)

# initialize pivot dictionary based on those lists
pivot_dict = {}         
for name in geo_names_list:
    pivot_dict[name] = {}
    for time in times_list:
        pivot_dict[name][time] = {};
        for field in fields_list:
            pivot_dict[name][time][field] = 0
            
# go back through all the pivot csv files and upload data in the appropriate places in the dictonary
for filename in os.listdir(pivot_dir):
    thisfile = os.path.join(pivot_dir, filename)
    with open(thisfile, 'r') as csv_file:
        # get time from filename and append to list
        filename_parts_list = thisfile.split(".")
        time = filename_parts_list[1]    
        csv_reader = csv.reader(csv_file, delimiter = ',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                geo = row[0]
                pivot_dict[geo][time][fields_list[0]] = int(float(row[1]))
                pivot_dict[geo][time][fields_list[1]] = int(float(row[2]))
                pivot_dict[geo][time][fields_list[2]] = int(float(row[3]))
                pivot_dict[geo][time][fields_list[3]] = int(float(row[4]))

#print (times_list)
#print (geo_names_list)
#print (fields_list)
#print (pivot_dict)

# now let's make some graphs!
selected_geography = 'Thailand'


#fig, axes = plt.subplots(3,3)
fig_num = 0
colors = ['r','b','m','g--']
labels = ['Indigenous range','Structural habitat','Effective potential habitat','Known occupied habitat']


# loop over geographies and make plots
for geo in geo_names_list:
    
        fig = plt.figure(fig_num)
        #if geo == selected_geography:
        figure_filename = pivot_type + "_" + geo + ".png"
        # loop over the areas 
        for a in range(len(fields_list)):
            if a == 0: continue
            areas_list = []
            years_list = []
            # for a given geography and area type, gt the data and send to plot
            for time in times_list:
                areas_list.append(pivot_dict[geo][time][fields_list[a]])
                date_list = time.split("-")
                years_list.append(date_list[0])
                #print (time, pivot_dict[geo][time][fields_list[0]])
            plt.plot(years_list, areas_list, colors[a], label = labels[a])
        plt.legend()
        plt.xticks(rotation = 90) # Rotates X-Axis Ticks
        plt.title(geo)
       # plt.show()
        fig.savefig(os.path.join(figure_dir, figure_filename))
        plt.close(fig)
        fig_num += 1




# Old code


# create data
#x = [10,20,30,40,50]
#y = [30,30,30,30,30]

# plot lines
#plt.plot(x, y, label = "line 1")
#plt.plot(y, x, label = "line 2")
#plt.legend()
#plt.show()


#print ("Hello world!")


    
#    # read in csv
#    data0_dict = csv.DictReader(csv_file, delimiter = ',')
#    data1_dict = {}
#    data2_dict = {}
#    for row in data0_dict:
#        # if get() can't find a value with an associated key, it returns the second argument, here an empty dictionary
#        data1_dict = pivot_dict.get(row['countrynam'], dict())
#        data1_dict[year] = pivot_dict[row['countrynam']].get(year, dict())
#        data2_dict
    
    
    
 