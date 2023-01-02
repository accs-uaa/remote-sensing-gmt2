# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Summarize to regions
# Author: Timm Nawrocki
# Last Updated: 2022-12-23
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Summarize to regions" is a function that summarizes a continuous raster to regions defined by a categorical raster.
# ---------------------------------------------------------------------------

# Define a function to summarize continuous rasters to categorical regions
def summarize_to_regions(**kwargs):
    """
    Description: summarizes a continuous raster to regions defined by a categorical raster
    Inputs: 'work_geodatabase' -- a geodatabase to store temporary results
            'input_array' -- an array containing the area raster (must be first), the continuous raster, and the categorical raster
            'output_array' -- an array containing the output raster
    Returned Value: Returns a raster to disk
    Preconditions: requires a continuous raster and categorical raster
    """

    # Import packages
    import arcpy
    from arcpy.sa import Int
    from arcpy.sa import Raster
    from arcpy.sa import RegionGroup
    from arcpy.sa import ZonalStatistics
    import datetime
    import time
    import os

    # Parse key word argument inputs
    work_geodatabase = kwargs['work_geodatabase']
    area_raster = kwargs['input_array'][0]
    continuous_raster = kwargs['input_array'][1]
    categorical_raster = kwargs['input_array'][2]
    output_raster = kwargs['output_array'][0]

    # Define intermediate datasets
    input_integer = os.path.join(os.path.split(categorical_raster)[0], 'integer.tif')

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

    # Calculate regions
    print(f'\tCalculating regions...')
    iteration_start = time.time()
    # Copy raster to integer
    arcpy.management.CopyRaster(categorical_raster,
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
    # Calculate regions
    raster_regions = RegionGroup(Raster(input_integer),
                                 'FOUR',
                                 'WITHIN',
                                 'NO_LINK')
    # End timing
    iteration_end = time.time()
    iteration_elapsed = int(iteration_end - iteration_start)
    iteration_success_time = datetime.datetime.now()
    # Report success
    print(
        f'\tCompleted at {iteration_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=iteration_elapsed)})')
    print('\t----------')

    # Summarize continuous raster to regions
    print(f'\tCalculating zonal statistics...')
    iteration_start = time.time()
    raster_statistics = ZonalStatistics(raster_regions,
                                        'VALUE',
                                        Raster(continuous_raster),
                                        'MEAN',
                                        'DATA',
                                        'CURRENT_SLICE')
    raster_int = Int(raster_statistics)
    # Export final raster
    arcpy.management.CopyRaster(raster_int,
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
    if arcpy.Exists(input_integer) == 1:
        arcpy.management.Delete(input_integer)

    # Return success message
    out_process = f'Successfully summarized continuous raster.'
    return out_process
