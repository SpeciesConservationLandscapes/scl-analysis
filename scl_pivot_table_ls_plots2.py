# scl_pivot_table_plots2.py
# ews 9/15/2022

# objective:  plot the national level pivot table results from the scl analysis
# into a series of subplots, showing either habitat or landscape data, per country
# over the length of the time series

# this script depends on successful completion of 
#   scl_analyze_hab_by_country2.py for the habitat areas by country
#   scl_analyze_ls_by_country2.py for the landscape areas by country

# previous attempts:  see scl_pivot_table_plots.py, scl_pivot_table_habitat_subplots.py

# approach:
#    read in the pivot tables by year
#    hold them in a nested dictionary keyd by data type and country, holding all the areas 
#    in a chronological list matching a list of all the time points


# some imports
import os
import pandas as pd
import matplotlib.pyplot as plt
import csv
import math

# Set up

# data files organized by folder by time point are in this directory:
scl_dir = r"C:\proj\species\tigers\TCLs v3\TCL delineation\scl_stats_09142022"
# subdirectory for pivot tables outputs
pivot_subdir = "pivot_tables\landscape_areas"
# figure subdirectory
fig_subdir = "pivot_tables\plots"
# example data file
example_data = "hab_pivot.2001-01-01.csv"


# the years to analyze are:
timepoints = ['2020-01-01','2019-01-01','2018-01-01','2017-01-01','2016-01-01','2015-01-01','2014-01-01','2013-01-01','2012-01-01','2011-01-01','2010-01-01','2009-01-01','2008-01-01','2007-01-01','2006-01-01','2005-01-01','2004-01-01','2003-01-01','2002-01-01','2001-01-01']
# a single year for testing purposes
#timepoints = ['2020-01-01']

# countries are:
countries = ['Afghanistan','Armenia','Arunachal Pradesh','Azad Kashmir','Azerbaijan','Bangladesh','Bhutan','Cambodia','China','Georgia','Hong Kong','India','Indonesia','Iran','Iraq','Jammu and Kashmir','Kazakhstan','Kyrgyzstan','Laos','Macao','Malaysia','Myanmar','Nepal','North Korea','Pakistan','Russia','Singapore','South Korea','Syria','Tajikistan','Thailand','Turkey','Turkmenistan','Uzbekistan','Vietnam']
# a single country for testing purposes
#countries = ['Afghanistan']

# landscape types to analyze are:
types = ['scl_restoration','scl_restoration_fragment','scl_species','scl_species_fragment','scl_survey','scl_survey_fragment']
# a single habitat type for testing purposes
#types = ['indigenous_range_area']

# get a list of the years from time points (this will be x axis for plots)
years_list = []
for time in timepoints:
   time_list = time.split("-")
   years_list.append(int(time_list[0]))
years_list.sort()


# get a list of the countries from example file
#df = pd.read_csv(os.path.join(scl_dir, pivot_subdir, example_data))
#countries = df['countrynam'].tolist()
#print(countries)

# create nested dictionary to hold the data
data_dict = {}
for country in countries:
    data_dict[country] = {}
    for type in types:
       data_dict[country][type] = {}
       for year in years_list:
          data_dict[country][type][year] = 0

# read in the csv files and populate a dictionary
for time in timepoints:
    # get year
    time_list = time.split("-")
    year = int(time_list[0])
    # put together filename and load up
    csvfilename = "ls_pivot." + time + ".csv"
    df = pd.read_csv(os.path.join(scl_dir, pivot_subdir, csvfilename), header=1)
    for col in df.columns:
        print(col)
        
    # set index of country names
    df.set_index('country', inplace=True)
    #print(df.head())
    # convert to dictionary
    hab_dict = df.to_dict('index')
    # loop over the keys to hab_dict, which are countries, and create lists for each of the data types
    for country in hab_dict.keys():
       for type in hab_dict[country].keys():   # these are the data types
          try:
             print("Working on ", country, type, year)
             data_dict[country][type][year] = hab_dict[country][type]
          except:
             print("Skipping with ", country, type, year)

# export that dictionary for further analysis
# thank you to https://stackoverflow.com/questions/24988131/nested-dictionary-to-multiindex-dataframe-where-dictionary-keys-are-column-label
df_unstacked = pd.DataFrame.from_dict(data_dict, orient="index").stack().to_frame()
df_restacked = pd.DataFrame(df_unstacked[0].values.tolist(), index=df_unstacked.index)
df_transposed = pd.DataFrame.transpose(df_restacked)

#for col in df_transposed.columns:
#    print(col)

csvfilename = "ls_country_pivot.all_years.csv"
df_transposed.to_csv(os.path.join(scl_dir, pivot_subdir, csvfilename))


# now we can make some plots
number_plots = len(countries)  # note for tigers, there are 35 countries, including disputed territories

# desired subplots
number_rows = 3
number_columns = 4
number_plots_per_page = number_rows * number_columns

# number of pages
number_pages = math.ceil(number_plots/(number_plots_per_page))
remainder = (number_plots/(number_plots_per_page)) % 1   # use modulo operator

# set colors and labels
colors = {
   'indigenous_range_area' : 'r',
   'str_hab_area' : 'b',
   'eff_pot_hab_area' : 'm',
   'occupied_eff_pot_hab_area' : 'g--'
   }
labels = {
   'indigenous_range_area' : 'Indigenous range',
   'str_hab_area' : 'Structural habitat',
   'eff_pot_hab_area' : 'Effective potential habitat',
   'occupied_eff_pot_hab_area' : 'Known occupied habitat'
   }

# for testing
#countries = ['Afghanistan','Armenia','Arunachal Pradesh','Azad Kashmir','Azerbaijan','Bangladesh','Bhutan','Cambodia','China','Georgia','Hong Kong','India']

# loop over pages, allocating countries in order to each page based on number of subplots
for page in range(number_pages):

    # figure out which countries go on which page based on number of subplots per page
    start_country_index = number_plots_per_page * page
    if (number_plots_per_page * page) <= number_plots:
       end_country_index = start_country_index + number_plots_per_page
    else:
       end_country_index = start_country_index + remainder
    # slice out the countries for this page
    these_countries = countries[start_country_index:end_country_index]
    #print(page, number_pages, start_country_index, end_country_index)
    #print(these_countries)
    
    # set up plots on page
    fig, axes = plt.subplots(nrows=number_rows, ncols=number_columns, sharex=True, sharey=False)
    #figure(figsize=(7.5,9))
    fig_num = 0
    
    # initialize plot number
    plot_num = 1

    # loop over geographies and make plots
    for country in these_countries:

        plt.subplot(number_rows,number_columns,plot_num)
    
        figure_filename = "habitat_plot." + country + ".png"
        # loop over data_dict and extract data for plot 
        for type in types:
            if type == 'indigenous_range_area': 
                indigenous_area = data_dict[country][type][year]
                indigenous_text = "Indigenous range = " + str(int(indigenous_area))
                continue
            data_list = []
            for year in years_list:
                data_list.append(data_dict[country][type][year])
            plt.plot(years_list, data_list, colors[type], label = labels[type])
        #plt.legend()
        plt.xticks(years_list)
        plt.locator_params(axis='x', nbins = 5)
        plt.xticks(rotation = 90) # rotates X-Axis Ticks
        #plt.ylabel("Area (km2)")
        title_text = country + " \n(" + indigenous_text + ")"
        #title_text = country
        plt.title(title_text, fontsize = 8)
        #plt.close(fig)
        
        # increment plot number
        plot_num += 1
        
    #plt.show()
    fig_filename = "habitat_by_country." + str(page) + ".png"
    #plt.savefig(os.path.join(scl_dir, fig_subdir, fig_filename), format="png")

print("That's all folks!")