# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Convert streams to raster
# Author: Timm Nawrocki
# Last Updated: 2022-12-08
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Convert streams to raster" creates a streams raster from a manually-delineated or pre-existing feature class source.
# ---------------------------------------------------------------------------

# Import packages
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import convert_to_binary_raster
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
input_feature = os.path.join(work_geodatabase, 'Hydrography_Streams_Modified')

# Define output dataset
stream_raster = os.path.join(hydrography_folder, 'Streams.tif')
distance_raster = os.path.join(hydrography_folder, 'Stream_Distance.tif')

#### CONVERT STREAMS TO RASTER

# Create key word arguments
kwargs_convert = {'buffer_distance': '2 Meters',
                  'work_geodatabase': work_geodatabase,
                  'input_array': [study_raster, input_feature],
                  'output_array': [stream_raster]
                  }

# Process the streams
print(f'Converting streams to raster...')
arcpy_geoprocessing(convert_to_binary_raster, **kwargs_convert)
print('----------')

#### CONVERT STREAMS TO DISTANCE RASTER

# Create key word arguments
kwargs_distance = {'work_geodatabase': work_geodatabase,
                   'input_array': [study_raster, input_feature],
                   'output_array': [distance_raster]}

# Process stream distance
print(f'Calculating stream distance...')
arcpy_geoprocessing(distance_from_feature, **kwargs_distance)
print('----------')
