import os
import pandas as pd
from modules.utilities import bcolors as bc
from modules.utilities import *

from csv_loader import *
from tools.image_downloader.modules.downloader import download

def image_level(args, DEFAULT_OID_DIR):
    """
    Main function to handle image level operations based on command line arguments.

    This function processes the command line arguments to set up directories,
    handle different subsets, and initiate the download process.

    Parameters:
    args (argparse.Namespace): Parsed command line arguments.
    DEFAULT_OID_DIR (str): Default directory for the Open Images Dataset.

    Returns:
    None
    """

    # Setup dataset and CSV directories
    dataset_dir, csv_dir = setup_directories(args, DEFAULT_OID_DIR)

    # Define the CSV file for class descriptions
    CLASSES_CSV = os.path.join(csv_dir, 'class-descriptions.csv')

    # Validate required subset argument
    if args.sub is None:
        print_error_and_exit('Missing subset argument.')

    # Determine file list based on the subset
    file_list = get_file_list(args.sub)

    # Validate and process further if subset is either human or machine
    if args.sub in ['h', 'm']:
        process_subset(args, dataset_dir, csv_dir, CLASSES_CSV, file_list)


def setup_directories(args, default_dir):
    """
    Set up dataset and CSV directories based on the provided arguments.

    Parameters:
    args (argparse.Namespace): Parsed command line arguments.
    default_dir (str): Default directory for the dataset.

    Returns:
    tuple: A tuple containing paths to the dataset and CSV directories.
    """
    if args.Dataset:
        dataset_dir = os.path.join(default_dir, args.Dataset)
    else:
        dataset_dir = os.path.join(default_dir, 'Dataset_nl')

    csv_dir = os.path.join(default_dir, 'csv_folder_nl')
    return dataset_dir, csv_dir


def print_error_and_exit(message):
    """
    Print an error message and exit the program.

    Parameters:
    message (str): The error message to be printed.
    """
    print(bc.FAIL + message + bc.ENDC)
    exit(1)


def get_file_list(subset):
    """
    Get the list of CSV files based on the chosen subset.

    Parameters:
    subset (str): The chosen subset ('h' for human or 'm' for machine).

    Returns:
    list: List of filenames corresponding to the chosen subset.
    """
    if subset == 'h':
        return ['train-annotations-human-imagelabels.csv',
                'validation-annotations-human-imagelabels.csv',
                'test-annotations-human-imagelabels.csv']
    elif subset == 'm':
        return ['train-annotations-machine-imagelabels.csv',
                'validation-annotations-machine-imagelabels.csv',
                'test-annotations-machine-imagelabels.csv']
    return []


def process_subset(args, dataset_dir, csv_dir, classes_csv, file_list):
    """
    Process the specified subset by downloading images and creating labels.

    Parameters:
    args (argparse.Namespace): Parsed command line arguments.
    dataset_dir (str): Path to the dataset directory.
    csv_dir (str): Path to the CSV directory.
    classes_csv (str): Path to the classes CSV file.
    file_list (list): List of file names for the chosen subset.

    Returns:
    None
    """
    # Validate required arguments
    if args.type_csv is None or args.classes is None:
        missing_arg = 'type_csv' if args.type_csv is None else 'classes'
        print_error_and_exit(f'Missing {missing_arg} argument.')

    # Set default value for multiclasses if not provided
    args.multiclasses = args.multiclasses or '0'

    # Process based on the type of classes (single or multiple)
    if args.multiclasses == '0':
        process_single_classes(args, dataset_dir, csv_dir, classes_csv, file_list)
    elif args.multiclasses == '1':
        process_multiple_classes(args, dataset_dir, csv_dir, classes_csv, file_list)


def process_single_classes(args, dataset_dir, csv_dir, classes_csv, file_list):
    """
    Process single classes for downloading images and creating labels.

    Parameters:
    args (argparse.Namespace): Parsed command line arguments.
    dataset_dir (str): Path to the dataset directory.
    csv_dir (str): Path to the CSV directory.
    classes_csv (str): Path to the classes CSV file.
    file_list (list): List of file names for the chosen subset.

    Returns:
    None
    """
    # Create directories for each class and csv type.
    mkdirs(dataset_dir, csv_dir, args.classes, args.type_csv)

    # Read class descriptions.
    df_classes = pd.read_csv(classes_csv, header=None)

    for class_name in args.classes:
        # Get class code from the CSV.
        class_code = df_classes.loc[df_classes[1] == class_name].values[0][0]

        # Process each csv file type.
        process_csv_types(args, file_list, csv_dir, dataset_dir, class_name, class_code)


def process_multiple_classes(args, dataset_dir, csv_dir, classes_csv, file_list):
    """
    Process multiple classes for downloading images and creating labels.

    Parameters:
    args (argparse.Namespace): Parsed command line arguments.
    dataset_dir (str): Path to the dataset directory.
    csv_dir (str): Path to the CSV directory.
    classes_csv (str): Path to the classes CSV file.
    file_list (list): List of file names for the chosen subset.

    Returns:
    None
    """
    # Concatenate class names for directory creation.
    multiclass_name = ['_'.join(args.classes)]
    mkdirs(dataset_dir, csv_dir, multiclass_name, args.type_csv)

    # Read class descriptions.
    df_classes = pd.read_csv(classes_csv, header=None)

    # Create a dictionary to map class names to their codes.
    class_dict = {class_name: df_classes.loc[df_classes[1] == class_name].values[0][0] for class_name in args.classes}

    # Process each csv file type for multiple classes.
    for class_name in args.classes:
        process_csv_types(args, file_list, csv_dir, dataset_dir, class_name, class_dict[class_name], args.classes)


def process_csv_types(args, file_list, csv_dir, dataset_dir, class_name, class_code, class_list=None):
    """
    Process different types of CSV files for downloading images.

    Parameters:
    args (argparse.Namespace): Parsed command line arguments.
    file_list (list): List of file names for the chosen subset.
    csv_dir (str): Path to the CSV directory.
    dataset_dir (str): Path to the dataset directory.
    class_name (str): Current class name.
    class_code (str): Code of the current class.
    class_list (list, optional): List of classes if multiple classes are involved.

    Returns:
    None
    """
    if args.type_csv in ['train', 'validation', 'test', 'all']:
        # Map CSV type to its corresponding index in file_list.
        csv_type_to_index = {'train': 0, 'validation': 1, 'test': 2, 'all': range(3)}

        # Determine indices based on the specified csv type.
        indices = csv_type_to_index[args.type_csv]
        indices = indices if isinstance(indices, range) else [indices]

        # Loop through each specified type.
        for i in indices:
            name_file = file_list[i]
            df_val = (csv_dir, name_file, args.yes)

            # Download images and labels.
            if not args.n_threads:
                download(args, df_val, ['train', 'validation', 'test'][i], dataset_dir, class_name, class_code, class_list)
            else:
                download(args, df_val, ['train', 'validation', 'test'][i], dataset_dir, class_name, class_code, class_list, int(args.n_threads))
    else:
        print_error_and_exit('csv file type not specified')

