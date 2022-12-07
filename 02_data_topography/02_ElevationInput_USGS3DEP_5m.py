# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Create composite USGS 3DEP 5m
# Author: Timm Nawrocki
# Last Updated: 2022-02-20
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Create composite USGS 3DEP 5m" combines individual DEM tiles and reprojects to NAD 1983 Alaska Albers.
# ---------------------------------------------------------------------------

# Import packages
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import merge_elevation_tiles
import os

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')
topography_folder = os.path.join(project_folder, 'Data_Input/topography')
tile_folder = os.path.join(topography_folder, 'tiles')
projected_folder = os.path.join(topography_folder, 'tiles_projected')

# Define geodatabases
work_geodatabase = os.path.join(project_folder, 'GMT2_RemoteSensing.gdb')

# Define input datasets
gmt2_raster = os.path.join(project_folder, 'Data_Input/GMT2_StudyArea.tif')

# Define output datasets
output_raster = os.path.join(topography_folder, 'float/Elevation.tif')

#### CREATE COMPOSITE DEM

# Create key word arguments
kwargs_merge = {'tile_folder': tile_folder,
                'projected_folder': projected_folder,
                'workspace': work_geodatabase,
                'cell_size': 5,
                'input_projection': 3338,
                'output_projection': 3338,
                'geographic_transformation': '',
                'input_array': [gmt2_raster],
                'output_array': [output_raster]
                }

# Merge source tiles
arcpy_geoprocessing(merge_elevation_tiles, **kwargs_merge)
