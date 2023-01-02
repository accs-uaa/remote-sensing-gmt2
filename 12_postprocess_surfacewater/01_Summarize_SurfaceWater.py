# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Summarize surface water to surficial features
# Author: Timm Nawrocki
# Last Updated: 2022-12-23
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Summarize surface water to surficial features" processes the surficial water raster into the final deliverable.
# ---------------------------------------------------------------------------

# Import packages
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import summarize_to_regions

# Set round date
round_date = 'round_20221219'
version_number = 'v1_0'

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')

# Define geodatabases
work_geodatabase = os.path.join(project_folder, 'GMT2_Workspace.gdb')

# Define input datasets
study_raster = os.path.join(project_folder, 'Data_Input/GMT2_StudyArea.tif')
water_raster = os.path.join(project_folder, 'Data_Output/output_rasters',
                            round_date, 'surface_water', 'GMT2_SeasonalWater_Percentage.tif')
surficial_raster = os.path.join(project_folder, 'Data_Output/output_rasters',
                                round_date, 'surficial_features', 'GMT2_SurficialFeatures.tif')

# Define output raster
output_raster = os.path.join(project_folder, 'Data_Output/data_package', version_number, 'surface_water',
                             'GMT2_SeasonalWater_Percentage.tif')

# Create key word arguments
kwargs_summarize = {'work_geodatabase': work_geodatabase,
                    'input_array': [study_raster, water_raster, surficial_raster],
                    'output_array': [output_raster]
                    }

# Post-process seasonal water percentage raster
print(f'Post-processing seasonal water percentage raster...')
arcpy_geoprocessing(summarize_to_regions, **kwargs_summarize)
print('----------')
