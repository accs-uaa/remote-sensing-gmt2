# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Calculate spectral metrics
# Author: Timm Nawrocki
# Last Updated: 2022-11-30
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Calculate spectral metrics" calculates enhanced vegetation index-2, normalized difference vegetation index, and normalized difference water index.
# ---------------------------------------------------------------------------

# Import packages
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import normalized_metrics

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')
processed_folder = os.path.join(project_folder, 'Data_Input/imagery/composite/processed')

# Define geodatabases
work_geodatabase = os.path.join(project_folder, 'GMT2_RemoteSensing.gdb')

# Define input datasets
study_raster = os.path.join(project_folder, 'Data_Input/GMT2_StudyArea.tif')
blue_raster = os.path.join(processed_folder, 'GMT2_Comp_01_Blue.tif')
green_raster = os.path.join(processed_folder, 'GMT2_Comp_02_Green.tif')
red_raster = os.path.join(processed_folder, 'GMT2_Comp_03_Red.tif')
nearir_raster = os.path.join(processed_folder, 'GMT2_Comp_04_NearIR.tif')

# Define output datasets
evi2_raster = os.path.join(processed_folder, 'GMT2_Comp_EVI2.tif')
ndvi_raster = os.path.join(processed_folder, 'GMT2_Comp_NDVI.tif')
ndwi_raster = os.path.join(processed_folder, 'GMT2_Comp_NDWI.tif')

# Define conversion factor
conversion_factor = 1000000

#### CALCULATE EVI-2

# Create key word arguments
kwargs_evi2 = {'metric_type': 'EVI2',
               'conversion_factor': conversion_factor,
               'work_geodatabase': work_geodatabase,
               'input_array': [study_raster, red_raster, green_raster],
               'output_array': [evi2_raster]
               }

# Calculate metric
print(f'Calculate EVI2...')
arcpy_geoprocessing(normalized_metrics, **kwargs_evi2)
print('----------')

#### CALCULATE NDVI

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

#### CALCULATE EVI-2

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
