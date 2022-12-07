# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Post-process image segments
# Author: Timm Nawrocki
# Last Updated: 2022-11-30
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Post-process image segments" converts the segment output from Google Earth Engine to a standard format raster, polygon, and point set.
# ---------------------------------------------------------------------------

# Import packages
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import postprocess_segments

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')
unprocessed_folder = os.path.join(project_folder, 'Data_Input/imagery/segments/unprocessed')
processed_folder = os.path.join(project_folder, 'Data_Input/imagery/segments/processed')

# Define geodatabases
work_geodatabase = os.path.join(project_folder, 'GMT2_RemoteSensing.gdb')

# Define input datasets
study_raster = os.path.join(project_folder, 'Data_Input/GMT2_StudyArea.tif')
segments_initial = os.path.join(unprocessed_folder, 'GMT2_Segments_Initial.tif')

# Define output datasets
segments_final = os.path.join(processed_folder, 'GMT2_Segments_Original.tif')
segments_polygon = os.path.join(work_geodatabase, 'GMT2_Segments_Original_Polygon')
segments_point = os.path.join(work_geodatabase, 'GMT2_Segments_Original_Point')

#### POST-PROCESS IMAGE SEGMENTS

# Create key word arguments
kwargs_process = {'cell_size': 2,
                  'work_geodatabase': work_geodatabase,
                  'input_array': [study_raster, segments_initial],
                  'output_array': [segments_final, segments_polygon, segments_point]
                  }

# Post-process segments
print('Post-processing image segments...')
arcpy_geoprocessing(postprocess_segments, **kwargs_process)
print('----------')
