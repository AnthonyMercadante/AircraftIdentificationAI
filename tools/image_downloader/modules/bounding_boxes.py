import os
import pandas as pd
from modules.utilities import *
from modules.downloader import *
from modules.csv_loader import *
from modules.utilities import bcolors as bc
from modules.show import *;

def bounding_boxes_images(args, DEFAULT_OID_DIR):
    dataset_dir, csv_dir = setup_directories(args, DEFAULT_OID_DIR)
    CLASSES_CSV = os.path.join(csv_dir, 'class-descriptions-boxable.csv')

    validate_required_arguments(args)

    if args.command == 'downloader':
        process_downloader_command(args, dataset_dir, csv_dir, CLASSES_CSV)
    elif args.command == 'visualizer':
        process_visualizer_command(args, dataset_dir)

def setup_directories(args, DEFAULT_OID_DIR):
    dataset_dir = os.path.join(DEFAULT_OID_DIR, args.Dataset if args.Dataset else 'Dataset')
    csv_dir = os.path.join(DEFAULT_OID_DIR, 'csv_folder')
    return dataset_dir, csv_dir

def validate_required_arguments(args):
    if args.type_csv is None:
        print_error_and_exit('Missing type_csv argument.')
    if args.classes is None:
        print_error_and_exit('Missing classes argument.')
    args.multiclasses = args.multiclasses or 0

def print_error_and_exit(message):
    print(bc.FAIL + message + bc.ENDC)
    exit(1)

def process_downloader_command(args, dataset_dir, csv_dir, CLASSES_CSV):
    logo(args.command)
    file_list = ['train-annotations-bbox.csv', 'validation-annotations-bbox.csv', 'test-annotations-bbox.csv']
    args.classes = process_class_arguments(args.classes)

    if args.multiclasses == '0':
        process_single_class_downloading(args, dataset_dir, csv_dir, CLASSES_CSV, file_list)
    elif args.multiclasses == '1':
        process_multiple_class_downloading(args, dataset_dir, csv_dir, CLASSES_CSV, file_list)

def process_class_arguments(classes_arg):
    if classes_arg[0].endswith('.txt'):
        with open(classes_arg[0]) as f:
            return [line.strip() for line in f.readlines()]
    else:
        return [arg.replace('_', ' ') for arg in classes_arg]

def process_single_class_downloading(args, dataset_dir, csv_dir, CLASSES_CSV, file_list):
    mkdirs(dataset_dir, csv_dir, args.classes, args.type_csv)
    df_classes = pd.read_csv(CLASSES_CSV, header=None)

    for class_name in args.classes:
        print(bc.INFO + f'Downloading {class_name}.' + bc.ENDC)
        class_code = df_classes.loc[df_classes[1] == class_name].values[0][0]

        for name_file in get_relevant_files(args.type_csv, file_list):
            df_val = l=load_ttv_csv(csv_dir, name_file, args.yes)
            download(args, df_val, name_file.split('-')[0], dataset_dir, class_name, class_code, threads=get_thread_count(args))

def get_relevant_files(type_csv, file_list):
    if type_csv == 'all':
        return file_list
    return [file for file in file_list if type_csv in file]

def get_thread_count(args):
    return int(args.n_threads) if args.n_threads else None


def process_multiple_class_downloading(args, dataset_dir, csv_dir, CLASSES_CSV, file_list):
    class_list = args.classes
    multiclass_name = '_'.join(class_list)
    mkdirs(dataset_dir, csv_dir, [multiclass_name], args.type_csv)

    df_classes = pd.read_csv(CLASSES_CSV, header=None)
    class_dict = {class_name: df_classes.loc[df_classes[1] == class_name].values[0][0] for class_name in class_list}

    for name_file in get_relevant_files(args.type_csv, file_list):
        df_val = load_ttv_csv(csv_dir, name_file, args.yes)
        download(args, df_val, name_file.split('-')[0], dataset_dir, multiclass_name, class_dict, threads=get_thread_count(args), class_list=class_list)


def process_visualizer_command(args, dataset_dir):
    while True:
        image_dir, class_name = get_visualization_inputs(dataset_dir)
        if not class_name:
            break

        download_dir = os.path.join(dataset_dir, image_dir, class_name)
        label_dir = os.path.join(download_dir, 'Label')

        validate_visualization_directories(download_dir, label_dir)

        index = 0
        max_index = len(os.listdir(download_dir)) - 1
        show_visualization_loop(class_name, download_dir, label_dir, max_index, index)

def show_classes(classes):
    """
    Display the list of downloaded classes in the selected folder during visualization mode.

    Parameters:
    classes (list): List of class names to be displayed.

    Returns:
    None
    """
    if not classes:
        print("No classes found.")
        return

    print("Downloaded Classes:")
    for class_name in classes:
        print(f"- {class_name}")
    print()


def get_visualization_inputs(dataset_dir):
    print("Which folder to visualize (train, test, validation)? <exit>")
    image_dir = input("> ")
    if image_dir == 'exit':
        return None, None

    class_image_dir = os.path.join(dataset_dir, image_dir)
    print("Which class? <exit>")
    show_classes(os.listdir(class_image_dir))  # Assumes implementation of show_classes

    class_name = input("> ")
    return (None, None) if class_name == 'exit' else (image_dir, class_name)

def validate_visualization_directories(download_dir, label_dir):
    if not os.path.isdir(download_dir) or not os.path.isdir(label_dir):
        print(bc.ERROR + "Images or labels folder not found" + bc.ENDC)
        exit(1)

def show_visualization_loop(class_name, download_dir, label_dir, max_index, index):
    # Assumes implementation of show and progression_bar functions
    while True:
        show(class_name, download_dir, label_dir, max_index, index)
        key = cv2.waitKey(0) & 0xFF
        index = update_index(key, index, max_index)

        if key == ord('q'):
            break

def update_index(key, index, max_index):
    if key == ord('d') and index < max_index:
        return index + 1
    elif key == ord('a') and index > 0:
        return index - 1
    return index
