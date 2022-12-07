# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Calculate river and stream position
# Author: Timm Nawrocki
# Last Updated: 2022-11-21
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Calculate river and stream position" calculates river and stream position from a river feature class, stream feature class, and float elevation raster.
# ---------------------------------------------------------------------------

# Import packages
import arcpy
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import generate_hydrographic_position

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')
topography_folder = os.path.join(project_folder, 'Data_Input/topography/float')
hydrography_folder = os.path.join(project_folder, 'Data_Input/hydrography')

# Define work geodatabase
work_geodatabase = os.path.join(project_folder, 'GMT2_RemoteSensing.gdb')

# Define input datasets
gmt2_raster = os.path.join(project_folder, 'Data_Input/GMT2_StudyArea.tif')
elevation_raster = os.path.join(topography_folder, 'Elevation.tif')
river_feature = os.path.join(work_geodatabase, 'GMT2_Rivers_Modified')
stream_feature = os.path.join(work_geodatabase, 'GMT2_Streams_Modified')

# Define output datasets
river_raster = os.path.join(hydrography_folder, 'River_Position.tif')
stream_raster = os.path.join(hydrography_folder, 'Stream_Position.tif')

#### CALCULATE RIVER POSITION

# Create key word arguments
kwargs_river = {'distance': '3000 METERS',
                'work_geodatabase': work_geodatabase,
                'input_array': [gmt2_raster, elevation_raster, river_feature],
                'output_array': [river_raster]
                }

# Process the river flowlines
if arcpy.Exists(river_raster) == 0:
    print(f'Processing river flowlines...')
    arcpy_geoprocessing(generate_hydrographic_position, **kwargs_river)
    print('----------')
else:
    print('River position already exists.')
    print('----------')

#### CALCULATE STREAM POSITION

# Create key word arguments
kwargs_stream = {'distance': '100 METERS',
                 'work_geodatabase': work_geodatabase,
                 'input_array': [gmt2_raster, elevation_raster, stream_feature],
                 'output_array': [stream_raster]
                 }

# Process the stream flowlines
if arcpy.Exists(stream_raster) == 0:
    print(f'Processing stream flowlines...')
    arcpy_geoprocessing(generate_hydrographic_position, **kwargs_stream)
    print('----------')
else:
    print('Stream position already exists.')
    print('----------')
