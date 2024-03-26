"""
 *************************************************************
 *                                                           *
 *    Author: Anthony Mercadante                             *
 *    Project: Aircraft Identification AI                    *
 *    Creation Date: March 11, 2024                          *
 *    Mohawk College Student - Student Number: 000361525     *
 *                                                           *
 *************************************************************
"""
import os

def update_index_in_files(folder_path, new_index=1):
    """
    Updates the first number in each line of all text files within the specified folder to a new index.

    Args:
    folder_path (str): The path to the folder containing the text files.
    new_index (int): The new index number to replace the first number in each line. Defaults to 81.
    """
    # List all files in the specified folder
    for filename in os.listdir(folder_path):
        # Construct the full file path
        file_path = os.path.join(folder_path, filename)
        # Check if the current file is a text file
        if os.path.isfile(file_path) and file_path.endswith('.txt'):
            # Read the contents of the file
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            # Replace the first number in each line with the new index
            with open(file_path, 'w') as file:
                for line in lines:
                    parts = line.split()
                    if parts:  # Check if the line is not empty
                        parts[0] = str(new_index)  # Update the first number
                        file.write(' '.join(parts) + '\n')

# Example usage
folder_path = 'output_images/labels'
update_index_in_files(folder_path)
