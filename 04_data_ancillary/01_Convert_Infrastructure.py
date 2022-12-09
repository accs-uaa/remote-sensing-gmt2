# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Convert infrastructure to raster
# Author: Timm Nawrocki
# Last Updated: 2022-12-08
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Convert infrastructure to raster" creates an infrastructure raster from a manually-delineated or pre-existing feature class source.
# ---------------------------------------------------------------------------

# Import packages
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import convert_to_binary_raster

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')
infrastructure_folder = os.path.join(project_folder, 'Data_Input/infrastructure')

# Define work geodatabase
work_geodatabase = os.path.join(project_folder, 'GMT2_RemoteSensing.gdb')

# Define input datasets
study_raster = os.path.join(project_folder, 'Data_Input/GMT2_StudyArea.tif')
input_feature = os.path.join(work_geodatabase, 'Infrastructure_Developed')

# Define output dataset
output_raster = os.path.join(infrastructure_folder, 'Infrastructure_Developed.tif')

# Create key word arguments
kwargs_convert = {'buffer_distance': None,
                  'work_geodatabase': work_geodatabase,
                  'input_array': [study_raster, input_feature],
                  'output_array': [output_raster]
                  }

# Process the infrastructure
print(f'Converting infrastructure to raster...')
arcpy_geoprocessing(convert_to_binary_raster, **kwargs_convert)
print('----------')
