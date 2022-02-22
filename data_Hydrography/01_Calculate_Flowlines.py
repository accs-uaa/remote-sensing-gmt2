# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Calculate flowlines
# Author: Timm Nawrocki
# Last Updated: 2022-02-21
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Calculate flowlines" calculates a stream network from a digital elevation model. The stream network is output as a line feature class, which likely will need to be manually corrected and edited in places.
# ---------------------------------------------------------------------------

# Import packages
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import generate_flowlines

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
gmt2_feature = os.path.join(work_geodatabase, 'GMT2_StudyArea')
elevation_raster = os.path.join(topography_folder, 'Elevation.tif')

# Define output datasets
river_feature = os.path.join(work_geodatabase, 'GMT2_Rivers_DEM')
stream_feature = os.path.join(work_geodatabase, 'GMT2_Streams_DEM')

# Create key word arguments
kwargs_flow = {'threshold': 50000,
               'fill_value': 2,
               'work_geodatabase': work_geodatabase,
               'input_array': [gmt2_feature, elevation_raster],
               'output_array': [river_feature, stream_feature]
               }

# Process the flowlines
print(f'Processing flowlines...')
arcpy_geoprocessing(generate_flowlines, **kwargs_flow)
print('----------')
