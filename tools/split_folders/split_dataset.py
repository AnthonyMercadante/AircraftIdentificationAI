# Import the splitfolders library
import splitfolders

# Define the path to the input folder containing the dataset
# Ensure this path points to your dataset directory
input_folder = r"A:\Projects\AircraftIdentificationAI\dataset"

# Define the path for the output folder where the split dataset will be saved
# This will be the location of the training, validation, and test datasets
output_folder = r"A:\Projects\AircraftIdentificationAI\split_dataset"

# Splitting the dataset into training, validation, and test sets
# The dataset will be split with the following ratio:
# - 70% of the data for training
# - 15% of the data for validation
# - 15% of the data for testing
# A seed is set for reproducibility
splitfolders.ratio(input_folder, output=output_folder, seed=42, ratio=(0.7, 0.15, 0.15))
