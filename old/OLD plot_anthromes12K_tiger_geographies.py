# plot_anthromes12K_tiger_geographies.py
# ews 12/4/2021


import os
import csv
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

# working directory
anthromes_output = r'C:\Users\esanderson\Documents\jupyter_notebooks\anthromes_tigers'

# summary of the zonal histogram outputs goes into a dataframe (df)
csv_file = os.path.join(anthromes_output, "tiger_habitat_ecoregions2.csv")
df = pd.read_csv(csv_file)
df.set_index('Year', inplace=True, drop=True)


# names and categories of the ecoregions
csv_file2 = "Sum_tiger_historic_range_12-04-2021_prj2.csv"
df_names = pd.read_csv(csv_file2)
names_dict = df_names.set_index('formatted_ECO_ID').T.to_dict('list')

# iterate over data frame, making a plot of each row
for idx, val in enumerate(df.columns):
    ymax_value = df[df.columns[idx]].max();
    eco_code = list(names_dict.keys())[idx];
    name = names_dict[eco_code][2];
    category = names_dict[eco_code][3];
    print(idx, val, eco_code, name, category)
    title_name = name + "\n" + category
    ax = df.plot(y=df.columns[idx],xlim=(-6500,2020), ylim = (0,ymax_value*1.1), style='-+',title=title_name);
    ax.set_xlabel("Year");
    ax.set_ylabel("Area");
    filename = val + '.jpg';
    ax.figure.savefig(filename);
