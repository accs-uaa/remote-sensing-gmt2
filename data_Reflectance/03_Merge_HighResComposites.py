# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Merge high-resolution imagery composites
# Author: Timm Nawrocki
# Last Updated: 2022-02-21
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Merge high-resolution imagery composites" combines Maxar and Spot-5 imagery composites with Spot-5 imagery selected by a manually defined mask raster.
# ---------------------------------------------------------------------------

# Import packages
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import extract_raster
from package_GeospatialProcessing import merge_segmentation_imagery

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')
maxar_folder = os.path.join(project_folder, 'Data_Input/imagery/maxar/composite')
spot_folder = os.path.join(project_folder, 'Data_Input/imagery/spot/composite')
composite_folder = os.path.join(project_folder, 'Data_Input/imagery/composite')

# Define geodatabases
work_geodatabase = os.path.join(project_folder, 'GMT2_RemoteSensing.gdb')

# Define input datasets
gmt2_raster = os.path.join(project_folder, 'Data_Input/GMT2_StudyArea.tif')
maxar_mask = os.path.join(project_folder, 'Data_Input/imagery/maxar/maxar_mask.tif')
maxar_image = os.path.join(maxar_folder, 'GMT2_MaxarComposite_AKALB.tif')
spot_image = os.path.join(spot_folder, 'GMT2_SpotComposite_AKALB.tif')

# Define output datasets
spot_extract = os.path.join(spot_folder, 'GMT2_SpotComposite_Extract.tif')
composite_image = os.path.join(composite_folder, 'GMT2_Composite_AKALB.tif')

#### EXTRACT SPOT IMAGERY

# Create key word arguments
kwargs_extract = {'work_geodatabase': work_geodatabase,
                  'input_array': [gmt2_raster, spot_image, maxar_mask],
                  'output_array': [spot_extract]
                  }

# Extract raster
print('Extracting Spot-5 imagery...')
arcpy_geoprocessing(extract_raster, **kwargs_extract)
print('----------')

#### MERGE SEGMENTATION IMAGERY

# Create key word arguments
kwargs_merge = {'input_projection': 3338,
                'work_geodatabase': work_geodatabase,
                'input_array': [gmt2_raster, spot_extract, maxar_image],
                'output_array': [composite_image]
                }

# Merge segmentation imagery
print('Merging segmentation imagery...')
arcpy_geoprocessing(merge_segmentation_imagery, **kwargs_merge)
print('----------')
