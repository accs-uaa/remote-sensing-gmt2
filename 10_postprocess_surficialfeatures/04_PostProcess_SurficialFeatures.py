# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Post-process surficial features
# Author: Timm Nawrocki
# Last Updated: 2022-12-15
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Post-process surficial features" processes the predicted raster into the final deliverable.
# ---------------------------------------------------------------------------

# Import packages
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import postprocess_predicted_raster

# Set round date
round_date = 'round_20221209'
version_number = 'v0_1'

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')

# Define geodatabases
project_geodatabase = os.path.join(project_folder, 'GMT2_RemoteSensing.gdb')
work_geodatabase = os.path.join(project_folder, 'GMT2_Workspace.gdb')

# Define input datasets
study_raster = os.path.join(project_folder, 'Data_Input/GMT2_StudyArea.tif')
input_raster = os.path.join(project_folder, 'Data_Output/output_rasters',
                            round_date, 'surficial_features', 'GMT2_SurficialFeatures.tif')
infrastructure_feature = os.path.join(project_geodatabase, 'Infrastructure_Developed')
infrastructure_raster = os.path.join(project_folder, 'Data_Input/infrastructure',
                                     'Infrastructure_Developed.tif')
segments_feature = os.path.join(project_geodatabase, 'GMT2_Segments_Revised_Polygon')
pipeline_raster = os.path.join(project_folder, 'Data_Input/infrastructure',
                               'Infrastructure_Pipelines.tif')
stream_raster = os.path.join(project_folder, 'Data_Input/hydrography/processed/Streams.tif')

# Define output raster
output_raster = os.path.join(project_folder, 'Data_Output/data_package', version_number, 'surficial_features',
                             'GMT2_SurficialFeatures.tif')

# Define surficial features dictionary
surficial_dictionary = {'barren': 1,
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

# Create key word arguments
kwargs_process = {'minimum_count': 505,
                  'stream_value': 10,
                  'water_value': 13,
                  'pipeline_value': 14,
                  'infrastructure_value': 15,
                  'attribute_dictionary': surficial_dictionary,
                  'work_geodatabase': work_geodatabase,
                  'input_array': [study_raster, input_raster, infrastructure_feature, infrastructure_raster,
                                  segments_feature, pipeline_raster, stream_raster],
                  'output_array': [output_raster]
                  }

# Post-process surficial features raster
print(f'Post-processing surficial features raster...')
arcpy_geoprocessing(postprocess_predicted_raster, **kwargs_process)
print('----------')
