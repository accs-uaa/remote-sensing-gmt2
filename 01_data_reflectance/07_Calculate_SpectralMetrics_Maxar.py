# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Calculate spectral metrics for Maxar imagery
# Author: Timm Nawrocki
# Last Updated: 2022-12-06
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Calculate spectral metrics" calculates normalized difference vegetation index, and normalized difference water index for the original resolution Maxar composite.
# ---------------------------------------------------------------------------

# Import packages
import arcpy
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import normalized_metrics

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')
imagery_folder = os.path.join(project_folder, 'Data_Input/imagery/maxar')
processed_folder = os.path.join(imagery_folder, 'processed')

# Define geodatabases
work_geodatabase = os.path.join(project_folder, 'GMT2_RemoteSensing.gdb')

# Define input datasets
study_raster = os.path.join(imagery_folder, 'composite/GMT2_MaxarComposite_WGS84.tif')
blue_raster = os.path.join(imagery_folder, 'composite/GMT2_MaxarComposite_WGS84.tif/Band_1')
green_raster = os.path.join(imagery_folder, 'composite/GMT2_MaxarComposite_WGS84.tif/Band_2')
red_raster = os.path.join(imagery_folder, 'composite/GMT2_MaxarComposite_WGS84.tif/Band_3')
nearir_raster = os.path.join(imagery_folder, 'composite/GMT2_MaxarComposite_WGS84.tif/Band_4')

# Define output datasets
ndvi_raster = os.path.join(processed_folder, 'GMT2_Maxar_NDVI.tif')
ndwi_raster = os.path.join(processed_folder, 'GMT2_Maxar_NDWI.tif')

# Define conversion factor
conversion_factor = 1000000

#### CALCULATE NDVI

if arcpy.Exists(ndvi_raster) == 0:
    # Create key word arguments
    kwargs_ndvi = {'metric_type': 'NORMALIZED',
                   'conversion_factor': conversion_factor,
                   'work_geodatabase': work_geodatabase,
                   'input_array': [study_raster, nearir_raster, red_raster],
                   'output_array': [ndvi_raster]
                   }

    # Calculate metric
    print(f'Calculate NDVI...')
    arcpy_geoprocessing(normalized_metrics, **kwargs_ndvi)
    print('----------')

else:
    print(f'NDVI raster already exists.')
    print('----------')

#### CALCULATE NDWI

if arcpy.Exists(ndwi_raster) == 0:
    # Create key word arguments
    kwargs_ndwi = {'metric_type': 'NORMALIZED',
                   'conversion_factor': conversion_factor,
                   'work_geodatabase': work_geodatabase,
                   'input_array': [study_raster, green_raster, nearir_raster],
                   'output_array': [ndwi_raster]
                   }

    # Calculate metric
    print(f'Calculate NDWI...')
    arcpy_geoprocessing(normalized_metrics, **kwargs_ndwi)
    print('----------')

else:
    print(f'NDWI raster already exists.')
    print('----------')
