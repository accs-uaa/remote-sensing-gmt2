# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Correct no data
# Author: Timm Nawrocki
# Last Updated: 2022-12-14
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Correct no data" is a function that corrects no data values by applying set null where less than a threshold.
# ---------------------------------------------------------------------------

# Define a function to correct no data
def correct_no_data(**kwargs):
    """
    Description: corrects no data values by setting null where less than a threshold
    Inputs: 'threshold' -- a numeric threshold to below which to set null
            'work_geodatabase' -- a geodatabase to store temporary results
            'input_array' -- an array containing the area raster, and the input raster
            'output_array' -- an array containing the output raster
    Returned Value: Returns a raster dataset on disk
    Preconditions: requires an input raster exported from Google Earth Engine or other source
    """

    # Import packages
    import arcpy
    from arcpy.sa import Raster
    from arcpy.sa import SetNull
    import datetime
    import time

    # Parse key word argument inputs
    threshold = kwargs['threshold']
    work_geodatabase = kwargs['work_geodatabase']
    area_raster = kwargs['input_array'][0]
    input_raster = kwargs['input_array'][1]
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

    # Set null where less than threshold
    print(f'\tCorrecting no data below values of {str(threshold)}...')
    iteration_start = time.time()
    null_raster = SetNull(Raster(input_raster) < threshold, Raster(input_raster))
    # Export raster as 32 bit float
    arcpy.management.CopyRaster(null_raster,
                                output_raster,
                                '',
                                '',
                                '-32764',
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

    # Return success message
    outprocess = f'Successfully corrected no data.'
    return outprocess