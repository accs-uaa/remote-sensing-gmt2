# ---------------------------------------------------------------------------
# Format confusion matrix
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Last Updated: 2022-12-03
# Usage: Script should be executed in R 4.1.0+.
# Description: "Format confusion matrix" calculates user's and producer's accuracy.
# ---------------------------------------------------------------------------

# Define version
round_date = 'round_20221209'

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
  rename(barren = X1, dunes = X2, nonpatterned_drained = X3, nonpatterned_floodplain = X4,
         nonpatterned_mesic = X5, permafrost_troughs = X6, poly_mesic = X7, poly_wet = X8,
         freshwater_marsh = X9, stream_corridor = X10, tidal_marsh = X11, salt_killed = X12,
         water = X13) %>%
  mutate(Actual = case_when(Actual == 1 ~ 'barren',
                            Actual == 2 ~ 'dunes',
                            Actual == 3 ~ 'nonpatterned_drained',
                            Actual == 4 ~ 'nonpatterned_floodplain',
                            Actual == 5 ~ 'nonpatterned_mesic',
                            Actual == 6 ~ 'permafrost_troughs',
                            Actual == 7 ~ 'poly_mesic',
                            Actual == 8 ~ 'poly_wet',
                            Actual == 9 ~ 'freshwater_marsh',
                            Actual == 10 ~ 'stream_corridor',
                            Actual == 11 ~ 'tidal_marsh',
                            Actual == 12 ~ 'salt_killed',
                            Actual == 13 ~ 'water',
                            TRUE ~ Actual)) %>%
  mutate(acc_producer = 0)

# Calculate user accuracy
count = 1
while (count < 15) {
  confusion_matrix[count, 16] = round(confusion_matrix[count, count + 1] / confusion_matrix[count, 15],
                                      digits = 2)
  count = count + 1
}

# Calculate producers accuracy
confusion_matrix[15, 1] = 'acc_user'
count = 2
while (count < 16) {
  confusion_matrix[15, count] = round(confusion_matrix[count - 1, count] / confusion_matrix[14, count],
                                      digits = 2)
  count = count + 1
}

# Export data
write.csv(confusion_matrix, file = output_file, fileEncoding = 'UTF-8', row.names = FALSE)