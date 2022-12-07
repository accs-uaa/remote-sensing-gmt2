# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Convert multi-band raster to single-band rasters
# Author: Timm Nawrocki
# Last Updated: 2022-11-30
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Convert multi-band raster to single-band rasters" converts a multi-band raster to single band rasters.
# ---------------------------------------------------------------------------

# Import packages
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import parse_raster_band

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')
composite_folder = os.path.join(project_folder, 'Data_Input/imagery/composite')
processed_folder = os.path.join(project_folder, 'Data_Input/imagery/composite/processed')

# Define geodatabases
work_geodatabase = os.path.join(project_folder, 'GMT2_RemoteSensing.gdb')

# Define input datasets
study_raster = os.path.join(project_folder, 'Data_Input/GMT2_StudyArea.tif')
composite_raster = os.path.join(composite_folder, 'GMT2_Composite_AKALB.tif')

# Define output rasters
blue_raster = os.path.join(processed_folder, 'GMT2_Comp_01_Blue.tif')
green_raster = os.path.join(processed_folder, 'GMT2_Comp_02_Green.tif')
red_raster = os.path.join(processed_folder, 'GMT2_Comp_03_Red.tif')
nearir_raster = os.path.join(processed_folder, 'GMT2_Comp_04_NearIR.tif')

# Define output list in band order
output_rasters = [blue_raster, green_raster, red_raster, nearir_raster]

# Export each band as a single band raster
count = 1
band_number = len(output_rasters)
while count <= band_number:
    # Create key word arguments
    kwargs_bands = {'band': count,
                    'work_geodatabase': work_geodatabase,
                    'input_array': [study_raster, composite_raster],
                    'output_array': [output_rasters[count-1]]
                    }

    # Parse band
    print(f'Parse raster band {count} of {band_number}...')
    arcpy_geoprocessing(parse_raster_band, **kwargs_bands)
    print('----------')

    # Increase count
    count += 1
