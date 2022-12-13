# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Assign existing vegetation type
# Author: Timm Nawrocki
# Last Updated: 2022-12-12
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
input_folder = os.path.join(data_folder, 'predicted_tables', round_date, 'geomorphology')
output_folder = os.path.join(data_folder, 'predicted_tables', round_date, 'vegetation')

# Define input files
os.chdir(input_folder)
input_files = glob.glob('*.csv')

# Define EVT dictionary
evt_dictionary = {'coastal and estuarine barren': 1,
                  'freshwater floodplain barren': 2,
                  'salt-killed tundra or marsh': 3,
                  'stream corridor': 4,
                  'water': 5,
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
def evt_key(geomorphology, hyd_estuary_dist, foliar_forb, foliar_graminoid, foliar_lichen,
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
    if geomorphology == 3:
        if foliar_dryeri >= 5:
            evt_class = 'Arctic Dryas-ericaceous dwarf shrub, acidic'
        # Define tussock tundra where not dwarf shrub
        elif foliar_erivag >= 10:
            if foliar_lowshrub >= 15:
                evt_class = 'Arctic tussock low shrub tundra'
            else:
                evt_class = 'Arctic tussock dwarf shrub tundra'
    #### DEFINE DUNE TYPES
    elif geomorphology == 2:
        if hyd_estuary_dist <= 100:
            evt_class = 'Arctic herbaceous & shrub coastal dune'
        elif hyd_estuary_dist > 100 and foliar_salshr >= 5:
            evt_class = 'Arctic willow inland dune'
        else:
            evt_class = 'Arctic herbaceous inland dune'
    #### DEFINE MESIC TYPES
    elif geomorphology in (5, 6, 7):
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
    elif geomorphology in (8, 9):
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
    #### DEFINE FLOODPLAIN TYPES
    elif geomorphology in (4, 10):
        if foliar_alnus >= 5:
            evt_class = 'Arctic alder floodplain'
        elif foliar_wetsed >= 35:
            evt_class = 'Arctic sedge meadow, wet'
        elif foliar_salshr >= 10:
            evt_class = 'Arctic willow floodplain'
        elif foliar_wetsed >= 10:
            evt_class = 'Arctic sedge meadow, wet'
        else:
            if geomorphology == 10:
                evt_class == 'stream corridor'
            else:
                evt_class = 'unclassified floodplain'
    #### DEFINE COASTAL TYPES
    # Define tidal marshes
    elif geomorphology == 11:
        evt_class = 'Arctic herbaceous coastal salt marsh'
    # Define salt-killed
    elif geomorphology == 12:
        evt_class = 'salt-killed tundra or marsh'
    #### DEFINE NON-VEGETATED TYPES
    # Define barrens
    elif geomorphology == 1:
        if hyd_estuary_dist <= 100:
            evt_class = 'coastal and estuarine barren'
        elif hyd_estuary_dist > 100:
            evt_class = 'floodplain barren'
    # Define water
    elif geomorphology == 13:
        if foliar_wetsed >= 30:
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
        lambda row: evt_key(row['geomorphology'], row['hyd_estuary_dist'], row['foliar_forb'], row['foliar_graminoid'],
                            row['foliar_lichen'], row['foliar_alnus'], row['foliar_betshr'], row['foliar_dryas'],
                            row['foliar_empnig'], row['foliar_erivag'], row['foliar_rhoshr'],
                            row['foliar_salshr'], row['foliar_sphagn'], row['foliar_vaculi'], row['foliar_vacvit'],
                            row['foliar_wetsed']),
        axis=1)

    # Fill null EVT
    input_data['evt'].fillna('unclassified', inplace=True)

    # Assign EVT value
    input_data['evt_value'] = input_data['evt'].apply(lambda x: evt_dictionary.get(x))

    # Save output data
    output_data = input_data.drop(['shape_m', 'shape_m2'], axis=1)
    output_data.to_csv(output_file, header=True, index=False, sep=',', encoding='utf-8')

    # Increase count
    count += 1
