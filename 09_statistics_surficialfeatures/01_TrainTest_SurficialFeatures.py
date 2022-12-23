# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Train and test surficial feature classifier
# Author: Timm Nawrocki
# Last Updated: 2022-12-20
# Usage: Must be executed in an Anaconda Python 3.9+ distribution.
# Description: "Train and test surficial feature classifier " trains a random forest model to predict surficial features from a set of training points. This script runs the model train and test steps to output a trained classifier file and predicted data set. The script must be run on a machine that can support 4 cores.
# ---------------------------------------------------------------------------

# Import packages
import os
import pandas as pd
from sklearn.model_selection import LeaveOneGroupOut
import time
import datetime

# Import functions from repository statistics package
from package_Statistics import multiclass_train_test

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
covariate_folder = os.path.join(data_folder, 'Data_Input/training_data/table_revised')
response_folder = os.path.join(data_folder, 'Data_Input/training_data/table_training')
output_folder = os.path.join(data_folder, 'Data_Output/model_results', round_date, 'surficial_features')

# Define output data
output_csv = os.path.join(output_folder, 'prediction.csv')
output_classifier = os.path.join(output_folder, 'classifier.joblib')
importance_mdi_csv = os.path.join(output_folder, 'importance_classifier_mdi.csv')
confusion_csv = os.path.join(output_folder, 'confusion_matrix_raw.csv')

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
                 's2_09_evi2', 's2_09_nbr', 's2_09_ndmi', 's2_09_ndsi', 's2_09_ndvi', 's2_09_ndwi',
                 'foliar_alnus', 'foliar_betshr', 'foliar_dryas', 'foliar_empnig', 'foliar_erivag', 'foliar_forb',
                 'foliar_graminoid', 'foliar_lichen', 'foliar_rhoshr', 'foliar_salshr', 'foliar_sphagn',
                 'foliar_vaculi', 'foliar_vacvit', 'foliar_wetsed',
                 'inf_developed', 'inf_pipeline']
cv_groups = ['cv_group']
retain_variables = ['segment_id', 'POINT_X', 'POINT_Y']
outer_cv_split_n = ['outer_cv_split_n']
prediction = ['class_predict']
output_variables = class_variable + predictor_all + outer_cv_split_n + prediction

# Define random state
rstate = 21

#### CONDUCT MODEL TRAIN AND TEST ITERATIONS

# Create a standardized parameter set for a random forest classifier
classifier_params = {'n_estimators': 500,
                     'criterion': 'gini',
                     'max_depth': None,
                     'min_samples_split': 2,
                     'min_samples_leaf': 1,
                     'min_weight_fraction_leaf': 0,
                     'max_features': 'sqrt',
                     'bootstrap': False,
                     'oob_score': False,
                     'warm_start': False,
                     'class_weight': 'balanced',
                     'n_jobs': 4,
                     'random_state': rstate}

# Define grids
grid_list = ['A4', 'A5', 'A6', 'A7',
             'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7',
             'C1', 'C2', 'C3', 'C4', 'C5', 'C6',
             'D1', 'D2', 'D3', 'D4', 'D5',
             'E1', 'E2', 'E3', 'E4', 'E5']

# Create data frame of input data
input_length = len(grid_list)
input_data = pd.DataFrame(columns=retain_variables + class_variable + cv_groups + predictor_all)
count = 1
for grid in grid_list:
    print(f'Reading input data {count} of {input_length}...')
    covariate_file = os.path.join(covariate_folder, grid + '.csv')
    response_file = os.path.join(response_folder, grid + '.csv')
    covariate_data = pd.read_csv(covariate_file)
    response_data = pd.read_csv(response_file)
    covariate_data = covariate_data.drop(['cv_group', 'train_class'], axis=1)
    join_data = response_data.join(covariate_data.set_index('segment_id'), on='segment_id')
    input_data = pd.concat([input_data, join_data], axis=0)
    input_data = input_data.fillna(0)
    input_data = input_data.loc[input_data[class_variable[0]] > 0].copy()
    count += 1
print(f'Input data contains {len(input_data)} rows.')

# Define leave one group out cross validation split methods
outer_cv_splits = LeaveOneGroupOut()

# Create empty data frames to store the results across all iterations
output_results = pd.DataFrame(columns=output_variables)
importances_all = pd.DataFrame(columns=['covariate', 'importance'])

# Conduct model train and test for iteration
outer_results, trained_classifier, importance_table = multiclass_train_test(classifier_params,
                                                                            outer_cv_splits,
                                                                            input_data,
                                                                            class_variable,
                                                                            predictor_all,
                                                                            cv_groups,
                                                                            retain_variables,
                                                                            outer_cv_split_n,
                                                                            prediction,
                                                                            rstate,
                                                                            output_classifier)

# Print results of model train and test
print(f'Outer results contain {len(outer_results)} rows.')
print('----------')

#### STORE RESULTS

# Calculate and store confusion matrix
print('Saving confusion matrix to csv file...')
iteration_start = time.time()
# Assign true and predicted values
true_data = outer_results[class_variable[0]]
pred_data = outer_results[prediction[0]]
# Create confusion matrix
confusion_data = pd.crosstab(true_data, pred_data, rownames=['Actual'], colnames=['Predicted'], margins=True)
# Export confusion matrix
confusion_data.to_csv(confusion_csv, header=True, index=True, sep=',', encoding='utf-8')
iteration_end = time.time()
iteration_elapsed = int(iteration_end - iteration_start)
iteration_success_time = datetime.datetime.now()
print(
    f'Completed at {iteration_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=iteration_elapsed)})')
print('----------')

# Store output results in csv file
print('Saving combined results to csv file...')
iteration_start = time.time()
outer_results.to_csv(output_csv, header=True, index=False, sep=',', encoding='utf-8')
iteration_end = time.time()
iteration_elapsed = int(iteration_end - iteration_start)
iteration_success_time = datetime.datetime.now()
print(
    f'Completed at {iteration_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=iteration_elapsed)})')
print('----------')

# Store output importances in csv file
print('Saving variable importances to csv file...')
iteration_start = time.time()
importance_table.to_csv(importance_mdi_csv, header=True, index=False, sep=',', encoding='utf-8')
iteration_end = time.time()
iteration_elapsed = int(iteration_end - iteration_start)
iteration_success_time = datetime.datetime.now()
print(
    f'Completed at {iteration_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=iteration_elapsed)})')
print('----------')
