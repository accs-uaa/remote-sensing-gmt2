# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Post-process existing vegetation type
# Author: Timm Nawrocki
# Last Updated: 2022-12-12
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Post-process existing vegetation type" processes the predicted raster into the final deliverable.
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
                            round_date, 'vegetation', 'GMT2_ExistingVegetationType.tif')
infrastructure_feature = os.path.join(project_geodatabase, 'Infrastructure_Developed')
infrastructure_raster = os.path.join(project_folder, 'Data_Input/infrastructure',
                                     'Infrastructure_Developed.tif')
segments_feature = os.path.join(project_geodatabase, 'GMT2_Segments_Revised_Polygon')
pipeline_raster = os.path.join(project_folder, 'Data_Input/infrastructure',
                               'Infrastructure_Pipelines.tif')
stream_raster = os.path.join(project_folder, 'Data_Input/hydrography/processed/Streams.tif')

# Define output raster
output_raster = os.path.join(project_folder, 'Data_Output/data_package', version_number, 'vegetation_type',
                             'GMT2_ExistingVegetationType.tif')

# Define EVT dictionary
evt_dictionary = {'coastal and estuarine barren': 1,
                  'freshwater floodplain barren': 2,
                  'salt-killed tundra or marsh': 3,
                  'stream corridor': 4,
                  'water': 5,
                  'infrastructure': 6,
                  'pipelines': 7,
                  'Arctic freshwater marsh': 8,
                  'Arctic herbaceous & dwarf shrub coastal beach': 9,
                  'Arctic herbaceous & shrub coastal dune': 10,
                  'Arctic herbaceous coastal salt marsh': 11,
                  'Arctic herbaceous inland dune': 12,
                  'Arctic sedge meadow, wet': 13,
                  'Arctic Dryas-ericaceous dwarf shrub, acidic': 14,
                  'Arctic birch low shrub, mesic': 15,
                  'Arctic birch low shrub, wet': 16,
                  'Arctic willow low shrub, mesic': 17,
                  'Arctic willow low shrub, wet': 18,
                  'Arctic alder floodplain': 19,
                  'Arctic willow floodplain': 20,
                  'Arctic willow inland dune': 21,
                  'Arctic tussock dwarf shrub tundra': 22,
                  'Arctic tussock low shrub tundra': 23,
                  'unclassified': 24,
                  'unclassified floodplain': 25
                  }

# Create key word arguments
kwargs_process = {'minimum_count': 505,
                  'stream_value': 4,
                  'water_value': 5,
                  'pipeline_value': 6,
                  'infrastructure_value': 7,
                  'attribute_dictionary': evt_dictionary,
                  'work_geodatabase': work_geodatabase,
                  'input_array': [study_raster, input_raster, infrastructure_feature, infrastructure_raster,
                                  segments_feature, pipeline_raster, stream_raster],
                  'output_array': [output_raster]
                  }

# Post-process EVT raster
print(f'Post-processing EVT raster...')
arcpy_geoprocessing(postprocess_predicted_raster, **kwargs_process)
print('----------')
