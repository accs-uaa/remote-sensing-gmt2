# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Post-process categorical rasters
# Author: Timm Nawrocki
# Last Updated: 2022-12-27
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Post-process categorical rasters" is a function that generalizes a predicted raster, applies a minimum mapping unit, and adds manually delineated classes.
# ---------------------------------------------------------------------------

# Define a function to post-process categorical raster
def postprocess_categorical_raster(**kwargs):
    """
    Description: generalizes categorical raster to minimum mapping unit and adds classes
    Inputs: 'minimum_count' -- the number of cells to be used as the minimum size for adjacent cells of a same value to be retained
            'stream_value' -- integer value to use for stream corridors
            'water_value' -- integer value to use for water
            'pipeline_value' -- integer value to use for pipelines
            'infrastructure_value' -- integer value to use for infrastructure
            'conditional_statement' -- a statement of values to select for proximity to pipeline and infrastructure
            'attribute_dictionary' -- a dictionary of name and value pairs for the map schema
            'work_geodatabase' -- a geodatabase to store temporary results
            'input_array' -- an array containing the area raster (must be first), the predicted raster, the infrastructure feature class, the infrastructure raster, the segments feature class, the pipeline raster, and the stream raster
            'output_array' -- an array containing the output raster
    Returned Value: Returns a raster to disk
    Preconditions: requires a predicted categorical raster
    """

    # Import packages
    import arcpy
    from arcpy.sa import BoundaryClean
    from arcpy.sa import Con
    from arcpy.sa import ExtractByAttributes
    from arcpy.sa import IsNull
    from arcpy.sa import MajorityFilter
    from arcpy.sa import Nibble
    from arcpy.sa import Raster
    from arcpy.sa import RegionGroup
    from arcpy.sa import SetNull
    from arcpy.sa import ZonalStatistics
    import datetime
    import os
    import time

    # Parse key word argument inputs
    minimum_count = kwargs['minimum_count']
    stream_value = kwargs['stream_value']
    water_value = kwargs['water_value']
    pipelines_value = kwargs['pipeline_value']
    infrastructure_value = kwargs['infrastructure_value']
    conditional_statement = kwargs['conditional_statement']
    attribute_dictionary = kwargs['attribute_dictionary']
    work_geodatabase = kwargs['work_geodatabase']
    area_raster = kwargs['input_array'][0]
    input_raster = kwargs['input_array'][1]
    infrastructure_feature = kwargs['input_array'][2]
    infrastructure_raster = kwargs['input_array'][3]
    segments_feature = kwargs['input_array'][4]
    pipeline_raster = kwargs['input_array'][5]
    stream_raster = kwargs['input_array'][6]
    output_raster = kwargs['output_array'][0]

    # Define work folder
    work_folder = os.path.split(input_raster)[0]
    infrastructure_folder = os.path.join(os.path.split(pipeline_raster)[0], 'zonal')
    if os.path.exists(infrastructure_folder) == 0:
        os.mkdir(infrastructure_folder)

    # Define intermediate datasets
    infrastructure_buffer = os.path.join(work_geodatabase, 'infrastructure_developed_buffer_50m')
    infrastructure_buffer_raster = os.path.join(infrastructure_folder, 'infrastructure_developed_raster.tif')
    infrastructure_zonal = os.path.join(infrastructure_folder, 'zonal_developed.tif')
    pipeline_zonal = os.path.join(infrastructure_folder, 'zonal_pipelines.tif')
    input_integer = os.path.join(work_folder, 'integer.tif')

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

    # Prepare infrastructure data
    if arcpy.Exists(infrastructure_zonal) == 0:
        print(f'\tPreparing infrastructure data...')
        iteration_start = time.time()
        # Buffer infrastructure by 50 m
        arcpy.analysis.PairwiseBuffer(infrastructure_feature,
                                      infrastructure_buffer,
                                      '50 Meters',
                                      'ALL',
                                      '',
                                      'PLANAR')
        # Convert infrastructure to raster
        arcpy.conversion.PolygonToRaster(infrastructure_buffer,
                                         'OBJECTID',
                                         infrastructure_buffer_raster,
                                         'CELL_CENTER',
                                         '',
                                         cell_size,
                                         'BUILD')
        # Set NoData to 0
        infrastructure_binary = Con(IsNull(Raster(infrastructure_buffer_raster)), 0, Raster(infrastructure_buffer_raster))
        # Calculate zonal statistics on infrastructure raster
        infrastructure_statistics = ZonalStatistics(segments_feature,
                                                    'OBJECTID',
                                                    infrastructure_binary,
                                                    'MEAN',
                                                    'DATA',
                                                    'CURRENT_SLICE')
        # Export statistics raster
        arcpy.management.CopyRaster(infrastructure_statistics,
                                    infrastructure_zonal,
                                    '',
                                    '',
                                    '-1',
                                    'NONE',
                                    'NONE',
                                    '32_BIT_FLOAT',
                                    'NONE',
                                    'NONE',
                                    'TIFF',
                                    'NONE',
                                    'CURRENT_SLICE',
                                    'NO_TRANSPOSE')
        # Delete intermediate datasets
        if arcpy.Exists(infrastructure_buffer) == 1:
            arcpy.management.Delete(infrastructure_buffer)
        if arcpy.Exists(infrastructure_buffer_raster) == 1:
            arcpy.management.Delete(infrastructure_buffer_raster)
        # End timing
        iteration_end = time.time()
        iteration_elapsed = int(iteration_end - iteration_start)
        iteration_success_time = datetime.datetime.now()
        # Report success
        print(
            f'\tCompleted at {iteration_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=iteration_elapsed)})')
        print('\t----------')

    # Prepare pipeline data
    if arcpy.Exists(pipeline_zonal) == 0:
        print(f'\tPreparing pipeline data...')
        iteration_start = time.time()
        # Calculate zonal statistics on pipeline raster
        pipeline_statistics = ZonalStatistics(segments_feature,
                                              'OBJECTID',
                                              Raster(pipeline_raster),
                                              'MEAN',
                                              'DATA',
                                              'CURRENT_SLICE')
        # Export statistics raster
        arcpy.management.CopyRaster(pipeline_statistics,
                                    pipeline_zonal,
                                    '',
                                    '',
                                    '-1',
                                    'NONE',
                                    'NONE',
                                    '32_BIT_FLOAT',
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

    # Generalize raster results
    print(f'\tGeneralizing predicted raster...')
    iteration_start = time.time()
    # Copy raster to integer
    print('\t\tConverting input raster to integers...')
    arcpy.management.CopyRaster(input_raster,
                                input_integer,
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
    arcpy.management.CalculateStatistics(input_integer)
    arcpy.management.BuildRasterAttributeTable(input_integer, 'Overwrite')
    # Clean raster boundaries
    print('\t\tCleaning raster boundaries...')
    raster_boundary = BoundaryClean(input_integer,
                                    'DESCEND',
                                    'TWO_WAY')
    # Apply majority filter
    print('\t\tSmoothing raster edges...')
    raster_majority = MajorityFilter(raster_boundary,
                                     'EIGHT',
                                     'MAJORITY')
    # End timing
    iteration_end = time.time()
    iteration_elapsed = int(iteration_end - iteration_start)
    iteration_success_time = datetime.datetime.now()
    # Report success
    print(
        f'\tCompleted at {iteration_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=iteration_elapsed)})')
    print('\t----------')

    # Calculate regions
    print(f'\tCalculating regions...')
    iteration_start = time.time()
    # Create conditional raster for sensitivity to pipelines and infrastructure
    proximity_raster = Con(raster_majority, 1, 0, conditional_statement)
    # Set null where infrastructure has contaminated predictions
    print('\t\tRemoving infrastructure errors...')
    raster_remove_1 = SetNull((Raster(infrastructure_zonal) > 0) & (proximity_raster == 1),
                              raster_majority)
    # Set null where pipelines have contaminated predictions
    print('\t\tRemoving pipeline errors...')
    raster_remove_2 = SetNull((Raster(pipeline_zonal) > 0) & (proximity_raster == 1),
                              raster_remove_1)
    # Calculate regions
    print('\t\tCalculating contiguous value areas...')
    raster_regions = RegionGroup(raster_remove_2,
                                 'FOUR',
                                 'WITHIN',
                                 'NO_LINK',
                                 f'{water_value}')
    # End timing
    iteration_end = time.time()
    iteration_elapsed = int(iteration_end - iteration_start)
    iteration_success_time = datetime.datetime.now()
    # Report success
    print(
        f'\tCompleted at {iteration_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=iteration_elapsed)})')
    print('\t----------')

    # Create nibble mask
    print(f'\tCreating mask raster of removed zones...')
    iteration_start = time.time()
    # Remove zones below minimum mapping unit
    print('\t\tRemoving contiguous areas below minimum mapping unit...')
    criteria = f'COUNT > {minimum_count}'
    raster_mask_1 = ExtractByAttributes(raster_regions,
                                        criteria)
    # Set null for water
    raster_mask = SetNull(raster_mask_1 == 0, raster_mask_1)
    # End timing
    iteration_end = time.time()
    iteration_elapsed = int(iteration_end - iteration_start)
    iteration_success_time = datetime.datetime.now()
    # Report success
    print(
        f'\tCompleted at {iteration_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=iteration_elapsed)})')
    print('\t----------')

    # Replace removed data
    print(f'\tReplacing removed data...')
    iteration_start = time.time()
    # Nibble raster
    raster_nibble = Nibble(raster_majority,
                           raster_mask,
                           'ALL_VALUES',
                           'PRESERVE_NODATA')
    # End timing
    iteration_end = time.time()
    iteration_elapsed = int(iteration_end - iteration_start)
    iteration_success_time = datetime.datetime.now()
    # Report success
    print(
        f'\tCompleted at {iteration_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=iteration_elapsed)})')
    print('\t----------')

    # Add missing values for water, infrastructure, pipelines, and stream corridors
    print(f'\tAdding missing values...')
    iteration_start = time.time()
    # Add stream corridors
    raster_modified_1 = Con(Raster(stream_raster) > 0, stream_value, raster_nibble)
    # Add water
    raster_modified_2 = Con(raster_majority == water_value, water_value, raster_modified_1)
    # Add pipelines
    raster_modified_3 = Con(Raster(pipeline_raster) > 0, pipelines_value, raster_modified_2)
    # Add infrastructure
    raster_modified_4 = Con(Raster(infrastructure_raster) > 0, infrastructure_value, raster_modified_3)
    # End timing
    iteration_end = time.time()
    iteration_elapsed = int(iteration_end - iteration_start)
    iteration_success_time = datetime.datetime.now()
    # Report success
    print(
        f'\tCompleted at {iteration_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=iteration_elapsed)})')
    print('\t----------')

    # Export final raster
    print(f'\tExporting final raster...')
    iteration_start = time.time()
    # Export extracted raster
    arcpy.management.CopyRaster(raster_modified_4,
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
    # Create raster attribute table
    arcpy.management.BuildRasterAttributeTable(output_raster, 'Overwrite')
    # Calculate attribute label field
    code_block = '''def get_label(value, dictionary):
        for label, id in dictionary.items():
            if value == id:
                return label'''
    expression = f'get_label(!VALUE!, {attribute_dictionary})'
    arcpy.management.CalculateField(output_raster,
                                    'label',
                                    expression,
                                    'PYTHON3',
                                    code_block)
    # End timing
    iteration_end = time.time()
    iteration_elapsed = int(iteration_end - iteration_start)
    iteration_success_time = datetime.datetime.now()
    # Report success
    print(
        f'\tCompleted at {iteration_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=iteration_elapsed)})')
    print('\t----------')

    # Delete intermediate datasets
    if arcpy.Exists(input_integer) == 1:
        arcpy.management.Delete(input_integer)

    # Return success message
    out_process = f'Successfully post-processed categorical raster.'
    return out_process
