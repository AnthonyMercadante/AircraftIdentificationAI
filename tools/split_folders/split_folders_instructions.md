# Split Dataset Instructions

This guide will help you set up and run the `split_dataset.py` script to split your dataset into training, validation, and testing sets. This step is crucial for preparing your dataset for machine learning model training.

## Prerequisites

Before you begin, ensure that you have:
- A Python environment (version >= 3.7.0).
- The `split-folders` library installed. If not, install it using `pip`:
  ```bash
  pip install split-folders
  ```

## Setting Up `split_dataset.py`

1. **Locate Your Dataset**: Identify the location of your dataset. This is the folder containing the images you wish to split into different sets.

2. **Edit the Script**: Open `split_dataset.py` in a text editor or IDE. You will need to modify the `input_folder` and `output_folder` paths:
   - `input_folder`: Replace this with the path to your dataset.
   - `output_folder`: Specify the path where you want the split datasets (training, validation, test) to be saved.

   Example:
   ```python
   input_folder = r"path_to_your_dataset_folder"
   output_folder = r"path_to_your_output_folder"
   ```

3. **Save the Changes**: After editing the paths, save the file.

## Running the Script

1. **Open a Command Line Interface**: Open a terminal or command prompt.

2. **Navigate to the Script's Directory**: Use the `cd` command to navigate to the directory where `split_dataset.py` is located.

3. **Run the Script**: Execute the script by running:
   ```bash
   python split_dataset.py
   ```

4. **Check the Output**: Once the script finishes running, check the `output_folder` you specified. It should contain three new folders: `train`, `val`, and `test`, each containing a portion of your dataset according to the specified ratios.

## Troubleshooting

- If you encounter any errors related to missing libraries, ensure that you have installed `split-folders` as mentioned in the prerequisites.
- Ensure that the paths for the `input_folder` and `output_folder` are correct and accessible.
