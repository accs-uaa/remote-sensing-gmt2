# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Post-process Phenology Greendown
# Author: Timm Nawrocki
# Last Updated: 2022-12-27
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Post-process Phenology Greendown" calculates mean greendown date and corrects to predicted surface types.
# ---------------------------------------------------------------------------

# Import packages
import arcpy
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import postprocess_continuous_raster

# Set round date
round_date = 'round_20221219'
version_number = 'v1_0'

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')
input_folder = os.path.join(project_folder, 'Data_Output/output_rasters', round_date, 'phen_greendown')
output_folder = os.path.join(project_folder, 'Data_Output/data_package', version_number, 'phen_greendown')

# Define geodatabases
work_geodatabase = os.path.join(project_folder, 'GMT2_Workspace.gdb')

# Define input datasets
study_raster = os.path.join(project_folder, 'Data_Input/GMT2_StudyArea.tif')
evt_raster = os.path.join(project_folder, 'Data_Output/output_rasters', round_date, 'vegetation_type',
                          'GMT2_ExistingVegetationType.tif')
infrastructure_raster = os.path.join(project_folder, 'Data_Input/infrastructure/Infrastructure_Developed.tif')

# Create empty list for input rasters
input_rasters = []

# Create list of input rasters
input_list = [[1, 2, 3, 4, 5],
              [6, 7, 8, 9, 10],
              [11, 12, 13, 14, 15],
              [16, 17, 18, 19, 20]]

# Loop through each input raster and post-process to output raster
count = 1
input_length = len(input_list)
for input_set in input_list:
    # Create empty list of input rasters
    input_rasters = []

    # Define input rasters
    for year in input_set:
        input_raster = os.path.join(input_folder, f'GMT2_Phen_Greendown_{str(year+2000)}.tif')
        input_rasters.append(input_raster)

    # Define output raster
    if count == 1:
        output_raster = os.path.join(output_folder, 'GMT2_Phen_Greendown_2005.tif')
    elif count == 2:
        output_raster = os.path.join(output_folder, 'GMT2_Phen_Greendown_2010.tif')
    elif count == 3:
        output_raster = os.path.join(output_folder, 'GMT2_Phen_Greendown_2015.tif')
    else:
        output_raster = os.path.join(output_folder, 'GMT2_Phen_Greendown_2020.tif')

    # Create output raster if it does not already exist
    if arcpy.Exists(output_raster) == 0:
        # Create key word arguments
        kwargs_process = {'calculate_mean': True,
                          'conditional_statement': 'VALUE = 1 Or VALUE = 2 Or VALUE = 5',
                          'data_type': '8_BIT_UNSIGNED',
                          'work_geodatabase': work_geodatabase,
                          'input_array': [study_raster, evt_raster, infrastructure_raster] + input_rasters,
                          'output_array': [output_raster]
                          }

        # Post-process phenology rasters
        print(f'Post-processing raster {count} of {input_length}...')
        arcpy_geoprocessing(postprocess_continuous_raster, **kwargs_process)
        print('----------')
    else:
        print(f'Raster {count} of {input_length} already exists.')
        print('----------')
    count += 1
