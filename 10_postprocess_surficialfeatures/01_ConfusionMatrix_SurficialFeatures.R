# ---------------------------------------------------------------------------
# Format confusion matrix
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Last Updated: 2022-12-19
# Usage: Script should be executed in R 4.1.0+.
# Description: "Format confusion matrix" calculates user's and producer's accuracy.
# ---------------------------------------------------------------------------

# Define version
round_date = 'round_20221219'

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
                 'surficial_features/confusion_matrix_raw.csv',
                 sep = '/')

# Define output files
output_file = paste(data_folder,
                    'Data_Output/model_results',
                    round_date,
                    'surficial_features/confusion_matrix.csv',
                    sep = '/')

# Import libraries
library(dplyr)
library(tidyr)

# Import data to data frame
raw_data = read.csv(raw_file)

# Change column and row labels
confusion_matrix = raw_data %>%
  rename(barren = X1, dunes = X2, nonpatterned_drained = X3, nonpatterned_floodplain = X4,
         nonpatterned_mesic = X5, nonpoly_wet = X6, permafrost_troughs = X7, poly_mesic = X8,
         poly_wet = X9, freshwater_marsh = X10, stream_corridor = X11, tidal_marsh = X12,
         salt_killed = X13, vegetated_beach = X14, water = X15) %>%
  mutate(Actual = case_when(Actual == 1 ~ 'barren',
                            Actual == 2 ~ 'dunes',
                            Actual == 3 ~ 'nonpatterned_drained',
                            Actual == 4 ~ 'nonpatterned_floodplain',
                            Actual == 5 ~ 'nonpatterned_mesic',
                            Actual == 6 ~ 'nonpoly_wet',
                            Actual == 7 ~ 'permafrost_troughs',
                            Actual == 8 ~ 'poly_mesic',
                            Actual == 9 ~ 'poly_wet',
                            Actual == 10 ~ 'freshwater_marsh',
                            Actual == 11 ~ 'stream_corridor',
                            Actual == 12 ~ 'tidal_marsh',
                            Actual == 13 ~ 'salt_killed',
                            Actual == 14 ~ 'vegetated_beach',
                            Actual == 15 ~ 'water',
                            TRUE ~ Actual)) %>%
  mutate(acc_producer = 0)

# Calculate user accuracy
count = 1
while (count < 17) {
  confusion_matrix[count, 18] = round(confusion_matrix[count, count + 1] / confusion_matrix[count, 17],
                                      digits = 2)
  count = count + 1
}

# Calculate producers accuracy
confusion_matrix[17, 1] = 'acc_user'
count = 2
while (count < 18) {
  confusion_matrix[17, count] = round(confusion_matrix[count - 1, count] / confusion_matrix[16, count],
                                      digits = 2)
  count = count + 1
}

# Export data
write.csv(confusion_matrix, file = output_file, fileEncoding = 'UTF-8', row.names = FALSE)