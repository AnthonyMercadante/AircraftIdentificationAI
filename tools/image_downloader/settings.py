# *************************************************************
# *                                                           *
# *    Author: Anthony Mercadante                             *
# *    Project: image_downloader tool                         *
# *    Creation Date: February 4, 2024                        *
# *    Mohawk College Student - Student Number: 000361525     *
# *                                                           *
# *************************************************************

import os
import shutil
import urllib

def PrepareFolders():
    """
    Prepares folders for dataset storage and downloads annotation files.
    
    The function first checks if a 'dataset' folder exists. If it does, it prompts
    the user to confirm its deletion. If confirmed, the folder is deleted and
    new 'dataset', 'dataset/images', and 'dataset/labels' folders are created.
    
    It then checks for the presence of specific annotation files in the current
    directory. If these files are missing, they are downloaded from predefined URLs.
    """
    # Check if 'dataset' folder exists
    if os.path.isdir('../../dataset'):
        remove = input('You have to remove dataset folder to continue (yes/no): ').lower()
        if remove.startswith('n'):
            exit(0)

    # Delete and recreate dataset folders
    shutil.rmtree('../../dataset', ignore_errors=True)
    os.mkdir("../../dataset")
    os.mkdir("../../dataset/images")
    os.mkdir("../../dataset/labels")

    # Define URLs for annotation files
    annotation_files = {
        "oidv6-train.csv": "https://storage.googleapis.com/openimages/v6/oidv6-train-annotations-bbox.csv",
        "oidv7-validation.csv": "https://storage.googleapis.com/openimages/v5/validation-annotations-bbox.csv",
        "oidv7-test.csv": "https://storage.googleapis.com/openimages/v5/test-annotations-bbox.csv"
    }

    # Download missing annotation files
    for filename, url in annotation_files.items():
        if not os.path.isfile(filename):
            urllib.request.urlretrieve(url, filename)

def ParamSettings(params):
    """
    Processes parameters and class names for dataset preparation.

    This function takes a dictionary 'params' as input, which contains various settings.
    It separates the 'classes' parameter from others and reads 'class_names.csv' to
    map class names to their corresponding IDs. It then validates and maps required
    class names from 'params' to their IDs, raising an error for any incorrect class names.

    Returns:
        tuple: A tuple containing a list of parameter values and a dictionary of 
               required class names mapped to their IDs.
    """
    # Extract required parameters excluding 'classes'
    required_params = [str(value) for key, value in params.items() if key != 'classes']

    # Read and map all class names from 'class_names.csv'
    with open('class_names.csv', 'r') as file:
        all_class_names = {line.split(',')[1].strip(): line.split(',')[0] for line in file}

    # Process and validate required class names
    required_class_names = {}
    current_name = ""
    for word in params['classes']:
        if word[0].isupper():
            if current_name and current_name in all_class_names:
                required_class_names[all_class_names[current_name]] = current_name
            current_name = word
        else:
            current_name += " " + word

    # Check the last accumulated name
    if current_name and current_name in all_class_names:
        required_class_names[all_class_names[current_name]] = current_name
    else:
        raise NameError(f'Incorrect class name: {current_name}')

    return required_params, required_class_names
