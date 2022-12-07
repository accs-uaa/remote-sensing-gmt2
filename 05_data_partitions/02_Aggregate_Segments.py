# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Aggregate segments
# Author: Timm Nawrocki
# Last Updated: 2022-12-06
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Aggregate segments" merges adjacent image segments that are within 0.05 threshold of NDVI and NDWI.
# ---------------------------------------------------------------------------

# Import packages
import arcpy
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import aggregate_segments

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')
imagery_folder = os.path.join(project_folder, 'Data_Input/imagery')
grid_folder = os.path.join(imagery_folder, 'segments/gridded')
aggregate_folder = os.path.join(imagery_folder, 'segments/aggregated')

# Define geodatabases
work_geodatabase = os.path.join(project_folder, 'GMT2_RemoteSensing.gdb')
segments_geodatabase = os.path.join(project_folder, 'GMT2_Segments_Aggregated.gdb')

# Define input datasets
ndvi_raster = os.path.join(imagery_folder, 'sentinel-2/growing_season/sent2_07_ndvi.tif')
ndwi_raster = os.path.join(imagery_folder, 'sentinel-2/growing_season/sent2_07_ndwi.tif')

# Define grids
grid_list = ['A4', 'A5', 'A6', 'A7',
             'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7',
             'C1', 'C2', 'C3', 'C4', 'C5', 'C6',
             'D1', 'D2', 'D3', 'D4', 'D5',
             'E1', 'E2', 'E3', 'E4', 'E5']

# Loop through each grid in grid list and produce zonal summaries
for grid in grid_list:
    print(f'Aggregating segments for grid {grid}...')

    # Define input grid raster
    grid_input = os.path.join(grid_folder, grid + '.tif')

    # Define output grid raster
    grid_output = os.path.join(aggregate_folder, grid + '.tif')

    # Define feature outputs
    grid_polygon = os.path.join(segments_geodatabase, 'polygon_' + grid)
    grid_point = os.path.join(segments_geodatabase, 'points_' + grid)

    # Create zonal summary if output raster does not already exist
    if arcpy.Exists(grid_output) == 0:
        # Create key word arguments
        kwargs_aggregate = {'zone_field': 'VALUE',
                            'work_geodatabase': work_geodatabase,
                            'input_array': [grid_input, ndvi_raster, ndwi_raster],
                            'output_array': [grid_polygon, grid_point, grid_output]
                            }

        # Process the zonal summaries
        print(f'\tAggregating segments for {grid}...')
        arcpy_geoprocessing(aggregate_segments, **kwargs_aggregate)
        print('\t----------')

    # If raster already exists, print message
    else:
        print(f'\tAggregated segments for {grid} already exist.')
        print('\t----------')
