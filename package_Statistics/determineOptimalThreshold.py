# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Determine optimal threshold
# Author: Timm Nawrocki
# Last Updated: 2022-11-25
# Usage: Must be executed in an Anaconda Python 3.8+ distribution.
# Description: "Determine optimal threshold" is a set of functions that test thresholds for conversion of continuous data to  binary predictions to determine a threshold value that minimizes the absolute value difference between sensitivity and specificity.
# ---------------------------------------------------------------------------

# Define a function to test binary threshold values
def test_binary_threshold(continuous_data, threshold, y_test):
    """
    Description: tests the performance of a threshold value by calculating sensitivity, specificity, auc, and accuracy on a test data set of response values
    Inputs: 'continuous_data' -- the continuous value set to test
            'threshold' -- the value to use as the conversion threshold to binary
            'y_test' -- the observed binary values
    Returned Value: Returns the sensitivity, specificity, auc, and accuracy for the specified threshold value
    Preconditions: requires existing probability predictions and binary responses of the same shape
    """

    # Import packages
    import numpy as np
    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import roc_auc_score

    # Create an empty array of zeroes that matches the length of the data
    predict_thresholded = np.zeros(continuous_data.shape)

    # Set values for all probabilities less than or equal to the threshold equal to 1
    predict_thresholded[continuous_data <= threshold] = 1

    # Determine error rates
    confusion_test = confusion_matrix(y_test.astype('int32'), predict_thresholded.astype('int32'))
    true_negative = confusion_test[0, 0]
    false_negative = confusion_test[1, 0]
    true_positive = confusion_test[1, 1]
    false_positive = confusion_test[0, 1]

    # Calculate sensitivity and specificity
    sensitivity = true_positive / (true_positive + false_negative)
    specificity = true_negative / (true_negative + false_positive)

    # Calculate AUC score
    auc = roc_auc_score(y_test.astype('int32'), continuous_data.astype(float))

    # Calculate overall accuracy
    accuracy = (true_negative + true_positive) / (true_negative + false_positive + false_negative + true_positive)

    # Return the thresholded probabilities and the performance metrics
    return sensitivity, specificity, auc, accuracy

# Define a function to test presence threshold values
def determine_optimal_threshold(continuous_data, y_test):
    """
    Description: determines the threshold value that minimizes the absolute value difference between sensitivity and specificity.
    Inputs: 'continuous_data' -- the continuous value set to test
            'y_test' -- the observed binary values
    Returned Value: Returns the optimal threshold value and the sensitivity, specificity, auc, and accuracy of the optimal threshold value
    Preconditions: requires existing continuous data and binary responses of the same shape
    """

    # Import packages
    import numpy as np

    # Determine threshold increment
    increment = (continuous_data.max(axis=0) - continuous_data.min(axis=0)) / 1000
    threshold = continuous_data.min(axis=0)

    # Iterate through numbers between 0 and 1000 to output a list of sensitivity and specificity values per threshold number
    i = 1
    sensitivity_list = []
    specificity_list = []
    threshold_list = []
    while i < 1000:
        threshold = threshold + increment
        sensitivity, specificity, auc, accuracy = test_binary_threshold(continuous_data, threshold, y_test)
        sensitivity_list.append(sensitivity)
        specificity_list.append(specificity)
        threshold_list.append(threshold)
        i = i + 1

    # Calculate a list of absolute value difference between sensitivity and specificity and find the optimal threshold
    difference_list = [np.absolute(a - b) for a, b in zip(sensitivity_list, specificity_list)]
    value, threshold = min((value, threshold) for (threshold, value) in enumerate(difference_list))
    threshold_select = threshold_list[threshold]

    # Calculate the performance of the optimal threshold
    sensitivity, specificity, auc, accuracy = test_binary_threshold(continuous_data, threshold_select, y_test)

    # Return the optimal threshold and the performance metrics of the optimal threshold
    return threshold_select, sensitivity, specificity, auc, accuracy
