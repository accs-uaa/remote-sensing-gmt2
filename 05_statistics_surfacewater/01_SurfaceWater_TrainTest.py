# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Train and test surface water threshold
# Author: Timm Nawrocki
# Last Updated: 2022-11-25
# Usage: Must be executed in an Anaconda Python 3.9+ distribution.
# Description: "Train and test surface water threshold" systematically tests thresholds for synthetic aperture radar (SAR) between points representative of water and not-water. The threshold that minimizes the absolute value difference between sensitivity and specificity is selected.
# ---------------------------------------------------------------------------

# Import packages
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from package_Statistics import determine_optimal_threshold
import time
import datetime

# Define round
round_date = 'round_20221125'

#### SET UP DIRECTORIES, FILES, AND FIELDS

# Set root directory
drive = 'N:/'
root_folder = 'ACCS_Work'

# Define folder structure
data_folder = os.path.join(drive,
                           root_folder,
                           'Projects/VegetationEcology/BLM_AIM/GMT-2/Data')
data_input = os.path.join(data_folder, 'Data_Input/surface_water')
data_output = os.path.join(data_folder, 'Data_Output/model_results', round_date, 'surface_water')

# Define input file
input_file = os.path.join(data_input, 'GMT2_SurfaceWater_Points.xlsx')

# Define output data
threshold_file = os.path.join(data_output, 'threshold.txt')
accuracy_file = os.path.join(data_output, 'accuracy.txt')
output_file = os.path.join(data_output, 'prediction.csv')

# Define variable sets
class_variable = ['water']
predictor_variable = ['vv']
retain_variables = ['OBJECTID', 'month', 'POINT_X', 'POINT_Y']
cv_split_n = ['cv_split_n']
predicted_variable = ['prediction']
all_variables = retain_variables + class_variable + predictor_variable + cv_split_n
output_variables = all_variables + predicted_variable

# Define random state
rstate = 21

#### CONDUCT MODEL TRAIN AND TEST ITERATIONS

# Create data frame of input data
input_data = pd.read_excel(input_file, sheet_name='GMT2_SurfaceWater_Points')

# Define cross validation
cv_splits = StratifiedKFold(n_splits=5, shuffle=True, random_state=rstate)

# Create an empty data frame to store the outer cross validation splits
outer_train = pd.DataFrame(columns=all_variables)
outer_test = pd.DataFrame(columns=all_variables)

# Create empty data frames to store the results across all iterations
outer_results = pd.DataFrame(columns=output_variables)

# Create cross validation splits
print('Creating cross validation splits...')
count = 1
for train_index, test_index in cv_splits.split(input_data,
                                               input_data[class_variable[0]]):
    # Split the data into train and test partitions
    train = input_data.iloc[train_index]
    test = input_data.iloc[test_index]
    # Insert outer_cv_split_n to train
    train = train.assign(cv_split_n=count)
    # Insert iteration to test
    test = test.assign(cv_split_n=count)
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

# Create empty threshold list
threshold_list = []

# Iterate through outer cross validation splits
cv_i = 1
while cv_i <= cv_length:
    iteration_start = time.time()
    print(f'\tConducting cross-validation iteration {cv_i} of {cv_length}...')

    # Partition the outer train split by iteration number
    train_iteration = outer_train.loc[outer_train[cv_split_n[0]] == cv_i].copy()
    test_iteration = outer_test.loc[outer_test[cv_split_n[0]] == cv_i].copy()

    # Reset indices
    train_iteration = train_iteration.reset_index()
    test_iteration = test_iteration.reset_index()

    # Identify X and y train splits
    X_train = train_iteration[predictor_variable].astype(float).copy()
    y_train = train_iteration[class_variable[0]].astype('int32').copy()

    # Evaluate thresholds
    threshold, sensitivity, specificity, auc, accuracy = determine_optimal_threshold(X_train, y_train)
    threshold_list.append(threshold)

    # Identify X and y test splits
    X_test = test_iteration[predictor_variable].astype(float).copy()
    y_test = test_iteration[class_variable[0]].astype('int32').copy()

    # Predict test data
    predict_thresholded = np.zeros(X_test.shape)
    predict_thresholded[X_test <= threshold] = 1
    predict_data = pd.DataFrame(predict_thresholded, columns=predicted_variable)

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
    cv_i += 1

# Identify observed and predicted
y_observed = outer_results[class_variable[0]]
y_predicted = outer_results[predicted_variable[0]]

# Determine error rates
confusion_test = confusion_matrix(y_observed.astype('int32'), y_predicted.astype('int32'))
true_negative = confusion_test[0, 0]
false_negative = confusion_test[1, 0]
true_positive = confusion_test[1, 1]
false_positive = confusion_test[0, 1]

# Calculate sensitivity and specificity
sensitivity = true_positive / (true_positive + false_negative)
specificity = true_negative / (true_negative + false_positive)

# Calculate AUC score
auc = roc_auc_score(y_observed.astype('int32'), y_predicted.astype(float))

# Calculate overall accuracy
accuracy = (true_negative + true_positive) / (true_negative + false_positive + false_negative + true_positive)

# Return the thresholded probabilities and the performance metrics
print(f'Mean Threshold = {np.mean(threshold_list)}')
print(f'Accuracy = {accuracy}')

# Export output results to csv with column identifying test samples
outer_results.to_csv(output_file, header=True, index=False, sep=',', encoding='utf-8')