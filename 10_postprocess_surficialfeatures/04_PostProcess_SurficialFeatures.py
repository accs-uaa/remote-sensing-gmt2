# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Post-process surficial features
# Author: Timm Nawrocki
# Last Updated: 2022-12-27
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Post-process surficial features" processes the predicted raster into the final deliverable.
# ---------------------------------------------------------------------------

# Import packages
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import postprocess_categorical_raster

# Set round date
round_date = 'round_20221219'
version_number = 'v1_0'

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
class_values = {'barren': 1,
                'dunes': 2,
                'non-patterned, drained': 3,
                'non-patterned, floodplain': 4,
                'non-patterned, mesic': 5,
                'non-polygonal, wet': 6,
                'thermokarst troughs': 7,
                'polygonal, mesic': 8,
                'polygonal, wet': 9,
                'freshwater marsh': 10,
                'stream corridor': 11,
                'tidal marsh': 12,
                'salt-killed': 13,
                'vegetated coastal beach': 14,
                'water': 15,
                'pipeline': 16,
                'infrastructure': 17}

# Create key word arguments
kwargs_process = {'minimum_count': 505,
                  'stream_value': 11,
                  'water_value': 15,
                  'pipeline_value': 16,
                  'infrastructure_value': 17,
                  'conditional_statement': 'VALUE = 1 Or VALUE = 2 Or VALUE = 3',
                  'attribute_dictionary': class_values,
                  'work_geodatabase': work_geodatabase,
                  'input_array': [study_raster, input_raster, infrastructure_feature, infrastructure_raster,
                                  segments_feature, pipeline_raster, stream_raster],
                  'output_array': [output_raster]
                  }

# Post-process surficial features raster
print(f'Post-processing surficial features raster...')
arcpy_geoprocessing(postprocess_categorical_raster, **kwargs_process)
print('----------')
