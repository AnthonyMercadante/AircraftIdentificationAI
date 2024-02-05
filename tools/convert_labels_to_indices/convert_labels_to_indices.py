# *************************************************************
# *                                                           *
# *    Author: Anthony Mercadante                             *
# *    Project: conver_labels_to_indices tool                 *
# *    Creation Date: February 4, 2024                        *
# *    Mohawk College Student - Student Number: 000361525     *
# *                                                           *
# *************************************************************

import os

# This script is designed to replace class names with corresponding indices in label files.
# It is particularly useful for preparing data for machine learning models where classes
# are expected to be numerical.

# Define the directory containing your label files.
# Update this path to the directory where your label files are stored.
label_dir = '../../dataset/labels'

# Define your class mapping.
# This dictionary maps class names (as they appear in the label files) to their respective indices.
# Add or modify entries in this dictionary according to your dataset's classes.
class_mapping = {
    'Aircraft': '0'
}

def replace_class_names(file_path, class_mapping):
    """
    Replaces class names in a label file with their corresponding class indices.

    Parameters:
    - file_path (str): Path to the label file that needs to be modified.
    - class_mapping (dict): A dictionary mapping class names (keys) to their respective indices (values).

    The function reads the content of the label file, replaces occurrences of class names with indices,
    and writes the modified content back to the same file.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        for class_name, class_index in class_mapping.items():
            line = line.replace(class_name, class_index)
        new_lines.append(line)

    with open(file_path, 'w') as file:
        file.writelines(new_lines)

# Iterate over each file in the label directory.
# This loop goes through all files in the specified directory and applies the replace_class_names function
# to each text file (files with a '.txt' extension).
for filename in os.listdir(label_dir):
    if filename.endswith('.txt'):
        file_path = os.path.join(label_dir, filename)
        replace_class_names(file_path, class_mapping)

# Print statement to indicate the completion of the process.
print("Class names replaced with indices.")

