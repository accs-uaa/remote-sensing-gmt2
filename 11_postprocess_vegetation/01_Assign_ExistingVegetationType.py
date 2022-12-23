# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Assign existing vegetation type
# Author: Timm Nawrocki
# Last Updated: 2022-12-23
# Usage: Must be executed in an Anaconda Python 3.9+ distribution.
# Description: "Assign existing vegetation type" assigns a vegetation type label from surficial features and foliar cover.
# ---------------------------------------------------------------------------

# Import packages
import glob
import pandas as pd
import os

# Define round
round_date = 'round_20221209'

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
data_folder = os.path.join(drive,
                           root_folder,
                           'Projects/VegetationEcology/BLM_AIM/GMT-2/Data/Data_Output')
input_folder = os.path.join(data_folder, 'predicted_tables', round_date, 'surface')
output_folder = os.path.join(data_folder, 'predicted_tables', round_date, 'vegetation')

# Define input files
os.chdir(input_folder)
input_files = glob.glob('*.csv')

predictor_all = ['top_aspect', 'top_elevation', 'top_exposure', 'top_heat_load', 'top_position', 'top_radiation',
                 'top_roughness', 'top_slope', 'top_surface_area', 'top_surface_relief', 'top_wetness',
                 'hyd_seasonal_water', 'hyd_river_position', 'hyd_stream_position',
                 'hyd_streams', 'hyd_stream_dist', 'hyd_estuary_dist',
                 'comp_01_blue', 'comp_02_green', 'comp_03_red', 'comp_04_nearir', 'comp_evi2', 'comp_ndvi',
                 'comp_ndwi',
                 'comp_01_blue_std', 'comp_02_green_std', 'comp_03_red_std', 'comp_04_nearir_std',
                 'comp_evi2_std', 'comp_ndvi_std', 'comp_ndwi_std',
                 'maxar_ndvi_std', 'maxar_ndvi_rng', 'maxar_ndwi_std', 'maxar_ndwi_rng',
                 's1_vh', 's1_vv', 'shape_m', 'shape_m2',
                 's2_06_02_blue', 's2_06_03_green', 's2_06_04_red', 's2_06_05_rededge1', 's2_06_06_rededge2',
                 's2_06_07_rededge3', 's2_06_08_nearir', 's2_06_08a_rededge4', 's2_06_11_shortir1', 's2_06_12_shortir2',
                 's2_06_evi2', 's2_06_nbr', 's2_06_ndmi', 's2_06_ndsi', 's2_06_ndvi', 's2_06_ndwi',
                 's2_07_02_blue', 's2_07_03_green', 's2_07_04_red', 's2_07_05_rededge1', 's2_07_06_rededge2',
                 's2_07_07_rededge3', 's2_07_08_nearir', 's2_07_08a_rededge4', 's2_07_11_shortir1', 's2_07_12_shortir2',
                 's2_07_evi2', 's2_07_nbr', 's2_07_ndmi', 's2_07_ndsi', 's2_07_ndvi', 's2_07_ndwi',
                 's2_08_02_blue', 's2_08_03_green', 's2_08_04_red', 's2_08_05_rededge1', 's2_08_06_rededge2',
                 's2_08_07_rededge3', 's2_08_08_nearir', 's2_08_08a_rededge4', 's2_08_11_shortir1', 's2_08_12_shortir2',
                 's2_08_evi2', 's2_08_nbr', 's2_08_ndmi', 's2_08_ndsi', 's2_08_ndvi', 's2_08_ndwi',
                 's2_09_02_blue', 's2_09_03_green', 's2_09_04_red', 's2_09_05_rededge1', 's2_09_06_rededge2',
                 's2_09_07_rededge3', 's2_09_08_nearir', 's2_09_08a_rededge4', 's2_09_11_shortir1', 's2_09_12_shortir2',
                 's2_09_evi2', 's2_09_nbr', 's2_09_ndmi', 's2_09_ndsi', 's2_09_ndvi', 's2_09_ndwi',
                 'foliar_alnus', 'foliar_betshr', 'foliar_dryas', 'foliar_empnig', 'foliar_erivag', 'foliar_forb',
                 'foliar_graminoid', 'foliar_lichen', 'foliar_rhoshr', 'foliar_salshr', 'foliar_sphagn',
                 'foliar_vaculi', 'foliar_vacvit', 'foliar_wetsed',
                 'inf_developed', 'inf_pipeline']

# Define EVT dictionary
evt_dictionary = {'coastal and estuarine barren': 1,
                  'freshwater floodplain barren': 2,
                  'salt-killed tundra or marsh': 3,
                  'stream corridor': 4,
                  'water': 5,
                  'infrastructure': 6,
                  'pipelines': 7,
                  'Arctic freshwater marsh': 8,
                  'Arctic herbaceous & dwarf shrub coastal beach': 9,
                  'Arctic herbaceous & shrub coastal dune': 10,
                  'Arctic herbaceous coastal salt marsh': 11,
                  'Arctic herbaceous inland dune': 12,
                  'Arctic sedge meadow, wet': 13,
                  'Arctic Dryas-ericaceous dwarf shrub, acidic': 14,
                  'Arctic birch low shrub, mesic': 15,
                  'Arctic birch low shrub, wet': 16,
                  'Arctic willow low shrub, mesic': 17,
                  'Arctic willow low shrub, wet': 18,
                  'Arctic alder floodplain': 19,
                  'Arctic willow floodplain': 20,
                  'Arctic willow inland dune': 21,
                  'Arctic tussock dwarf shrub tundra': 22,
                  'Arctic tussock low shrub tundra': 23,
                  'unclassified': 24,
                  'unclassified floodplain': 25
                  }


# Define EVT Key
def evt_key(surface, hyd_estuary_dist,
            foliar_alnus, foliar_betshr, foliar_dryas, foliar_empnig, foliar_erivag,
            foliar_rhoshr, foliar_salshr, foliar_sphagn, foliar_vaculi, foliar_vacvit,
            foliar_wetsed):
    # Define supporting data
    foliar_shrub = foliar_alnus + foliar_betshr + foliar_dryas + foliar_empnig + foliar_rhoshr + foliar_salshr + foliar_vaculi + foliar_vacvit
    foliar_ericaceous = foliar_empnig + foliar_rhoshr + foliar_vaculi + foliar_vacvit
    foliar_dryeri = foliar_ericaceous + foliar_dryas
    foliar_lowshrub = foliar_betshr + foliar_salshr
    foliar_dwarfshrub = foliar_dryas + foliar_empnig + foliar_vaculi + foliar_vacvit
    ratio_willow_birch = foliar_salshr / (foliar_salshr + foliar_betshr + 0.01)
    wetland_indicator = foliar_wetsed + foliar_sphagn
    # Define default class
    evt_class = 'unclassified'

    #### DEFINE DRAINED TYPES
    if surface == 3:
        if foliar_dryeri >= 5:
            evt_class = 'Arctic Dryas-ericaceous dwarf shrub, acidic'
        # Define tussock tundra where not dwarf shrub
        elif foliar_erivag >= 10:
            if foliar_lowshrub >= 15:
                evt_class = 'Arctic tussock low shrub tundra'
            else:
                evt_class = 'Arctic tussock dwarf shrub tundra'
    #### DEFINE DUNE TYPES
    elif surface == 2:
        if hyd_estuary_dist <= 100:
            evt_class = 'Arctic herbaceous & shrub coastal dune'
        elif hyd_estuary_dist > 100 and foliar_salshr >= 5:
            evt_class = 'Arctic willow inland dune'
        else:
            evt_class = 'Arctic herbaceous inland dune'
    #### DEFINE MESIC TYPES
    elif surface in (5, 7, 8):
        # Define tussock tundra
        if foliar_erivag >= 8:
            if foliar_lowshrub >= 15:
                evt_class = 'Arctic tussock low shrub tundra'
            else:
                evt_class = 'Arctic tussock dwarf shrub tundra'
        # Define shrub types
        elif foliar_shrub >= 10:
            # Define low shrub types
            if foliar_lowshrub >= 15:
                if ratio_willow_birch >= 0.4:
                    if wetland_indicator >= 10:
                        evt_class = 'Arctic willow low shrub, wet'
                    else:
                        evt_class = 'Arctic willow low shrub, mesic'
                else:
                    if wetland_indicator >= 10:
                        evt_class = 'Arctic birch low shrub, wet'
                    else:
                        evt_class = 'Arctic birch low shrub, mesic'
            # Define dwarf shrub types
            elif foliar_dryeri >= 5:
                evt_class = 'Arctic Dryas-ericaceous dwarf shrub, acidic'
        # Define herbaceous types
        elif foliar_wetsed >= 10:
            evt_class = 'Arctic sedge meadow, wet'
    #### DEFINE WET TYPES
    elif surface in (6, 9):
        # Define tussock tundra
        if foliar_erivag >= 30:
            if foliar_lowshrub >= 15:
                evt_class = 'Arctic tussock low shrub tundra'
            else:
                evt_class = 'Arctic tussock dwarf shrub tundra'
        # Define shrub types
        elif foliar_shrub >= 30:
            # Define low shrub types
            if ratio_willow_birch >= 0.4:
                if wetland_indicator >= 10:
                    evt_class = 'Arctic willow low shrub, wet'
                else:
                    evt_class = 'Arctic willow low shrub, mesic'
            else:
                if wetland_indicator >= 10:
                    evt_class = 'Arctic birch low shrub, wet'
                else:
                    evt_class = 'Arctic birch low shrub, mesic'
        # Define herbaceous types
        elif foliar_shrub <= 30:
            if foliar_wetsed >= 10:
                evt_class = 'Arctic sedge meadow, wet'
            else:
                evt_class = 'Arctic freshwater marsh'
    #### DEFINE FRESHWATER MARSH
    elif surface == 10:
        evt_class = 'Arctic freshwater marsh'
    #### DEFINE FLOODPLAIN TYPES
    elif surface in (4, 11):
        if foliar_alnus >= 5:
            evt_class = 'Arctic alder floodplain'
        elif foliar_wetsed >= 35:
            evt_class = 'Arctic sedge meadow, wet'
        elif foliar_salshr >= 10:
            evt_class = 'Arctic willow floodplain'
        elif foliar_wetsed >= 10:
            evt_class = 'Arctic sedge meadow, wet'
        else:
            if surface == 10:
                evt_class = 'stream corridor'
            else:
                evt_class = 'unclassified floodplain'
    #### DEFINE COASTAL TYPES
    # Define tidal marshes
    elif surface == 11:
        evt_class = 'Arctic herbaceous coastal salt marsh'
    # Define salt-killed
    elif surface == 12:
        evt_class = 'salt-killed tundra or marsh'
    # Define vegetated coastal beaches
    elif surface == 14:
        evt_class = 'Arctic herbaceous & dwarf shrub coastal beach'
    #### DEFINE NON-VEGETATED TYPES
    # Define barrens
    elif surface == 1:
        if hyd_estuary_dist <= 20:
            evt_class = 'coastal and estuarine barren'
        elif hyd_estuary_dist > 20:
            evt_class = 'freshwater floodplain barren'
    # Define water
    elif surface == 13:
        if foliar_wetsed >= 40:
            evt_class = 'Arctic freshwater marsh'
        else:
            evt_class = 'water'

    return evt_class

# Loop through input files and assign EVT
count = 1
input_length = len(input_files)
for file in input_files:
    print(f'Processing input file {count} of {input_length}...')
    # Define output file
    output_file = os.path.join(output_folder, os.path.split(file)[1])

    # Read input data
    input_data = pd.read_csv(file).dropna()

    # Assign EVT
    input_data['evt'] = input_data.apply(
        lambda row: evt_key(row['surface'], row['hyd_estuary_dist'],
                            row['foliar_alnus'], row['foliar_betshr'], row['foliar_dryas'],
                            row['foliar_empnig'], row['foliar_erivag'], row['foliar_rhoshr'],
                            row['foliar_salshr'], row['foliar_sphagn'], row['foliar_vaculi'], row['foliar_vacvit'],
                            row['foliar_wetsed']),
        axis=1)

    # Fill null EVT
    input_data['evt'].fillna('unclassified', inplace=True)

    # Assign EVT value
    input_data['evt_value'] = input_data['evt'].apply(lambda x: evt_dictionary.get(x))

    # Save output data
    output_data = input_data.drop(predictor_all, axis=1)
    output_data.to_csv(output_file, header=True, index=False, sep=',', encoding='utf-8')

    # Increase count
    count += 1
