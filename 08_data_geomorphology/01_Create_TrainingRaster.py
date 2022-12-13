# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Create training raster
# Author: Timm Nawrocki
# Last Updated: 2022-12-08
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Create training raster" creates a raster of training data values from a set of manually delineated polygons representing different types for a classification.
# ---------------------------------------------------------------------------

# Import packages
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import convert_class_data

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')
training_folder = os.path.join(project_folder, 'Data_Input/training_data/processed')

# Define geodatabases
work_geodatabase = os.path.join(project_folder, 'GMT2_RemoteSensing.gdb')

# Define input datasets
study_raster = os.path.join(project_folder, 'Data_Input/GMT2_StudyArea.tif')
class_feature = os.path.join(work_geodatabase, 'Training_Geomorphology_v7')

# Define output datasets
class_raster = os.path.join(training_folder, 'Training_Geomorphology.tif')

# Define fields
class_field = 'surface'

# Define class values
class_values = {'barren': 1,
                'dunes': 2,
                'non-patterned, drained': 3,
                'non-patterned, floodplain': 4,
                'non-patterned, mesic': 5,
                'permafrost troughs': 6,
                'polygonal, mesic center': 7,
                'polygonal, wet center': 8,
                'freshwater marsh': 9,
                'stream corridor': 10,
                'tidal marsh': 11,
                'salt-killed': 12,
                'water': 13}

#### CREATE TRAINING RASTER

# Create key word arguments
kwargs_training = {'class_field': class_field,
                   'value_dictionary': class_values,
                   'work_geodatabase': work_geodatabase,
                   'input_array': [study_raster, class_feature],
                   'output_array': [class_raster]
                   }

# Convert polygon class data to raster
print(f'Converting polygon class data to raster...')
arcpy_geoprocessing(convert_class_data, **kwargs_training)
print('----------')
