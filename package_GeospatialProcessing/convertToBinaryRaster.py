# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Convert to binary raster
# Author: Timm Nawrocki
# Last Updated: 2022-12-08
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Convert to raster" is a function that converts polygons to a binary raster with an optional buffer.
# ---------------------------------------------------------------------------

# Define a function to convert to a binary presence-absence raster
def convert_to_binary_raster(**kwargs):
    """
    Description: converts polygons to raster with value 1 and value 0 in intervening space
    Inputs: 'buffer_distance' -- optional distance for the buffer, enter None for no buffer step
            'work_geodatabase' -- a geodatabase to store temporary results
            'input_array' -- an array containing the area raster and the input feature class
            'output_array' -- an array containing the output binary raster
    Returned Value: Returns a raster dataset on disk
    Preconditions: requires a manually-delineated or pre-existing feature class
    """

    # Import packages
    import os
    import arcpy
    from arcpy.sa import Con
    from arcpy.sa import ExtractByMask
    from arcpy.sa import IsNull
    from arcpy.sa import Raster
    import datetime
    import time

    # Parse key word argument inputs
    buffer_distance = kwargs['buffer_distance']
    work_geodatabase = kwargs['work_geodatabase']
    area_raster = kwargs['input_array'][0]
    input_feature = kwargs['input_array'][1]
    output_raster = kwargs['output_array'][0]

    # Define intermediate datasets
    buffer_feature = os.path.join(work_geodatabase, 'buffer_feature')
    dissolve_feature = os.path.join(work_geodatabase, 'dissolve_feature')
    feature_raster = os.path.join(os.path.split(output_raster)[0], 'feature_raster.tif')

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

    # Buffer feature class if buffer distance specified
    if buffer_distance != None:
        print(f'\tBuffer input feature {buffer_distance}...')
        iteration_start = time.time()
        arcpy.analysis.PairwiseBuffer(input_feature,
                                      buffer_feature,
                                      buffer_distance,
                                      'NONE',
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

    # Dissolve features
    if arcpy.Exists(buffer_feature) == 1:
        input_feature = buffer_feature
    print(f'\tDissolving feature...')
    iteration_start = time.time()
    arcpy.analysis.PairwiseDissolve(input_feature,
                                    dissolve_feature,
                                    '',
                                    '',
                                    'MULTI_PART')
    # End timing
    iteration_end = time.time()
    iteration_elapsed = int(iteration_end - iteration_start)
    iteration_success_time = datetime.datetime.now()
    # Report success
    print(
        f'\tCompleted at {iteration_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=iteration_elapsed)})')
    print('\t----------')

    # Convert to raster
    print(f'\tConverting feature to raster...')
    iteration_start = time.time()
    arcpy.conversion.PolygonToRaster(dissolve_feature,
                                     'OBJECTID',
                                     feature_raster,
                                     'CELL_CENTER',
                                     '',
                                     cell_size,
                                     'BUILD')
    # Change null values to zero
    full_raster = Con(IsNull(Raster(feature_raster)), 0, Raster(feature_raster))
    # Extract raster to study area
    extract_raster = ExtractByMask(full_raster, area_raster)
    # Export final raster
    arcpy.management.CopyRaster(extract_raster,
                                output_raster,
                                '',
                                '',
                                '-128',
                                'NONE',
                                'NONE',
                                '8_BIT_SIGNED',
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

    # Delete intermediate datasets
    if arcpy.Exists(buffer_feature) == 1:
        arcpy.management.Delete(buffer_feature)
    if arcpy.Exists(dissolve_feature) == 1:
        arcpy.management.Delete(dissolve_feature)
    if arcpy.Exists(feature_raster) == 1:
        arcpy.management.Delete(feature_raster)

    # Return success message
    outprocess = f'Successfully converted feature to binary raster.'
    return outprocess
