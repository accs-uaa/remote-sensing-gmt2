# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Merge phenology greenup rasters
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Last Updated: 2022-12-15
# Usage: Code chunks must be executed sequentially in R Studio or R Studio Server installation.
# Description: "Merge phenology greenup rasters" merges the predicted grid rasters into a single output raster.
# ---------------------------------------------------------------------------

# Define round date
round_date = 'round_20221209'

# Set root directory
drive = 'N:'
root_folder = 'ACCS_Work'

# Define input folders
project_folder = paste(drive,
                       root_folder,
                       'Projects/VegetationEcology/BLM_AIM/GMT-2/Data',
                       sep = '/')

# Define input folder
raster_folder = paste(project_folder,
                      'Data_Output/predicted_rasters',
                      round_date,
                      'phen_greenup',
                      sep = '/')

# Define output folder
output_folder = paste(project_folder,
                      'Data_Output/output_rasters',
                      round_date,
                      'phen_greenup',
                      sep = '/')

# Import required libraries for geospatial processing: sp, raster, rgdal, and stringr.
library(sp)
library(raster)
library(rgdal)

# Create year list
year_list = seq(1, 20, 1)

# Iterate through major grids and merge raster tiles
for (year in year_list) {
  
  # Define input folder
  input_folder = paste(raster_folder, year, sep = '/')
  
  # Define output file
  output_raster = paste(output_folder, 
                        '/',
                        'GMT2_Phen_Greenup_',
                        year + 2000,
                        '.tif',
                        sep = '')
  
  # Generate output raster if it does not already exist
  if (!file.exists(output_raster)) {
    
    # Generate list of raster img files from input folder
    raster_files = list.files(path = input_folder,
                              pattern = paste('..*.tif$', sep = ''),
                              full.names = TRUE)
    count = length(raster_files)
    
    # Convert list of files into list of raster objects
    start = proc.time()
    print(paste('Compiling ', toString(count), ' rasters for year ', toString(year + 2000), '...'))
    raster_objects = lapply(raster_files, raster)
    # Add function and filename attributes to list
    raster_objects$fun = max
    raster_objects$filename = output_raster
    raster_objects$overwrite = TRUE
    raster_objects$datatype = 'FLT4S'
    raster_objects$progress = 'text'
    raster_objects$format = 'GTiff'
    raster_objects$options = c('TFW=YES')
    end = proc.time() - start
    print(paste('Completed in ', end[3], ' seconds.', sep = ''))
    
    # Merge rasters
    start = proc.time()
    print(paste('Merging ', toString(count), ' rasters for year ', toString(year + 2000), '...'))
    merged_raster = do.call(mosaic, raster_objects)
    end = proc.time() - start
    print(paste('Completed in ', end[3], ' seconds.', sep = ''))
  } else {
    print(paste('Raster ', major_grid, ' already exists.'))
  }
}