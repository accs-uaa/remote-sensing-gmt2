# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Distance from feature
# Author: Timm Nawrocki
# Last Updated: 2022-12-08
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Distance from feature" is a function that calculates euclidean distance from a feature class.
# ---------------------------------------------------------------------------

# Define a function to calculate Euclidean distance from a feature class
def distance_from_feature(**kwargs):
    """
    Description: calculates Euclidean distance from a feature class
    Inputs: 'work_geodatabase' -- a geodatabase to store temporary results
            'input_array' -- an array containing the area raster and the input feature class
            'output_array' -- an array containing the output distance raster
    Returned Value: Returns a raster dataset on disk
    Preconditions: requires a manually-delineated or pre-existing feature class
    """

    # Import packages
    import os
    import arcpy
    from arcpy.sa import EucDistance
    from arcpy.sa import ExtractByMask
    from arcpy.sa import IsNull
    from arcpy.sa import Raster
    import datetime
    import time

    # Parse key word argument inputs
    work_geodatabase = kwargs['work_geodatabase']
    area_raster = kwargs['input_array'][0]
    input_feature = kwargs['input_array'][1]
    output_raster = kwargs['output_array'][0]

    # Set overwrite option
    arcpy.env.overwriteOutput = True

    # Specify core usage
    arcpy.env.parallelProcessingFactor = '0'

    # Set workspace
    arcpy.env.workspace = work_geodatabase

    # Set snap raster and extent
    arcpy.env.snapRaster = area_raster
    arcpy.env.extent = Raster(area_raster).extent

    # Set output coordinate system
    arcpy.env.outputCoordinateSystem = Raster(area_raster)

    # Set cell size environment
    cell_size = arcpy.management.GetRasterProperties(area_raster, 'CELLSIZEX', '').getOutput(0)
    arcpy.env.cellSize = int(cell_size)

    # Calculate Euclidean distance
    print(f'\tCalculating distance...')
    iteration_start = time.time()
    euclidean_raster = EucDistance(input_feature,
                                   '',
                                   cell_size,
                                   '',
                                   'PLANAR')
    # End timing
    iteration_end = time.time()
    iteration_elapsed = int(iteration_end - iteration_start)
    iteration_success_time = datetime.datetime.now()
    # Report success
    print(
        f'\tCompleted at {iteration_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=iteration_elapsed)})')
    print('\t----------')

    # Extract to study area
    print(f'\tConverting feature to raster...')
    iteration_start = time.time()
    # Extract raster to study area
    extract_raster = ExtractByMask(euclidean_raster, area_raster)
    # Export final raster
    arcpy.management.CopyRaster(extract_raster,
                                output_raster,
                                '',
                                '',
                                '-2147483648',
                                'NONE',
                                'NONE',
                                '32_BIT_SIGNED',
                                'NONE',
                                'NONE',
                                'TIFF',
                                'NONE',
                                'CURRENT_SLICE',
                                'NO_TRANSPOSE')
    # End timing
    iteration_end = time.time()
    iteration_elapsed = int(iteration_end - iteration_start)
    iteration_success_time = datetime.datetime.now()
    # Report success
    print(
        f'\tCompleted at {iteration_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=iteration_elapsed)})')
    print('\t----------')

    # Return success message
    outprocess = f'Successfully calculated Euclidean distance.'
    return outprocess
