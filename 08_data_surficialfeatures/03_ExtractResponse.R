# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Extract response data to points
# Author: Timm Nawrocki
# Last Updated: 2022-12-20
# Usage: Must be executed in R 4.0.0+.
# Description: "Extract response data to points" extracts the training and validation grid data to points.
# ---------------------------------------------------------------------------

# Set root directory
drive = 'N:'
root_folder = 'ACCS_Work'

# Define input folders
project_folder = paste(drive,
                       root_folder,
                       'Projects/VegetationEcology/BLM_AIM/GMT-2/Data',
                       sep = '/')
grid_folder = paste(project_folder,
                    'Data_Input/validation',
                    sep = '/')
training_folder = paste(project_folder,
                        'Data_Input/training_data',
                        sep = '/')

# Define output folders
output_folder = paste(training_folder,
                      'table_training',
                      sep = '/')

# Define segments geodatabase
segments_geodatabase = paste(project_folder,
                             'GMT2_Segments_Gridded.gdb',
                             sep = '/')

# Define input datasets
grid_raster = paste(grid_folder, 'GMT2_ValidationGroups.tif', sep = '/')
training_raster = paste(training_folder, 'processed/Training_SurficialFeatures.tif', sep = '/')

# Define grids
grid_list = c('A4', 'A5', 'A6', 'A7',
              'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7',
              'C1', 'C2', 'C3', 'C4', 'C5', 'C6',
              'D1', 'D2', 'D3', 'D4', 'D5',
              'E1', 'E2', 'E3', 'E4', 'E5')
grid_length = length(grid_list)

# Import required libraries for geospatial processing: dplyr, raster, rgdal, sp, and stringr.
library(dplyr)
library(raster)
library(sf)
library(stringr)

# Generate a stack of ancillary rasters
print('Creating ancillary raster stack...')
start = proc.time()
ancillary_stack = stack(c(grid_raster, training_raster))
end = proc.time() - start
print(end[3])

# Set count
count = 1

# Loop through each grid and extract covariates
for (grid in grid_list) {
  # Define input points
  input_points = paste('points_', grid, sep = '')
  
  # Define output table
  output_file = paste(output_folder, '/', grid, '.csv', sep = '')
  
  # Create output table if it does not already exist
  if (!file.exists(output_file)) {
    print(paste('Extracting segments ', toString(count), ' out of ', toString(grid_length), '...', sep=''))
    
    # Read path data
    print('Extracting covariates...')
    start = proc.time()
    print(input_points)
    point_data = st_read(dsn = segments_geodatabase, layer = input_points)
    end = proc.time() - start
    print(end[3])
    
    # Extract ancillary data
    print('Extracting ancillary data...')
    start = proc.time()
    point_ancillary = data.frame(point_data, raster::extract(ancillary_stack, point_data))
    end = proc.time() - start
    print(end[3])
    
    # Convert field names to standard
    point_ancillary = point_ancillary %>%
      dplyr::rename(cv_group = GMT2_ValidationGroups,
                    train_class = Training_SurficialFeatures) %>%
      dplyr::select(-POINT_X, -POINT_Y, -shape_m, -shape_m2)
    
    # Export data as a csv
    st_write(point_ancillary, output_file, coords = FALSE)
    print(paste('Extraction iteration ', toString(count), ' out of ', toString(grid_length), ' completed.', sep=''))
    print('----------')
  } else {
    # Report that output already exists
    print(paste('Extraction ', toString(count), ' out of ', toString(grid_length), ' already exists.', sep = ''))
    print('----------')
  }
  # Increase count
  count = count + 1
}
