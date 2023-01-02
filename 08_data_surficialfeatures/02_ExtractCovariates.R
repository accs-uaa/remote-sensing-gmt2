# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Extract covariates to points
# Author: Timm Nawrocki
# Last Updated: 2022-12-20
# Usage: Must be executed in R 4.0.0+.
# Description: "Extract covariates to points" extracts data from rasters to points.
# ---------------------------------------------------------------------------

# Set root directory
drive = 'N:'
root_folder = 'ACCS_Work'

# Define input folders
project_folder = paste(drive,
                       root_folder,
                       'Projects/VegetationEcology/BLM_AIM/GMT-2/Data',
                       sep = '/')
zonal_folder = paste(project_folder,
                     'Data_Input/zonal_revised',
                     sep = '/')

# Define output folders
output_folder = paste(training_folder,
                      'table_revised',
                      sep = '/')

# Define segments geodatabase
segments_geodatabase = paste(project_folder,
                             'GMT2_Segments_Gridded.gdb',
                             sep = '/')

# Define grids
grid_list = c('A4', 'A5', 'A6', 'A7',
              'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7',
              'C1', 'C2', 'C3', 'C4', 'C5', 'C6',
              'D1', 'D2', 'D3', 'D4', 'D5',
              'E1', 'E2', 'E3', 'E4', 'E5')
grid_length = length(grid_list)

# Import libraries
library(dplyr)
library(raster)
library(sf)
library(stringr)

# Set count
count = 1

# Loop through each grid and extract covariates
for (grid in grid_list) {
  # Define input points
  input_points = paste('points_', grid, sep = '')
  
  # Define output table
  output_file = paste(output_folder, '/', grid, '.csv', sep = '')
  
  # Define zonal data
  zonal_data = paste(zonal_folder, grid, sep = '/')
  
  # Create output table if it does not already exist
  if (!file.exists(output_file)) {
    print(paste('Extracting segments ', toString(count), ' out of ', toString(grid_length), '...', sep=''))
    
    # Create a list of zonal predictor rasters
    predictors_zonal = list.files(zonal_data, pattern = 'tif$', full.names = TRUE)
    print(paste('Number of predictor rasters: ', length(predictors_zonal), sep = ''))
    
    # Generate a stack of zonal predictor rasters
    print('Creating zonal raster stack...')
    start = proc.time()
    predictor_stack = stack(predictors_zonal)
    end = proc.time() - start
    print(end[3])
    
    # Read path data and extract covariates
    print('Extracting covariates...')
    start = proc.time()
    print(input_points)
    point_data = st_read(dsn = segments_geodatabase, layer = input_points)
    point_zonal = data.frame(point_data, raster::extract(predictor_stack, point_data))
    end = proc.time() - start
    print(end[3])
    
    # Convert field names to standard
    point_zonal = point_zonal %>%
      dplyr::rename(top_aspect = Aspect,
                    top_elevation = Elevation,
                    top_exposure = Exposure,
                    top_heat_load = HeatLoad,
                    top_position = Position,
                    top_radiation = Radiation,
                    top_roughness = Roughness,
                    top_slope = Slope,
                    top_surface_area = SurfaceArea,
                    top_surface_relief = SurfaceRelief,
                    top_wetness = Wetness,
                    hyd_river_position = River_Position,
                    hyd_stream_position = Stream_Position,
                    hyd_streams = Streams,
                    hyd_stream_dist = Stream_Distance,
                    hyd_seasonal_water = GMT2_SeasonalWater_Percentage,
                    hyd_estuary_dist = Estuary_Distance,
                    inf_developed = Infrastructure_Developed,
                    inf_pipeline = Infrastructure_Pipelines,
                    comp_01_blue = GMT2_Comp_01_Blue,
                    comp_01_blue_std = GMT2_Comp_01_Blue_STD,
                    comp_02_green = GMT2_Comp_02_Green,
                    comp_02_green_std = GMT2_Comp_02_Green_STD,
                    comp_03_red = GMT2_Comp_03_Red,
                    comp_03_red_std = GMT2_Comp_03_Red_STD,
                    comp_04_nearir = GMT2_Comp_04_NearIR,
                    comp_04_nearir_std = GMT2_Comp_04_NearIR_STD,
                    comp_evi2 = GMT2_Comp_EVI2,
                    comp_evi2_std = GMT2_Comp_EVI2_STD,
                    comp_ndvi = GMT2_Comp_NDVI,
                    comp_ndvi_std = GMT2_Comp_NDVI_STD,
                    comp_ndwi = GMT2_Comp_NDWI,
                    comp_ndwi_std = GMT2_Comp_NDWI_STD,
                    maxar_ndvi_std = GMT2_Maxar_NDVI_STD,
                    maxar_ndvi_rng = GMT2_Maxar_NDVI_RNG,
                    maxar_ndwi_std = GMT2_Maxar_NDWI_STD,
                    maxar_ndwi_rng = GMT2_Maxar_NDWI_RNG,
                    s1_vh = Sent1_vh,
                    s1_vv = Sent1_vv,
                    s2_06_02_blue = Sent2_06_2_blue,
                    s2_06_03_green = Sent2_06_3_green,
                    s2_06_04_red = Sent2_06_4_red,
                    s2_06_05_rededge1 = Sent2_06_5_redEdge1,
                    s2_06_06_rededge2 = Sent2_06_6_redEdge2,
                    s2_06_07_rededge3 = Sent2_06_7_redEdge3,
                    s2_06_08_nearir = Sent2_06_8_nearInfrared,
                    s2_06_08a_rededge4 = Sent2_06_8a_redEdge4,
                    s2_06_11_shortir1 = Sent2_06_11_shortInfrared1,
                    s2_06_12_shortir2 = Sent2_06_12_shortInfrared2,
                    s2_06_evi2 = Sent2_06_evi2,
                    s2_06_nbr = Sent2_06_nbr,
                    s2_06_ndmi = Sent2_06_ndmi,
                    s2_06_ndsi = Sent2_06_ndsi,
                    s2_06_ndvi = Sent2_06_ndvi,
                    s2_06_ndwi = Sent2_06_ndwi,
                    s2_07_02_blue = Sent2_07_2_blue,
                    s2_07_03_green = Sent2_07_3_green,
                    s2_07_04_red = Sent2_07_4_red,
                    s2_07_05_rededge1 = Sent2_07_5_redEdge1,
                    s2_07_06_rededge2 = Sent2_07_6_redEdge2,
                    s2_07_07_rededge3 = Sent2_07_7_redEdge3,
                    s2_07_08_nearir = Sent2_07_8_nearInfrared,
                    s2_07_08a_rededge4 = Sent2_07_8a_redEdge4,
                    s2_07_11_shortir1 = Sent2_07_11_shortInfrared1,
                    s2_07_12_shortir2 = Sent2_07_12_shortInfrared2,
                    s2_07_evi2 = Sent2_07_evi2,
                    s2_07_nbr = Sent2_07_nbr,
                    s2_07_ndmi = Sent2_07_ndmi,
                    s2_07_ndsi = Sent2_07_ndsi,
                    s2_07_ndvi = Sent2_07_ndvi,
                    s2_07_ndwi = Sent2_07_ndwi,
                    s2_08_02_blue = Sent2_08_2_blue,
                    s2_08_03_green = Sent2_08_3_green,
                    s2_08_04_red = Sent2_08_4_red,
                    s2_08_05_rededge1 = Sent2_08_5_redEdge1,
                    s2_08_06_rededge2 = Sent2_08_6_redEdge2,
                    s2_08_07_rededge3 = Sent2_08_7_redEdge3,
                    s2_08_08_nearir = Sent2_08_8_nearInfrared,
                    s2_08_08a_rededge4 = Sent2_08_8a_redEdge4,
                    s2_08_11_shortir1 = Sent2_08_11_shortInfrared1,
                    s2_08_12_shortir2 = Sent2_08_12_shortInfrared2,
                    s2_08_evi2 = Sent2_08_evi2,
                    s2_08_nbr = Sent2_08_nbr,
                    s2_08_ndmi = Sent2_08_ndmi,
                    s2_08_ndsi = Sent2_08_ndsi,
                    s2_08_ndvi = Sent2_08_ndvi,
                    s2_08_ndwi = Sent2_08_ndwi,
                    s2_09_02_blue = Sent2_09_2_blue,
                    s2_09_03_green = Sent2_09_3_green,
                    s2_09_04_red = Sent2_09_4_red,
                    s2_09_05_rededge1 = Sent2_09_5_redEdge1,
                    s2_09_06_rededge2 = Sent2_09_6_redEdge2,
                    s2_09_07_rededge3 = Sent2_09_7_redEdge3,
                    s2_09_08_nearir = Sent2_09_8_nearInfrared,
                    s2_09_08a_rededge4 = Sent2_09_8a_redEdge4,
                    s2_09_11_shortir1 = Sent2_09_11_shortInfrared1,
                    s2_09_12_shortir2 = Sent2_09_12_shortInfrared2,
                    s2_09_evi2 = Sent2_09_evi2,
                    s2_09_nbr = Sent2_09_nbr,
                    s2_09_ndmi = Sent2_09_ndmi,
                    s2_09_ndsi = Sent2_09_ndsi,
                    s2_09_ndvi = Sent2_09_ndvi,
                    s2_09_ndwi = Sent2_09_ndwi,
                    foliar_forb = ABoVE_PFT_Top_Cover_Forb_2020,
                    foliar_graminoid = ABoVE_PFT_Top_Cover_Graminoid_2020,
                    foliar_lichen = ABoVE_PFT_Top_Cover_tmLichenLight_2020,
                    foliar_alnus = NorthAmericanBeringia_alnus_A6,
                    foliar_betshr = NorthAmericanBeringia_betshr_A6,
                    foliar_dryas = NorthAmericanBeringia_dryas_A6,
                    foliar_empnig = NorthAmericanBeringia_empnig_A6,
                    foliar_erivag = NorthAmericanBeringia_erivag_A6,
                    foliar_rhoshr = NorthAmericanBeringia_rhoshr_A6,
                    foliar_salshr = NorthAmericanBeringia_salshr_A6,
                    foliar_sphagn = NorthAmericanBeringia_sphagn_A6,
                    foliar_vaculi = NorthAmericanBeringia_vaculi_A6,
                    foliar_vacvit = NorthAmericanBeringia_vacvit_A6,
                    foliar_wetsed = NorthAmericanBeringia_wetsed_A6)
    
    # Export data as a csv
    st_write(point_zonal, output_file, coords = FALSE)
    print(paste('Extraction iteration ', toString(count), ' out of ', toString(grid_length), ' completed.', sep=''))
    print('----------')
  } else {
    # Report that output already exists
    print(paste('Extraction ', toString(count), ' out of ', toString(grid_length), ' already exists.', sep = ''))
    print('----------')
  }
  # Increase count
  count = count + 1
}
