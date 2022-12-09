# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Create geomorphology rasters
# Author: Timm Nawrocki
# Last Updated: 2022-12-04
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Create geomorphology rasters" combines tiles into a discrete geomorphology raster and probabilistic class rasters.
# ---------------------------------------------------------------------------

# Import packages
import arcpy
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import predictions_to_raster

# Set round date
round_date = 'round_20221125'

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')
segment_folder = os.path.join(project_folder, 'Data_Input/imagery/segments/gridded')
prediction_folder = os.path.join(project_folder, 'Data_Output/predicted_tables', round_date, 'geomorphology')
raster_folder = os.path.join(project_folder, 'Data_Output/predicted_rasters', round_date)
output_folder = os.path.join(project_folder, 'Data_Output/output_rasters', round_date, 'geomorphology')

# Define geodatabases
work_geodatabase = os.path.join(project_folder, 'GMT2_RemoteSensing.gdb')

# Define input datasets
study_raster = os.path.join(project_folder, 'Data_Input/GMT2_StudyArea.tif')

# Define output raster
output_raster = os.path.join(output_folder, 'GMT2_Geomorphology.tif')

#### CREATE DISCRETE PHYSIOGRAPHY

# Define and create geomorphology directory
geomorphology_folder = os.path.join(raster_folder, 'geomorphology')
if os.path.exists(geomorphology_folder) == 0:
    os.mkdir(geomorphology_folder)

# Define geomorphology dictionary
geomorphology_dictionary = {'barren': 1,
                            'dunes': 2,
                            'non-patterned': 3,
                            'polygonal, wet center': 4,
                            'polygonal, wet trough': 5,
                            'salt-killed': 6,
                            'tidal marsh': 7,
                            'water': 8
                            }

# Create key word arguments
kwargs_discrete = {'segment_folder': segment_folder,
                   'prediction_folder': prediction_folder,
                   'grid_folder': geomorphology_folder,
                   'target_field': 'geomorphology',
                   'data_type': 'discrete',
                   'attribute_dictionary': geomorphology_dictionary,
                   'conversion_factor': 'NA',
                   'work_geodatabase': work_geodatabase,
                   'input_array': [study_raster],
                   'output_array': [output_raster]
                   }

# Convert predictions to physiography raster
if arcpy.Exists(output_raster) == 0:
    print(f'Converting discrete predictions to physiography raster...')
    arcpy_geoprocessing(predictions_to_raster, **kwargs_discrete)
    print('----------')
else:
    print('Discrete raster already exists.')
    print('----------')

#### CREATE CONTINUOUS PHYSIOGRAPHY PROBABILITY

# Define class list and physiography list
class_list = ['class_01', 'class_02', 'class_03', 'class_04',
              'class_05', 'class_06', 'class_07', 'class_08']
physiography_list = ['barren', 'dunes', 'nonpatterned', 'polywetcenter',
                     'polywettrough', 'saltkilled', 'tidalmarsh', 'water']

# Iterate through each class and export a continuous probability raster
count = 1
for class_label in class_list:
    # Identify corresponding physiography label
    physiography_label = physiography_list[count - 1]

    # Define and create physiography directory
    probability_folder = os.path.join(raster_folder, 'geomorph_' + physiography_label)
    if os.path.exists(probability_folder) == 0:
        os.mkdir(probability_folder)

    # Define output raster
    physiography_name = physiography_label.capitalize()
    continuous_output = os.path.join(output_folder, f'GMT2_GeomorphProbability_{physiography_name}.tif')

    # Create key word arguments
    kwargs_continuous = {'segment_folder': segment_folder,
                         'prediction_folder': prediction_folder,
                         'grid_folder': probability_folder,
                         'target_field': class_label,
                         'data_type': 'continuous',
                         'attribute_dictionary': 'NA',
                         'conversion_factor': 1000,
                         'work_geodatabase': work_geodatabase,
                         'input_array': [study_raster],
                         'output_array': [continuous_output]
                         }

    # Convert predictions to probability raster
    if arcpy.Exists(continuous_output) == 0:
        print(f'Converting probability predictions for {physiography_label} to raster...')
        arcpy_geoprocessing(predictions_to_raster, **kwargs_continuous)
        print('----------')
    else:
        print(f'{physiography_name} raster already exists.')
        print('----------')

    # Increase count
    count += 1
