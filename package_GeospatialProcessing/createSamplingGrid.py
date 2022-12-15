# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Create sampling grid
# Author: Timm Nawrocki
# Last Updated: 2022-12-14
# Usage: Must be executed in an ArcGIS Pro Python 3.6+ installation.
# Description: "Create sampling grid" is a function that generates a sampling raster grid at a resolution based off a provided snap raster and creates an accompanying point representation.
# ---------------------------------------------------------------------------

# Define a function to generate a sampling grid
def create_sampling_grid(**kwargs):
    """
    Description: creates a raster and point feature class sampling grid
    Inputs: 'work_geodatabase' -- path to a file geodatabase that will serve as the workspace
            'input_array' -- an array containing the study
            'output_array' -- an array containing the output polygon feature class
    Returned Value: Returns raster and point feature class
    Preconditions: requires a snap raster that includes the target raster cell size
    """

    # Import packages
    import arcpy
    from arcpy.sa import ExtractByMask
    from arcpy.sa import Raster
    import datetime
    import os
    import time

    # Parse key word argument inputs
    work_geodatabase = kwargs['work_geodatabase']
    area_raster = kwargs['input_array'][0]
    snap_raster = kwargs['input_array'][1]
    output_raster = kwargs['output_array'][0]
    output_points = kwargs['output_array'][1]

    # Set overwrite option
    arcpy.env.overwriteOutput = True

    # Specify core usage
    arcpy.env.parallelProcessingFactor = '0'

    # Set workspace
    arcpy.env.workspace = work_geodatabase

    # Set snap raster and extent
    arcpy.env.snapRaster = snap_raster
    arcpy.env.extent = Raster(area_raster).extent

    # Set output coordinate system
    arcpy.env.outputCoordinateSystem = Raster(area_raster)

    # Set cell size environment
    cell_size = arcpy.management.GetRasterProperties(snap_raster, 'CELLSIZEX', '').getOutput(0)
    arcpy.env.cellSize = int(cell_size)

    # Define intermediate datasets
    buffer_feature = os.path.join(work_geodatabase, 'buffer_feature')

    # Extract raster to study area
    print(f'\tExtracting snap raster...')
    iteration_start = time.time()
    extract_raster = ExtractByMask(snap_raster, area_raster)
    # Convert raster to points
    arcpy.conversion.RasterToPoint(extract_raster,
                                   output_points,
                                   'VALUE')
    arcpy.management.DeleteField(output_points, ['pointid', 'grid_code'], 'DELETE_FIELDS')
    arcpy.management.AddXY(output_points)
    # Convert to raster
    arcpy.conversion.PointToRaster(output_points,
                                   'OBJECTID',
                                   output_raster,
                                   'MAXIMUM',
                                   '',
                                   cell_size,
                                   'BUILD')
    # End timing
    iteration_end = time.time()
    iteration_elapsed = int(iteration_end - iteration_start)
    iteration_success_time = datetime.datetime.now()
    # Report success
    print(
        f'\t\tCompleted at {iteration_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=iteration_elapsed)})')
    print('\t\t----------')

    # Return success message
    outprocess = f'\tSuccessfully created sampling grid.'
    return outprocess