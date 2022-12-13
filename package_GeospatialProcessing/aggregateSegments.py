# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Aggregate segments
# Author: Timm Nawrocki
# Last Updated: 2022-12-12
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Aggregate segments" is a function that aggregates segments based on thresholds of NDVI and NDWI.
# ---------------------------------------------------------------------------

# Define a function to aggregate segments
def aggregate_segments(**kwargs):
    """
    Description: aggregates segments based on thresholds on NDVI and NDWI
    Inputs: 'threshold' -- a numeric threshold to add to NDVI and NDWI to merge segments
            'zone_field' -- a string value of the field to use from the zone raster to define zones
            'work_geodatabase' -- a geodatabase to store temporary results
            'input_array' -- an array containing the zone raster, the ndvi raster raster, and the ndwi raster
            'output_array' -- an array containing the output segment polygon feature, point feature, and raster
    Returned Value: Returns a raster dataset on disk
    Preconditions: requires an input raster and zone raster from image segmentation that can be created through other scripts in this repository
    """

    # Import packages
    import arcpy
    from arcpy.sa import Combine
    from arcpy.sa import Int
    from arcpy.sa import Raster
    from arcpy.sa import ZonalStatistics
    import datetime
    import time

    # Parse key word argument inputs
    threshold = kwargs['threshold']
    zone_field = kwargs['zone_field']
    work_geodatabase = kwargs['work_geodatabase']
    zone_raster = kwargs['input_array'][0]
    ndvi_raster = kwargs['input_array'][1]
    ndwi_raster = kwargs['input_array'][2]
    output_polygon = kwargs['output_array'][0]
    output_points = kwargs['output_array'][1]
    output_raster = kwargs['output_array'][2]

    # Set overwrite option
    arcpy.env.overwriteOutput = True

    # Specify core usage
    arcpy.env.parallelProcessingFactor = '0'

    # Set workspace
    arcpy.env.workspace = work_geodatabase

    # Set snap raster and extent
    arcpy.env.snapRaster = zone_raster
    arcpy.env.extent = Raster(zone_raster).extent

    # Set output coordinate system
    arcpy.env.outputCoordinateSystem = Raster(zone_raster)

    # Set cell size environment
    cell_size = arcpy.management.GetRasterProperties(zone_raster, 'CELLSIZEX', '').getOutput(0)
    arcpy.env.cellSize = int(cell_size)

    # Determine zone raster value type
    value_number = arcpy.management.GetRasterProperties(zone_raster, "VALUETYPE").getOutput(0)
    no_data_value = arcpy.Describe(zone_raster).noDataValue
    value_dictionary = {
        0: '1_BIT',
        1: '2_BIT',
        2: '4_BIT',
        3: '8_BIT_UNSIGNED',
        4: '8_BIT_SIGNED',
        5: '16_BIT_UNSIGNED',
        6: '16_BIT_SIGNED',
        7: '32_BIT_UNSIGNED',
        8: '32_BIT_SIGNED',
        9: '32_BIT_FLOAT',
        10: '64_BIT'
    }
    value_type = value_dictionary.get(int(value_number))
    print(f'\t\tOutput data type will be {value_type}.')
    print(f'\t\tOutput no data value will be {no_data_value}.')
    print('\t\t----------')

    # Calculate zonal statistics for NDVI
    print(f'\t\tCalculating zonal NDVI...')
    iteration_start = time.time()
    ndvi_zonal = ZonalStatistics(zone_raster,
                                 zone_field,
                                 ndvi_raster,
                                 'MEAN',
                                 'DATA',
                                 'CURRENT_SLICE',
                                 '',
                                 '')
    ndvi_threshold = Int((ndvi_zonal + threshold) * 10)
    # End timing
    iteration_end = time.time()
    iteration_elapsed = int(iteration_end - iteration_start)
    iteration_success_time = datetime.datetime.now()
    # Report success
    print(
        f'\t\tCompleted at {iteration_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=iteration_elapsed)})')
    print('\t\t----------')

    # Calculate zonal statistics for NDWI
    print(f'\t\tCalculating zonal NDWI...')
    iteration_start = time.time()
    ndwi_zonal = ZonalStatistics(zone_raster,
                                 zone_field,
                                 ndwi_raster,
                                 'MEAN',
                                 'DATA',
                                 'CURRENT_SLICE',
                                 '',
                                 '')
    ndwi_threshold = Int((ndwi_zonal + threshold) * 10)
    # End timing
    iteration_end = time.time()
    iteration_elapsed = int(iteration_end - iteration_start)
    iteration_success_time = datetime.datetime.now()
    # Report success
    print(
        f'\t\tCompleted at {iteration_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=iteration_elapsed)})')
    print('\t\t----------')

    # Combine NDVI and NDWI
    print(f'\t\tCombining thresholded NDVI and NDWI...')
    iteration_start = time.time()
    combine_raster = Combine([ndvi_threshold, ndwi_threshold])
    # Convert to polygon and add attributes
    print(f'\t\tConverting to polygon...')
    arcpy.conversion.RasterToPolygon(combine_raster,
                                     output_polygon,
                                     'NO_SIMPLIFY',
                                     'VALUE',
                                     'SINGLE_OUTER_PART')
    arcpy.management.DeleteField(output_polygon,
                                 ['Id', 'gridcode'],
                                 'DELETE_FIELDS')
    arcpy.management.CalculateField(output_polygon,
                                    'shape_m',
                                    '!SHAPE.length!',
                                    'PYTHON3')
    arcpy.management.CalculateField(output_polygon,
                                    'shape_m2',
                                    '!SHAPE.area!',
                                    'PYTHON3')
    arcpy.management.CalculateField(output_polygon,
                                    'segment_id',
                                    '!OBJECTID!',
                                    'PYTHON3')
    print(f'\t\tConverting to point...')
    # Convert to points with shape attributes and coordinates
    arcpy.management.FeatureToPoint(output_polygon,
                                    output_points,
                                    'INSIDE')
    arcpy.management.DeleteField(output_points,
                                 ['ORIG_FID'],
                                 'DELETE_FIELDS')
    arcpy.management.AddXY(output_points)
    print(f'\t\tConverting to raster...')
    arcpy.conversion.PolygonToRaster(output_polygon,
                                     'OBJECTID',
                                     output_raster,
                                     'CELL_CENTER')
    # End timing
    iteration_end = time.time()
    iteration_elapsed = int(iteration_end - iteration_start)
    iteration_success_time = datetime.datetime.now()
    # Report success
    print(
        f'\t\tCompleted at {iteration_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=iteration_elapsed)})')
    print('\t\t----------')

    # Return success message
    outprocess = f'\tSuccessfully created segments.'
    return outprocess
