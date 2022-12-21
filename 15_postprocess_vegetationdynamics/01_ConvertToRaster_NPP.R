# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Convert NPP predictions to rasters
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Last Updated: 2022-12-15
# Usage: Script must be executed using R 4.2.1+.
# Description: "Convert NPP predictions to rasters" processes the predicted tables into predicted rasters by grid.
# ---------------------------------------------------------------------------

# Define round date and target
round_date = 'round_20221209'
target = 'pred_npp'

# Set root directory
drive = 'N:'
root_folder = 'ACCS_Work'

# Define input folders
project_folder = paste(drive,
                       root_folder,
                       'Projects/VegetationEcology/BLM_AIM/GMT-2/Data',
                       sep = '/')

# Define folder containing segment rasters
segment_folder = paste(project_folder,
                       'Data_Input/imagery/segments/gridded',
                       sep = '/')

# Define geodatabase storing segment polygons
segment_geodatabase = paste(project_folder,
                            'GMT2_Segments_Gridded.gdb',
                            sep = '/')

# Define input folder
prediction_folder = paste(project_folder,
                          'Data_Output/predicted_tables',
                          round_date,
                          'productivity',
                          sep = '/')
# Define output folder
raster_folder = paste(project_folder,
                      'Data_Output/predicted_rasters',
                      round_date,
                      'productivity',
                      sep = '/')

# Import required libraries for geospatial processing: sp, raster, rgdal, and stringr.
library(dplyr)
library(fasterize)
library(sf)
library(sp)
library(raster)
library(rgdal)
library(stringr)

# Define grids
grid_list = c('A4', 'A5', 'A6', 'A7',
             'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7',
             'C1', 'C2', 'C3', 'C4', 'C5', 'C6',
             'D1', 'D2', 'D3', 'D4', 'D5',
             'E1', 'E2', 'E3', 'E4', 'E5')
prediction_length = length(grid_list)

# Convert rasters for each year in sequence
year_list = seq(0, 20, 1)
for (year in year_list) {
  # Define input folder
  input_folder = paste(prediction_folder, year, sep = '/')
  
  # Define output folder
  output_folder = paste(raster_folder, year, sep = '/')
  
  # Create raster directory if it does not exist
  if (!file.exists(output_folder)) {
    dir.create(output_folder)
  }
  
  # Loop through each grid and convert predictions to raster
  count = 1
  for (grid in grid_list) {
    # Define input and output data
    input_file = paste(input_folder, '/', grid, '.csv', sep = '')
    segment_file = paste(segment_folder, '/', grid, '.tif', sep = '')
    segment_feature = paste('polygons_', grid, sep = '')
    output_raster = paste(output_folder, '/', grid, '.tif', sep='')
    
    # Process raster if it does not already exist
    if (!file.exists(output_raster)) {
      start = proc.time()
      # Import data
      input_data = read.csv(input_file)
      segment_raster = raster(segment_file)
      segment_polygon = st_read(dsn = segment_geodatabase, layer = segment_feature)
    
      # Bind predicted points to segment polygons
      segment_predictions = segment_polygon %>%
        dplyr::left_join(input_data, by = 'segment_id')
    
      # Rasterize the polygon
      predicted_raster = fasterize(segment_predictions, segment_raster, field = target, fun = 'first')
    
      # Export raster
      rf = writeRaster(predicted_raster, filename=output_raster, format="GTiff", overwrite=TRUE)
      end = proc.time() - start
      print(end[3])
      # Print output
      print(paste('Conversion iteration ',
                  toString(count),
                  ' out of ',
                  toString(prediction_length),
                  ' completed...',
                  sep=''))
      print('----------')
    } else {
      print(paste('Raster ',
                  toString(count),
                  ' out of ',
                  toString(prediction_length),
                  ' already exists.',
                  sep = ''))
      print('----------')
    }
    count = count + 1
  }
}