# scl-analysis

miscellaneous scripts for analysis of SCL and indigenous range results

SCL scripts:

**scl_convert_geojson_shp.py**: loop over directories of scl_geojson files and convert to shapefile, adding fields for species, date, and type

**scl_pivot_table_analysis.py**: loop over directory of scl_states_geojson files and create a pivot table of habitat areas (indigenous range, structural habitat, effective potential habitat, and occupied habitat) for each country for each year

**scl_pivot_table_plots.py**: loop over pivot tables (from scl_pivot_table_analysis.py) and plot the changes in habitat area for each country for each year

**scl_analyze_areas_kbas_pas.py**: reach into the nested "areas" field and pull out and summarize area of KBAs and Protected Areas for each landscape

**scl_analyze_areas_biomes.py**: reach into the nested "areas" field and pull out and summarize area of biome information for each landscape

Indigenous range scripts:

Run these first three in the order listed:

**loop_over_tabulate_areas.py**: arcpy script to iteratively run tabulate areas, analyzing the tiger ecoregion/divisions of the indigenous range against the Anthrome 12K maps

**summarize_tabluate_areas.py**: run through the tabulate area results (see tabulate_areas.py) showing the areas of Anthrome 12K classes in each indigenous range ecoregion/division, apply the Anthrome 12K definition of tiger habitat classes, and summarize the areas for each time point.

**plot_tabulate_areas.py**: join the Ecoregion/divide names with the areas of habitat over time (derived from Anthrome 12K; see summarize_tabulate_areas.py), plot the changes over time, and find the first year of significant human impact (defined as a change in 10% of habitat area

…

**Summarize_tiger_points_ecoregions.py**: script to associate references from combined_historical_points file by ecoregion into a table for the paper.
