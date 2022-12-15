# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Calculate zonal means for MODIS sampling grid
# Author: Timm Nawrocki
# Last Updated: 2022-12-14
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Calculate zonal means for MODIS sampling grid" calculates zonal means of input datasets to 500 m raster cells.
# ---------------------------------------------------------------------------

# Import packages
import arcpy
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import calculate_zonal_statistics

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define round date
round_date = 'round_20221209'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')
vegetation_folder = os.path.join(project_folder, 'Data_Input/vegetation/foliar_cover')
surficial_folder = os.path.join(project_folder, 'Data_Output/output_rasters', round_date,
                                'geomorphology/probability')
infrastructure_folder = os.path.join(project_folder, 'Data_Input/infrastructure')
productivity_folder = os.path.join(project_folder, 'Data_Input/imagery/modis_productivity/processed')
phenology_folder = os.path.join(project_folder, 'Data_Input/imagery/modis_phenology/processed')
output_folder = os.path.join(project_folder, 'Data_Input/vegetation_dynamics/zonal')

# Define input datasets
sample_raster = os.path.join(project_folder, 'Data_Input/validation/MODIS_SamplingGrid_500m.tif')
validation_raster = os.path.join(project_folder, 'Data_Input/validation/GMT2_ValidationGroups.tif')
estuary_distance = os.path.join(project_folder, 'Data_Input/hydrography/processed/Estuary_Distance.tif')
surface_water = os.path.join(project_folder, 'Data_Output/output_rasters', round_date,
                             'surface_water/GMT2_SeasonalWater_Percentage.tif')

# Define work geodatabase
project_geodatabase = os.path.join(project_folder, 'GMT2_RemoteSensing.gdb')
work_geodatabase = os.path.join(project_folder, 'GMT2_Workspace.gdb')

# Create empty raster list
input_rasters = []

# Create list of vegetation rasters
arcpy.env.workspace = vegetation_folder
vegetation_rasters = arcpy.ListRasters('*', 'TIF')
for raster in vegetation_rasters:
    raster_path = os.path.join(vegetation_folder, raster)
    input_rasters.append(raster_path)

# Create list of surficial probability rasters
arcpy.env.workspace = surficial_folder
surficial_rasters = arcpy.ListRasters('*', 'TIF')
for raster in surficial_rasters:
    raster_path = os.path.join(surficial_folder, raster)
    input_rasters.append(raster_path)

# Create list of infrastructure rasters
arcpy.env.workspace = infrastructure_folder
infrastructure_rasters = arcpy.ListRasters('*', 'TIF')
for raster in infrastructure_rasters:
    raster_path = os.path.join(infrastructure_folder, raster)
    input_rasters.append(raster_path)

# Create list of productivity rasters
arcpy.env.workspace = productivity_folder
productivity_rasters = arcpy.ListRasters('*', 'TIF')
for raster in productivity_rasters:
    raster_path = os.path.join(productivity_folder, raster)
    input_rasters.append(raster_path)

# Create list of phenology rasters
arcpy.env.workspace = phenology_folder
phenology_rasters = arcpy.ListRasters('*', 'TIF')
for raster in phenology_rasters:
    raster_path = os.path.join(phenology_folder, raster)
    input_rasters.append(raster_path)

# Append additional rasters
input_rasters.append(surface_water)
input_rasters.append(estuary_distance)
input_rasters.append(validation_raster)

# Set workspace to default
arcpy.env.workspace = work_geodatabase

# Create zonal summary for each raster in input list
count = 1
raster_length = len(input_rasters)
for input_raster in input_rasters:
    # Define output raster
    raster_name = os.path.split(input_raster)[1]
    output_raster = os.path.join(output_folder, raster_name)

    # Create zonal summary if output raster does not already exist
    if arcpy.Exists(output_raster) == 0:
        # Create key word arguments
        kwargs_zonal = {'statistic': 'MEAN',
                        'zone_field': 'VALUE',
                        'work_geodatabase': work_geodatabase,
                        'input_array': [sample_raster, input_raster],
                        'output_array': [output_raster]
                        }

        # Process the zonal summaries
        print(f'\tProcessing zonal summary {count} of {raster_length}...')
        arcpy_geoprocessing(calculate_zonal_statistics, **kwargs_zonal)
        print('\t----------')

    # If raster already exists, print message
    else:
        print(f'\tZonal summary {count} of {raster_length} already exists.')
        print('\t----------')

    # Increase counter
    count += 1
