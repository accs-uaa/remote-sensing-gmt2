# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Predict geomorphology types to points
# Author: Timm Nawrocki
# Last Updated: 2022-12-09
# Usage: Must be executed in an Anaconda Python 3.9+ distribution.
# Description: "Predict geomorphology types to points" predicts a random forest model to a set of grid csv files containing extracted covariate values to produce a set of output predictions with mean and standard deviation. The script must be run on a machine that can support 4 cores.
# ---------------------------------------------------------------------------

# Import packages
import glob
import joblib
import os
import pandas as pd
import time
import datetime

# Import functions from repository statistics package
from package_Statistics import multiclass_predict

# Define round
round_date = 'round_20221209'

# Define number of predicted classes
class_number = 13

#### SET UP DIRECTORIES, FILES, AND FIELDS

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
data_folder = os.path.join(drive,
                           root_folder,
                           'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')
input_folder = os.path.join(data_folder, 'Data_Input/training_data/table')
model_folder = os.path.join(data_folder, 'Data_Output/model_results', round_date, 'geomorphology')
output_folder = os.path.join(data_folder, 'Data_Output/predicted_tables', round_date, 'geomorphology')

# Define input files
os.chdir(input_folder)
input_files = glob.glob('*.csv')
classifier_path = os.path.join(model_folder, 'classifier.joblib')

# Define variable sets
class_variable = ['train_class']
predictor_all = ['top_aspect', 'top_elevation', 'top_exposure', 'top_heat_load', 'top_position', 'top_radiation',
                 'top_roughness', 'top_slope', 'top_surface_area', 'top_surface_relief', 'top_wetness',
                 'hyd_seasonal_water', 'hyd_river_position', 'hyd_stream_position',
                 'hyd_streams', 'hyd_stream_dist', 'hyd_estuary_dist',
                 'comp_01_blue', 'comp_02_green', 'comp_03_red', 'comp_04_nearir', 'comp_evi2', 'comp_ndvi', 'comp_ndwi',
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
                 's2_09_evi2', 's2_09_nbr', 's2_09_ndmi', 's2_09_ndsi', 's2_09_ndvi', 's2_09_ndwi']
retain_variables = ['segment_id', 'POINT_X', 'POINT_Y',
                    'foliar_alnus', 'foliar_betshr', 'foliar_dryas', 'foliar_empnig', 'foliar_erivag', 'foliar_forb',
                    'foliar_graminoid', 'foliar_lichen', 'foliar_rhoshr', 'foliar_salshr', 'foliar_sphagn',
                    'foliar_vaculi', 'foliar_vacvit', 'foliar_wetsed']
prediction = ['geomorphology']
output_columns = retain_variables + predictor_all

# Define random state
rstate = 21

# Load model into memory
print('Loading classifier into memory...')
segment_start = time.time()
classifier = joblib.load(classifier_path)
# Report success
segment_end = time.time()
segment_elapsed = int(segment_end - segment_start)
segment_success_time = datetime.datetime.now()
print(f'Completed at {segment_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=segment_elapsed)})')
print('----------')

# Predict each input dataset
count = 1
input_length = len(input_files)
for file in input_files:
    # Define output file
    output_file = os.path.join(output_folder, os.path.split(file)[1])

    # Predict input dataset if output does not already exist
    if os.path.exists(output_file) == 0:
        print(f'Predicting input dataset {count} out of {input_length}...')

        # Load input data
        print('\tLoading input data')
        segment_start = time.time()
        all_data = pd.read_csv(file)
        input_data = all_data[retain_variables + class_variable + predictor_all].copy()
        input_data = input_data.dropna(axis=0, how='any')
        print(f'\tInput dataset contains {len(input_data)} rows...')
        X_data = input_data[predictor_all].astype(float)
        # Prepare output_data
        output_data = input_data[output_columns]
        # Report success
        segment_end = time.time()
        segment_elapsed = int(segment_end - segment_start)
        segment_success_time = datetime.datetime.now()
        print(f'\tCompleted at {segment_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=segment_elapsed)})')
        print('\t----------')

        # Predict data
        print('\tPredicting classes to points...')
        segment_start = time.time()
        output_data = multiclass_predict(classifier, X_data, prediction, class_number, output_data)
        # Report success
        segment_end = time.time()
        segment_elapsed = int(segment_end - segment_start)
        segment_success_time = datetime.datetime.now()
        print(f'\tCompleted at {segment_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=segment_elapsed)})')
        print('\t----------')

        # Export output data to csv
        print('\tExporting predictions to csv...')
        segment_start = time.time()
        output_data.to_csv(output_file, header=True, index=False, sep=',', encoding='utf-8')
        # Report success
        segment_end = time.time()
        segment_elapsed = int(segment_end - segment_start)
        segment_success_time = datetime.datetime.now()
        print(f'\tCompleted at {segment_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=segment_elapsed)})')
        print('\t----------')

    else:
        # Return message that output already exists
        print(f'Output dataset {count} out of {input_length} already exists.')

    # Increase count
    count += 1
    print('----------')
