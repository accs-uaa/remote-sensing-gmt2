# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Create existing vegetation type rasters
# Author: Timm Nawrocki
# Last Updated: 2022-12-12
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Create existing vegetation type rasters" combines tiles into a vegetation type raster.
# ---------------------------------------------------------------------------

# Import packages
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import predictions_to_raster

# Set round date
round_date = 'round_20221209'

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')
segment_folder = os.path.join(project_folder, 'Data_Input/imagery/segments/gridded')
prediction_folder = os.path.join(project_folder, 'Data_Output/predicted_tables', round_date, 'vegetation')
grid_folder = os.path.join(project_folder, 'Data_Output/predicted_rasters', round_date, 'vegetation')
output_folder = os.path.join(project_folder, 'Data_Output/output_rasters', round_date, 'vegetation')

# Define geodatabases
work_geodatabase = os.path.join(project_folder, 'GMT2_Workspace.gdb')

# Define input datasets
study_raster = os.path.join(project_folder, 'Data_Input/GMT2_StudyArea.tif')

# Define output raster
output_raster = os.path.join(output_folder, 'GMT2_ExistingVegetationType.tif')

# Define EVT dictionary
evt_dictionary = {'coastal and estuarine barren': 1,
                  'freshwater floodplain barren': 2,
                  'salt-killed tundra or marsh': 3,
                  'stream corridor': 4,
                  'water': 5,
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
kwargs_attributes = {'segment_folder': segment_folder,
                     'prediction_folder': prediction_folder,
                     'grid_folder': grid_folder,
                     'target_field': 'evt_value',
                     'data_type': 'discrete',
                     'attribute_dictionary': evt_dictionary,
                     'conversion_factor': 'NA',
                     'work_geodatabase': work_geodatabase,
                     'input_array': [study_raster],
                     'output_array': [output_raster]
                     }

# Convert predictions to EVT raster
print(f'Converting predictions to EVT raster...')
arcpy_geoprocessing(predictions_to_raster, **kwargs_attributes)
print('----------')
