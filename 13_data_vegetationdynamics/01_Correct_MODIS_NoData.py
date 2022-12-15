# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Correct null values for MODIS data
# Author: Timm Nawrocki
# Last Updated: 2022-12-14
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Correct null values for MODIS data" corrects null values below a threshold of 1 for MODIS phenology and productivity datasets.
# ---------------------------------------------------------------------------

# Import packages
import arcpy
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import correct_no_data

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')
vegetation_folder = os.path.join(project_folder, 'Data_Input/vegetation/foliar_cover')
productivity_input = os.path.join(project_folder, 'Data_Input/imagery/modis_productivity/unprocessed')
phenology_input = os.path.join(project_folder, 'Data_Input/imagery/modis_phenology/unprocessed')
productivity_output = os.path.join(project_folder, 'Data_Input/imagery/modis_productivity/processed')
phenology_output = os.path.join(project_folder, 'Data_Input/imagery/modis_phenology/processed')

# Define input datasets
sample_raster = os.path.join(project_folder, 'Data_Input/validation/MODIS_SamplingGrid_500m.tif')

# Define work geodatabase
project_geodatabase = os.path.join(project_folder, 'GMT2_RemoteSensing.gdb')
work_geodatabase = os.path.join(project_folder, 'GMT2_Workspace.gdb')

# Create empty raster lists
productivity_list = []
phenology_list = []

# Create list of productivity rasters
arcpy.env.workspace = productivity_input
productivity_rasters = arcpy.ListRasters('*', 'TIF')
for raster in productivity_rasters:
    raster_path = os.path.join(productivity_input, raster)
    productivity_list.append(raster_path)

# Create list of phenology rasters
arcpy.env.workspace = phenology_input
phenology_rasters = arcpy.ListRasters('*', 'TIF')
for raster in phenology_rasters:
    raster_path = os.path.join(phenology_input, raster)
    phenology_list.append(raster_path)

# Set workspace to default
arcpy.env.workspace = work_geodatabase

#### CORRECT NO DATA FOR PRODUCTIVITY RASTERS
count = 1
raster_length = len(productivity_list) + len(phenology_list)
for input_raster in productivity_list:
    # Define output raster
    raster_name = os.path.split(input_raster)[1]
    output_raster = os.path.join(productivity_output, raster_name)

    # Create zonal summary if output raster does not already exist
    if arcpy.Exists(output_raster) == 0:
        # Create key word arguments
        kwargs_correct = {'threshold': 1,
                          'work_geodatabase': work_geodatabase,
                          'input_array': [sample_raster, input_raster],
                          'output_array': [output_raster]
                          }

        # Process the zonal summaries
        print(f'Processing no data for raster {count} of {raster_length}...')
        arcpy_geoprocessing(correct_no_data, **kwargs_correct)
        print('----------')

    # If raster already exists, print message
    else:
        print(f'Raster {count} of {raster_length} already exists.')
        print('----------')

    # Increase counter
    count += 1

#### CORRECT NO DATA VALUES FOR PHENOLOGY RASTERS

for input_raster in phenology_list:
    # Define output raster
    raster_name = os.path.split(input_raster)[1]
    output_raster = os.path.join(phenology_output, raster_name)

    # Create zonal summary if output raster does not already exist
    if arcpy.Exists(output_raster) == 0:
        # Create key word arguments
        kwargs_correct = {'threshold': 1,
                          'work_geodatabase': work_geodatabase,
                          'input_array': [sample_raster, input_raster],
                          'output_array': [output_raster]
                          }

        # Process the zonal summaries
        print(f'Processing no data for raster {count} of {raster_length}...')
        arcpy_geoprocessing(correct_no_data, **kwargs_correct)
        print('----------')

    # If raster already exists, print message
    else:
        print(f'Raster {count} of {raster_length} already exists.')
        print('----------')

    # Increase counter
    count += 1
