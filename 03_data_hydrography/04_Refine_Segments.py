# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Refine image segments
# Author: Timm Nawrocki
# Last Updated: 2022-11-30
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Refine image segments" divides segment polygons using floodplain and river boundary polygons.
# ---------------------------------------------------------------------------

# Import packages
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import splice_segments_floodplains

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')
segments_folder = os.path.join(project_folder, 'Data_Input/imagery/segments/processed')
hydrography_folder = os.path.join(project_folder, 'Data_Input/hydrography')

# Define geodatabases
work_geodatabase = os.path.join(project_folder, 'GMT2_RemoteSensing.gdb')

# Define input datasets
study_raster = os.path.join(project_folder, 'Data_Input/GMT2_StudyArea.tif')
segments_original = os.path.join(work_geodatabase, 'GMT2_Segments_Original_Polygon')
floodplain_raster = os.path.join(hydrography_folder, 'Floodplain.tif')
river_raster = os.path.join(hydrography_folder, 'River.tif')

# Define output datasets
segments_raster = os.path.join(segments_folder, 'GMT2_Segments_Revised.tif')
segments_final = os.path.join(work_geodatabase, 'GMT2_Segments_Revised_Polygon')
segments_point = os.path.join(work_geodatabase, 'GMT2_Segments_Revised_Point')

#### REFINE IMAGE SEGMENTS

# Create key word arguments
kwargs_refine = {'work_geodatabase': work_geodatabase,
                 'input_array': [study_raster, segments_original, floodplain_raster, river_raster],
                 'output_array': [segments_raster, segments_final, segments_point]
                 }

# Refine image segments
print('Refining image segments based on floodplain and river boundaries...')
arcpy_geoprocessing(splice_segments_floodplains, **kwargs_refine)
print('----------')
