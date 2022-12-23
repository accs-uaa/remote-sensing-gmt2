# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Predict phenology maturity
# Author: Timm Nawrocki
# Last Updated: 2022-12-23
# Usage: Must be executed in an Anaconda Python 3.9+ distribution.
# Description: "Predict phenology maturity" predicts a random forest model to a set of grid csv files containing extracted covariate values to produce a set of output predictions. The script must be run on a machine that can support 4 cores.
# ---------------------------------------------------------------------------

# Import packages
import glob
import joblib
import os
import pandas as pd
import time
import datetime

# Define round
round_date = 'round_20221219'

#### SET UP DIRECTORIES, FILES, AND FIELDS

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
data_folder = os.path.join(drive,
                           root_folder,
                           'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')
input_folder = os.path.join(data_folder, 'Data_Output/predicted_tables', round_date, 'geomorphology')
model_folder = os.path.join(data_folder, 'Data_Output/model_results', round_date, 'phen_maturity')
output_folder = os.path.join(data_folder, 'Data_Output/predicted_tables', round_date, 'phen_maturity')

# Define input files
os.chdir(input_folder)
input_files = glob.glob('*.csv')
regressor_path = os.path.join(model_folder, 'regressor.joblib')

# Define variable sets
regress_variable = ['maturity']
predictor_all = ['foliar_forb', 'foliar_graminoid', 'foliar_lichen',
                 'foliar_alnus', 'foliar_betshr', 'foliar_dryas', 'foliar_empnig',
                 'foliar_erivag', 'foliar_rhoshr', 'foliar_salshr', 'foliar_sphagn',
                 'foliar_vaculi', 'foliar_vacvit', 'foliar_wetsed',
                 'prob_barren', 'prob_dunes', 'prob_nonpatterneddrained',
                 'prob_floodplain', 'prob_nonpatternedmesic', 'prob_nonpolywet',
                 'prob_troughs', 'prob_polymesic', 'prob_polywet', 'prob_freshmarsh',
                 'prob_streamcorridor', 'prob_tidalmarsh', 'prob_saltkilled', 'prob_coastalbeach',
                 'prob_water', 'hyd_estuary_dist', 'hyd_seasonal_water',
                 'inf_developed', 'inf_pipeline',
                 'year']
retain_variables = ['segment_id', 'POINT_X', 'POINT_Y']
predict_variable = ['pred_maturity']
output_columns = retain_variables + predict_variable

# Define random state
rstate = 21

# Load model into memory
print('Loading regressor into memory...')
segment_start = time.time()
regressor = joblib.load(regressor_path)
# Report success
segment_end = time.time()
segment_elapsed = int(segment_end - segment_start)
segment_success_time = datetime.datetime.now()
print(
    f'Completed at {segment_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=segment_elapsed)})')
print('----------')

# Create loop to predict each year
year_list = range(1, 21, 1)
for year in year_list:
    print(f'Predicting variable for year {str(2000 + year)}...')

    # Create year folder
    year_folder = os.path.join(output_folder, str(year))
    if os.path.exists(year_folder) == 0:
        os.mkdir(year_folder)

    # Predict each input dataset
    count = 1
    input_length = len(input_files)
    for file in input_files:
        # Define output file
        output_file = os.path.join(year_folder, os.path.split(file)[1])

        # Predict input dataset if output does not already exist
        if os.path.exists(output_file) == 0:
            print(f'\tPredicting input dataset {count} out of {input_length}...')

            # Load input data
            print('\t\tLoading input data')
            segment_start = time.time()
            all_data = pd.read_csv(file)
            # Rename physiography variables
            all_data = all_data.rename(columns={'class_01': 'prob_barren',
                                                'class_02': 'prob_dunes',
                                                'class_03': 'prob_nonpatterneddrained',
                                                'class_04': 'prob_floodplain',
                                                'class_05': 'prob_nonpatternedmesic',
                                                'class_06': 'prob_troughs',
                                                'class_07': 'prob_polymesic',
                                                'class_08': 'prob_polywet',
                                                'class_09': 'prob_freshmarsh',
                                                'class_10': 'prob_streamcorridor',
                                                'class_11': 'prob_tidalmarsh',
                                                'class_12': 'prob_saltkilled',
                                                'class_13': 'prob_water'})
            all_data = all_data.assign(year=year)
            # Select input data
            input_data = all_data[retain_variables + predictor_all].copy()
            input_data = input_data.fillna(0)
            print(f'\t\tInput dataset contains {len(input_data)} rows...')
            X_data = input_data[predictor_all].astype(float)
            # Prepare output_data
            output_data = input_data[retain_variables]
            # Report success
            segment_end = time.time()
            segment_elapsed = int(segment_end - segment_start)
            segment_success_time = datetime.datetime.now()
            print(
                f'\t\tCompleted at {segment_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=segment_elapsed)})')
            print('\t\t----------')

            # Predict data
            print('\t\tPredicting classes to points...')
            segment_start = time.time()
            prediction = regressor.predict(X_data)
            predict_data = pd.DataFrame(prediction,
                                        columns=predict_variable)

            # Add predictions to outer data
            output_data = pd.concat([output_data, predict_data], axis=1)
            # Correct negative predictions to zero
            output_data.loc[output_data[predict_variable[0]] < 0, predict_variable[0]] = 0
            # Report success
            segment_end = time.time()
            segment_elapsed = int(segment_end - segment_start)
            segment_success_time = datetime.datetime.now()
            print(f'\t\tCompleted at {segment_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=segment_elapsed)})')
            print('\t\t----------')

            # Export output data to csv
            print('\t\tExporting predictions to csv...')
            segment_start = time.time()
            output_data.to_csv(output_file, header=True, index=False, sep=',', encoding='utf-8')
            # Report success
            segment_end = time.time()
            segment_elapsed = int(segment_end - segment_start)
            segment_success_time = datetime.datetime.now()
            print(f'\t\tCompleted at {segment_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=segment_elapsed)})')
            print('\t\t----------')

        else:
            # Return message that output already exists
            print(f'\tOutput dataset {count} out of {input_length} already exists.')

        # Increase count
        count += 1
        print('\t----------')
    print('----------')
