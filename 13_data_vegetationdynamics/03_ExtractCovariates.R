# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Extract covariates to points
# Author: Timm Nawrocki
# Last Updated: 2022-12-15
# Usage: Must be executed in R 4.0.0+.
# Description: "Extract covariates to points" extracts data from rasters to MODIS sample grid points.
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
                     'Data_Input/vegetation_dynamics/zonal',
                     sep = '/')

# Define output folders
output_folder = paste(project_folder,
                      'Data_Input/vegetation_dynamics/table',
                      sep = '/')

# Define input data
project_geodatabase = paste(project_folder,
                            'GMT2_RemoteSensing.gdb',
                            sep = '/')
sample_points = 'MODIS_SamplingGrid_500m_Points'

# Define output data
output_file = paste(output_folder, 'MODIS_SamplingGrid_Extracted.csv', sep = '/')

# Import required libraries for geospatial processing: dplyr, raster, rgdal, sp, and stringr.
library(dplyr)
library(raster)
library(sf)
library(stringr)
library(tidyr)
    
# Create a list of zonal predictor rasters
predictors_zonal = list.files(zonal_folder, pattern = 'tif$', full.names = TRUE)
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
point_data = st_read(dsn = project_geodatabase, layer = sample_points)
point_zonal = data.frame(point_data, raster::extract(predictor_stack, point_data))
end = proc.time() - start
print(end[3])
    
# Convert field names to standard
point_zonal = point_zonal %>%
  dplyr::rename(hyd_seasonal_water = GMT2_SeasonalWater_Percentage,
                hyd_estuary_dist = Estuary_Distance,
                inf_developed = Infrastructure_Developed,
                inf_pipeline = Infrastructure_Pipelines,
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
                foliar_wetsed = NorthAmericanBeringia_wetsed_A6,
                prob_barren = GMT2_Probability_barren,
                prob_dunes = GMT2_Probability_dunes,
                prob_freshmarsh = GMT2_Probability_freshwater_marsh,
                prob_nonpatternedmesic = GMT2_Probability_nonpatterned_mesic,
                prob_nonpatterneddrained = GMT2_Probability_nonpatterned_drained,
                prob_floodplain = GMT2_Probability_nonpatterned_floodplain,
                prob_troughs = GMT2_Probability_permafrost_troughs,
                prob_polymesic = GMT2_Probability_poly_mesiccenter,
                prob_polywet = GMT2_Probability_poly_wetcenter,
                prob_saltkilled = GMT2_Probability_salt_killed,
                prob_streamcorridor = GMT2_Probability_stream_corridor,
                prob_tidalmarsh = GMT2_Probability_tidal_marsh,
                prob_water = GMT2_Probability_water,
                cv_group = GMT2_ValidationGroups,
                phen_2001_01_greenup = MCD12Q2006_2001_01_midgreenup,
                phen_2001_02_maturity = MCD12Q2006_2001_02_maturity,
                phen_2001_03_senescence = MCD12Q2006_2001_03_senescence,
                phen_2001_04_greendown = MCD12Q2006_2001_04_midgreendown,
                phen_2002_01_greenup = MCD12Q2006_2002_01_midgreenup,
                phen_2002_02_maturity = MCD12Q2006_2002_02_maturity,
                phen_2002_03_senescence = MCD12Q2006_2002_03_senescence,
                phen_2002_04_greendown = MCD12Q2006_2002_04_midgreendown,
                phen_2003_01_greenup = MCD12Q2006_2003_01_midgreenup,
                phen_2003_02_maturity = MCD12Q2006_2003_02_maturity,
                phen_2003_03_senescence = MCD12Q2006_2003_03_senescence,
                phen_2003_04_greendown = MCD12Q2006_2003_04_midgreendown,
                phen_2004_01_greenup = MCD12Q2006_2004_01_midgreenup,
                phen_2004_02_maturity = MCD12Q2006_2004_02_maturity,
                phen_2004_03_senescence = MCD12Q2006_2004_03_senescence,
                phen_2004_04_greendown = MCD12Q2006_2004_04_midgreendown,
                phen_2005_01_greenup = MCD12Q2006_2005_01_midgreenup,
                phen_2005_02_maturity = MCD12Q2006_2005_02_maturity,
                phen_2005_03_senescence = MCD12Q2006_2005_03_senescence,
                phen_2005_04_greendown = MCD12Q2006_2005_04_midgreendown,
                phen_2006_01_greenup = MCD12Q2006_2006_01_midgreenup,
                phen_2006_02_maturity = MCD12Q2006_2006_02_maturity,
                phen_2006_03_senescence = MCD12Q2006_2006_03_senescence,
                phen_2006_04_greendown = MCD12Q2006_2006_04_midgreendown,
                phen_2007_01_greenup = MCD12Q2006_2007_01_midgreenup,
                phen_2007_02_maturity = MCD12Q2006_2007_02_maturity,
                phen_2007_03_senescence = MCD12Q2006_2007_03_senescence,
                phen_2007_04_greendown = MCD12Q2006_2007_04_midgreendown,
                phen_2008_01_greenup = MCD12Q2006_2008_01_midgreenup,
                phen_2008_02_maturity = MCD12Q2006_2008_02_maturity,
                phen_2008_03_senescence = MCD12Q2006_2008_03_senescence,
                phen_2008_04_greendown = MCD12Q2006_2008_04_midgreendown,
                phen_2009_01_greenup = MCD12Q2006_2009_01_midgreenup,
                phen_2009_02_maturity = MCD12Q2006_2009_02_maturity,
                phen_2009_03_senescence = MCD12Q2006_2009_03_senescence,
                phen_2009_04_greendown = MCD12Q2006_2009_04_midgreendown,
                phen_2010_01_greenup = MCD12Q2006_2010_01_midgreenup,
                phen_2010_02_maturity = MCD12Q2006_2010_02_maturity,
                phen_2010_03_senescence = MCD12Q2006_2010_03_senescence,
                phen_2010_04_greendown = MCD12Q2006_2010_04_midgreendown,
                phen_2011_01_greenup = MCD12Q2006_2011_01_midgreenup,
                phen_2011_02_maturity = MCD12Q2006_2011_02_maturity,
                phen_2011_03_senescence = MCD12Q2006_2011_03_senescence,
                phen_2011_04_greendown = MCD12Q2006_2011_04_midgreendown,
                phen_2012_01_greenup = MCD12Q2006_2012_01_midgreenup,
                phen_2012_02_maturity = MCD12Q2006_2012_02_maturity,
                phen_2012_03_senescence = MCD12Q2006_2012_03_senescence,
                phen_2012_04_greendown = MCD12Q2006_2012_04_midgreendown,
                phen_2013_01_greenup = MCD12Q2006_2013_01_midgreenup,
                phen_2013_02_maturity = MCD12Q2006_2013_02_maturity,
                phen_2013_03_senescence = MCD12Q2006_2013_03_senescence,
                phen_2013_04_greendown = MCD12Q2006_2013_04_midgreendown,
                phen_2014_01_greenup = MCD12Q2006_2014_01_midgreenup,
                phen_2014_02_maturity = MCD12Q2006_2014_02_maturity,
                phen_2014_03_senescence = MCD12Q2006_2014_03_senescence,
                phen_2014_04_greendown = MCD12Q2006_2014_04_midgreendown,
                phen_2015_01_greenup = MCD12Q2006_2015_01_midgreenup,
                phen_2015_02_maturity = MCD12Q2006_2015_02_maturity,
                phen_2015_03_senescence = MCD12Q2006_2015_03_senescence,
                phen_2015_04_greendown = MCD12Q2006_2015_04_midgreendown,
                phen_2016_01_greenup = MCD12Q2006_2016_01_midgreenup,
                phen_2016_02_maturity = MCD12Q2006_2016_02_maturity,
                phen_2016_03_senescence = MCD12Q2006_2016_03_senescence,
                phen_2016_04_greendown = MCD12Q2006_2016_04_midgreendown,
                phen_2017_01_greenup = MCD12Q2006_2017_01_midgreenup,
                phen_2017_02_maturity = MCD12Q2006_2017_02_maturity,
                phen_2017_03_senescence = MCD12Q2006_2017_03_senescence,
                phen_2017_04_greendown = MCD12Q2006_2017_04_midgreendown,
                phen_2018_01_greenup = MCD12Q2006_2018_01_midgreenup,
                phen_2018_02_maturity = MCD12Q2006_2018_02_maturity,
                phen_2018_03_senescence = MCD12Q2006_2018_03_senescence,
                phen_2018_04_greendown = MCD12Q2006_2018_04_midgreendown,
                phen_2019_01_greenup = MCD12Q2006_2019_01_midgreenup,
                phen_2019_02_maturity = MCD12Q2006_2019_02_maturity,
                phen_2019_03_senescence = MCD12Q2006_2019_03_senescence,
                phen_2019_04_greendown = MCD12Q2006_2019_04_midgreendown,
                npp_2000 = MODIS_2000_NPP,
                npp_2001 = MODIS_2001_NPP,
                npp_2002 = MODIS_2002_NPP,
                npp_2003 = MODIS_2003_NPP,
                npp_2004 = MODIS_2004_NPP,
                npp_2005 = MODIS_2005_NPP,
                npp_2006 = MODIS_2006_NPP,
                npp_2007 = MODIS_2007_NPP,
                npp_2008 = MODIS_2008_NPP,
                npp_2009 = MODIS_2009_NPP,
                npp_2010 = MODIS_2010_NPP,
                npp_2011 = MODIS_2011_NPP,
                npp_2012 = MODIS_2012_NPP,
                npp_2013 = MODIS_2013_NPP,
                npp_2014 = MODIS_2014_NPP,
                npp_2015 = MODIS_2015_NPP,
                npp_2016 = MODIS_2016_NPP,
                npp_2017 = MODIS_2017_NPP,
                npp_2018 = MODIS_2018_NPP,
                npp_2019 = MODIS_2019_NPP,
                npp_2020 = MODIS_2020_NPP)

# Split extracted data to independent and response
independent_data = point_zonal %>%
  dplyr::select(pointid, POINT_X, POINT_Y,
         hyd_seasonal_water, hyd_estuary_dist, inf_developed, inf_pipeline,
         foliar_forb, foliar_graminoid, foliar_lichen, foliar_alnus,
         foliar_betshr, foliar_dryas, foliar_empnig, foliar_erivag,
         foliar_rhoshr, foliar_salshr, foliar_sphagn, foliar_vaculi,
         foliar_vacvit, foliar_wetsed, prob_barren, prob_dunes,
         prob_freshmarsh, prob_nonpatternedmesic, prob_nonpatterneddrained, prob_floodplain,
         prob_troughs, prob_polymesic, prob_polywet, prob_saltkilled,
         prob_streamcorridor, prob_tidalmarsh, prob_water, cv_group) %>%
  mutate(across(everything(), .fns = ~replace_na(.,0))) %>%
  mutate(cv_group = as.integer(cv_group))
response_data = point_zonal %>%
  dplyr::select(-POINT_X, -POINT_Y, -Shape,
                -hyd_seasonal_water, -hyd_estuary_dist, -inf_developed, -inf_pipeline,
                -foliar_forb, -foliar_graminoid, -foliar_lichen, -foliar_alnus,
                -foliar_betshr, -foliar_dryas, -foliar_empnig, -foliar_erivag,
                -foliar_rhoshr, -foliar_salshr, -foliar_sphagn, -foliar_vaculi,
                -foliar_vacvit, -foliar_wetsed, -prob_barren, -prob_dunes,
                -prob_freshmarsh, -prob_nonpatternedmesic, -prob_nonpatterneddrained, -prob_floodplain,
                -GMT2_Probability_poly_mixed,
                -prob_troughs, -prob_polymesic, -prob_polywet, -prob_saltkilled,
                -prob_streamcorridor, -prob_tidalmarsh, -prob_water, -cv_group) %>%
  pivot_longer(!pointid, names_to = 'covariate', values_to = 'value') %>%
  mutate(year = case_when(str_detect(covariate, '2000', negate=FALSE) ~ 0,
                          str_detect(covariate, '2001', negate=FALSE) ~ 1,
                          str_detect(covariate, '2002', negate=FALSE) ~ 2,
                          str_detect(covariate, '2003', negate=FALSE) ~ 3,
                          str_detect(covariate, '2004', negate=FALSE) ~ 4,
                          str_detect(covariate, '2005', negate=FALSE) ~ 5,
                          str_detect(covariate, '2006', negate=FALSE) ~ 6,
                          str_detect(covariate, '2007', negate=FALSE) ~ 7,
                          str_detect(covariate, '2008', negate=FALSE) ~ 8,
                          str_detect(covariate, '2009', negate=FALSE) ~ 9,
                          str_detect(covariate, '2010', negate=FALSE) ~ 10,
                          str_detect(covariate, '2011', negate=FALSE) ~ 11,
                          str_detect(covariate, '2012', negate=FALSE) ~ 12,
                          str_detect(covariate, '2013', negate=FALSE) ~ 13,
                          str_detect(covariate, '2014', negate=FALSE) ~ 14,
                          str_detect(covariate, '2015', negate=FALSE) ~ 15,
                          str_detect(covariate, '2016', negate=FALSE) ~ 16,
                          str_detect(covariate, '2017', negate=FALSE) ~ 17,
                          str_detect(covariate, '2018', negate=FALSE) ~ 18,
                          str_detect(covariate, '2019', negate=FALSE) ~ 19,
                          str_detect(covariate, '2020', negate=FALSE) ~ 20,
                          str_detect(covariate, '2021', negate=FALSE) ~ 21,
                          TRUE ~ -999)) %>%
  mutate(covariate = case_when(str_detect(covariate, 'npp', negate=FALSE) ~ 'npp',
                               str_detect(covariate, 'greenup', negate=FALSE) ~ 'greenup',
                               str_detect(covariate, 'maturity', negate=FALSE) ~ 'maturity',
                               str_detect(covariate, 'senescence', negate=FALSE) ~ 'senescence',
                               str_detect(covariate, 'greendown', negate=FALSE) ~ 'greendown',
                               TRUE ~ '-999')) %>%
  pivot_wider(names_from = 'covariate', values_from = 'value')

# Join independent and response data to create a spatiotemporal series
spatiotemporal_series = response_data %>%
  left_join(independent_data, by = 'pointid')

# Export data as a csv
st_write(spatiotemporal_series, output_file, coords = FALSE)