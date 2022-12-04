# ---------------------------------------------------------------------------
# Format confusion matrix
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Last Updated: 2022-12-03
# Usage: Script should be executed in R 4.1.0+.
# Description: "Format confusion matrix" calculates user's and producer's accuracy.
# ---------------------------------------------------------------------------

# Define version
round_date = 'round_20221125'

# Set root directory
drive = 'N:'
root_folder = 'ACCS_Work'

# Define input data
data_folder = paste(drive,
                    root_folder,
                    'Projects/VegetationEcology/BLM_AIM/GMT-2/Data',
                    sep = '/')
raw_file = paste(data_folder,
                 'Data_Output/model_results',
                 round_date,
                 'geomorphology/confusion_matrix_raw.csv',
                 sep = '/')

# Define output files
output_file = paste(data_folder,
                    'Data_Output/model_results',
                    round_date,
                    'geomorphology/confusion_matrix.csv',
                    sep = '/')

# Import libraries
library(dplyr)
library(tidyr)

# Import data to data frame
raw_data = read.csv(raw_file)

# Change column and row labels
confusion_matrix = raw_data %>%
  rename(barren = X1, dunes = X2, non_patterned = X3, wet_center = X4,
         wet_trough = X5, salt_killed = X6, tidal_marsh = X7, water = X8) %>%
  mutate(Actual = case_when(Actual == 1 ~ 'barren',
                            Actual == 2 ~ 'dunes',
                            Actual == 3 ~ 'non_patterned',
                            Actual == 4 ~ 'wet_center',
                            Actual == 5 ~ 'wet_trough',
                            Actual == 6 ~ 'salt_killed',
                            Actual == 7 ~ 'tidal_marsh',
                            Actual == 8 ~ 'water',
                            TRUE ~ Actual)) %>%
  mutate(acc_producer = 0)

# Calculate user accuracy
count = 1
while (count < 10) {
  confusion_matrix[count, 11] = round(confusion_matrix[count, count + 1] / confusion_matrix[count, 10],
                                      digits = 2)
  count = count + 1
}

# Calculate producers accuracy
confusion_matrix[10, 1] = 'acc_user'
count = 2
while (count < 11) {
  confusion_matrix[10, count] = round(confusion_matrix[count - 1, count] / confusion_matrix[9, count],
                                      digits = 2)
  count = count + 1
}

# Export data
write.csv(confusion_matrix, file = output_file, fileEncoding = 'UTF-8', row.names = FALSE)