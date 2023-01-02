# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Train and test regressor for phenology greenup
# Author: Timm Nawrocki
# Last Updated: 2022-12-23
# Usage: Must be executed in an Anaconda Python 3.9+ distribution.
# Description: "Train and test regressor for phenology greenup" trains a Random Forest model to predict greenup day of year from a set of training samples. This script runs the model train and test steps to output a trained regressor file and predicted data set.
# ---------------------------------------------------------------------------

# Import packages
import os
import numpy as np
import pandas as pd
import joblib
import time
import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import LeaveOneGroupOut

# Define round
round_date = 'round_20221219'

# Define target group
lower_threshold = 155
upper_threshold = 204

#### SET UP DIRECTORIES, FILES, AND FIELDS

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
data_folder = os.path.join(drive,
                           root_folder,
                           'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')
input_file = os.path.join(data_folder,
                          'Data_Input/vegetation_dynamics/table/',
                          'MODIS_SamplingGrid_Extracted.csv')
output_folder = os.path.join(data_folder, 'Data_Output/model_results', round_date, 'phen_greenup')

# Define output files
output_file = os.path.join(output_folder, 'prediction.csv')
performance_text = os.path.join(output_folder, 'performance.txt')

# Define variable sets
regress_variable = ['greenup']
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
predict_variable = ['pred_greenup']
cv_groups = ['cv_group']
outer_cv_split_n = ['outer_cv_split_n']
retain_variables = ['pointid', 'POINT_X', 'POINT_Y']
input_variables = retain_variables + cv_groups + predictor_all + regress_variable
output_variables = retain_variables + cv_groups + outer_cv_split_n \
                   + predictor_all + regress_variable + predict_variable

# Define random state
rstate = 21

#### CONDUCT MODEL TRAIN AND TEST ITERATIONS

# Create a standardized parameter set for a random forest classifier
rf_params = {'n_estimators': 500,
             'criterion': 'squared_error',
             'max_depth': None,
             'min_samples_split': 2,
             'min_samples_leaf': 1,
             'min_weight_fraction_leaf': 0,
             'max_features': 'sqrt',
             'bootstrap': False,
             'oob_score': False,
             'warm_start': False,
             'n_jobs': 4,
             'random_state': rstate}

# Create data frame of input data
input_data = pd.read_csv(input_file)
input_data = input_data[input_variables]
input_data = input_data.dropna()
input_data = input_data.loc[input_data[regress_variable[0]] > lower_threshold]
input_data = input_data.loc[input_data[regress_variable[0]] < upper_threshold]
print(f'Input data contains {len(input_data)} valid rows.')

# Define outer cross validation splits
outer_cv_splits = LeaveOneGroupOut()

# Create an empty data frame to store the outer cross validation splits
outer_train = pd.DataFrame(columns=regress_variable + predictor_all)
outer_test = pd.DataFrame(columns=regress_variable + predictor_all)

# Create empty data frames to store the results across all iterations
outer_results = pd.DataFrame(columns=output_variables)

# Create outer cross validation splits
print('Creating cross validation splits...')
count = 1
for train_index, test_index in outer_cv_splits.split(input_data,
                                                     input_data[regress_variable[0]],
                                                     input_data[cv_groups[0]]):
    # Split the data into train and test partitions
    train = input_data.iloc[train_index]
    test = input_data.iloc[test_index]
    # Insert outer_cv_split_n to train
    train = train.assign(outer_cv_split_n=count)
    # Insert iteration to test
    test = test.assign(outer_cv_split_n=count)
    # Append to data frames
    outer_train = pd.concat([outer_train, train], axis=0, join='outer',
                            ignore_index=True, sort=True)
    outer_test = pd.concat([outer_test, test], axis=0, join='outer',
                           ignore_index=True, sort=True)
    # Increase counter
    count += 1
cv_length = count - 1
print(f'Created {cv_length} outer cross-validation group splits.')
print('----------')

# Iterate through outer cross validation splits
outer_cv_i = 1
while outer_cv_i <= cv_length:
    iteration_start = time.time()
    print(f'\tConducting outer cross-validation iteration {outer_cv_i} of {cv_length}...')

    # Partition the outer train split by iteration number
    train_iteration = outer_train.loc[outer_train[outer_cv_split_n[0]] == outer_cv_i].copy()
    test_iteration = outer_test.loc[outer_test[outer_cv_split_n[0]] == outer_cv_i].copy()

    # Reset indices
    train_iteration = train_iteration.reset_index()
    test_iteration = test_iteration.reset_index()

    # Identify X and y train splits
    X_train_regress = train_iteration[predictor_all].astype(float).copy()
    y_train_regress = train_iteration[regress_variable[0]].astype(float).copy()

    # Train model using predictor set
    outer_regressor = RandomForestRegressor(**rf_params)
    outer_regressor.fit(X_train_regress, y_train_regress)

    # Identify X and y test splits
    X_test_regress = test_iteration[predictor_all].astype(float).copy()
    y_test_regress = test_iteration[regress_variable[0]].astype(float).copy()

    # Predict test data
    prediction = outer_regressor.predict(X_test_regress)
    predict_data = pd.DataFrame(prediction,
                                columns=predict_variable)

    # Add predictions to outer data
    output_iteration = pd.concat([test_iteration, predict_data], axis=1)
    outer_results = pd.concat([outer_results, output_iteration], axis=0, join='outer',
                              ignore_index=True, sort=True)

    # Print end message
    iteration_end = time.time()
    iteration_elapsed = int(iteration_end - iteration_start)
    iteration_success_time = datetime.datetime.now()
    print(
        f'\tCompleted at {iteration_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=iteration_elapsed)})')
    print('\t----------')

    # Increase counter
    outer_cv_i += 1

# TRAIN AND EXPORT FINAL MODEL

# Identify X and y train splits
X_train_regress = input_data[predictor_all].astype(float).copy()
y_train_regress = input_data[regress_variable[0]].astype(float).copy()

# Fit final regressor
final_regressor = RandomForestRegressor(**rf_params)
final_regressor.fit(X_train_regress, y_train_regress)

# Save regressor to external file
output_regressor = os.path.join(output_folder, 'regressor.joblib')
joblib.dump(final_regressor, output_regressor)

# Correct negative predictions to zero
outer_results.loc[outer_results[predict_variable[0]] < 0, predict_variable[0]] = 0

# Export output results to csv with column identifying test samples
outer_results = outer_results[output_variables]
outer_results.to_csv(output_file, header=True, index=False, sep=',', encoding='utf-8')

#### PRINT PERFORMANCE RESULTS

# Partition output results to foliar cover observed and predicted
y_regress_observed = outer_results[regress_variable[0]]
y_regress_predicted = outer_results[predict_variable[0]]

# Calculate performance metrics from output_results
r_score = r2_score(y_regress_observed, y_regress_predicted, sample_weight=None,
                   multioutput='uniform_average')
mae = mean_absolute_error(y_regress_observed, y_regress_predicted)
rmse = np.sqrt(mean_squared_error(y_regress_observed, y_regress_predicted))

# Report results
print('R2 = ', str(r_score))
print('MAE = ', str(mae))
print('RMSE = ', str(rmse))

# Write performance metrics to text file
with open(performance_text, 'w') as f:
    f.write('R2 = ' + str(r_score) + '\n')
    f.write('MAE = ' + str(mae) + '\n')
    f.write('RMSE = ' + str(rmse) + '\n')
