# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Convert estuarine to distance
# Author: Timm Nawrocki
# Last Updated: 2022-12-09
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Convert estuarine to distance" calculate Euclidean distance from a manually-delineated or pre-existing feature class source.
# ---------------------------------------------------------------------------

# Import packages
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import distance_from_feature

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')
hydrography_folder = os.path.join(project_folder, 'Data_Input/hydrography/processed')

# Define work geodatabase
work_geodatabase = os.path.join(project_folder, 'GMT2_RemoteSensing.gdb')

# Define input datasets
study_raster = os.path.join(project_folder, 'Data_Input/GMT2_StudyArea.tif')
input_feature = os.path.join(work_geodatabase, 'Coastal_Estuarine')

# Define output dataset
distance_raster = os.path.join(hydrography_folder, 'Estuary_Distance.tif')

#### CONVERT ESTUARY TO DISTANCE RASTER

# Create key word arguments
kwargs_distance = {'work_geodatabase': work_geodatabase,
                   'input_array': [study_raster, input_feature],
                   'output_array': [distance_raster]}

# Process estuary distance
print(f'Calculating estuary distance...')
arcpy_geoprocessing(distance_from_feature, **kwargs_distance)
print('----------')
