# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Create 500 m sampling grid and points
# Author: Timm Nawrocki
# Last Updated: 2022-12-14
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Create 500 m sampling grid and points" creates a 500 m sampling grid for processing MODIS-derived 500 m data.
# ---------------------------------------------------------------------------

# Import packages
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import create_sampling_grid
import os

# Set root directory
drive = 'N:/'
root_folder = os.path.join(drive, 'ACCS_Work')

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')

# Define geodatabases
project_geodatabase = os.path.join(project_folder, 'GMT2_RemoteSensing.gdb')
work_geodatabase = os.path.join(project_folder, 'GMT2_Workspace.gdb')

# Define input datasets
study_raster = os.path.join(project_folder, 'Data_Input/GMT2_StudyArea.tif')
snap_raster = os.path.join(project_folder, 'Data_Input/imagery/modis_phenology/unprocessed',
                           'MCD12Q2006_2001_01_midgreenup.tif')

# Define output grid datasets
sampling_grid = os.path.join(project_folder, 'Data_Input/validation', 'MODIS_SamplingGrid_500m.tif')
sampling_points = os.path.join(project_geodatabase, 'MODIS_SamplingGrid_500m_Points')

# Create key word arguments for the validation grid index
kwargs_sampling = {'work_geodatabase': work_geodatabase,
                   'input_array': [study_raster, snap_raster],
                   'output_array': [sampling_grid, sampling_points]
                   }

# Create the validation grid index
print('Creating 500 m sampling grid and points...')
arcpy_geoprocessing(create_sampling_grid, **kwargs_sampling)
print('----------')
