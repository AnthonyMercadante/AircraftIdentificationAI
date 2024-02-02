import os
import itertools
import cv2
from modules.utilities import images_options
from modules.utilities import bcolors as bc
from modules.utilities import download_img


def download(args, df_val, folder, dataset_dir, class_name, class_code, class_list=None, threads=20):
    """
    Manage the download of images and the creation of labels.

    This function handles the downloading of images from a given dataset based on specific parameters. 
    It also manages the creation of labels for these images.

    Parameters:
    args (argparse.Namespace): Arguments provided by the user or a script.
    df_val (pandas.DataFrame): DataFrame containing values relevant to the dataset.
    folder (str): The folder type (e.g., 'train', 'validation', 'test').
    dataset_dir (str): The directory where the dataset is stored or will be stored.
    class_name (str): The name of the class for which images are being downloaded.
    class_code (str): The code corresponding to the class_name.
    class_list (list, optional): List of classes, used when multiple classes are involved. Defaults to None.
    threads (int, optional): The number of threads to use for downloading images. Defaults to 20.

    Returns:
    None
    """
    
    # Determine the terminal size for proper formatting of print statements.
    term_columns = get_terminal_size()

    # Calculate the length for header formatting.
    l = int((term_columns - len(class_name)) / 2)

    # Header display.
    print_header(l, class_name)

    # Inform user about the download process.
    print(bc.INFO + 'Downloading {} images.'.format(args.type_csv) + bc.ENDC)

    # Filter the DataFrame based on user arguments.
    df_val_images = images_options(df_val, args)

    # Create a list of image IDs to download.
    images_list = get_images_list(df_val_images, class_code)

    # Apply limit if specified in arguments.
    if args.limit is not None:
        images_list = apply_limit(images_list, args.limit)

    # Determine class name list for labeling.
    class_name_list = determine_class_name_list(class_list, class_name)

    # Download images.
    download_img(folder, dataset_dir, class_name_list, images_list, threads)

    # Generate labels if not a subset.
    if not args.sub:
        get_label(folder, dataset_dir, class_name, class_code, df_val, class_name_list, args)


def get_terminal_size():
    """
    Determine the terminal size for properly formatting the output.
    
    Returns:
    int: Number of columns in the terminal.
    """
    if os.name == 'posix':
        _, columns = os.popen('stty size', 'r').read().split()
    elif os.name == 'nt':
        try:
            columns, _ = os.get_terminal_size(0)
        except OSError:
            columns, _ = os.get_terminal_size(1)
    else:
        columns = 50

    return int(columns)


def print_header(length, class_name):
    """
    Print the header for the download process.

    Parameters:
    length (int): Length for formatting the header.
    class_name (str): Name of the class.
    """
    print('\n' + bc.HEADER + '-' * length + class_name + '-' * length + bc.ENDC)


def get_images_list(df, class_code):
    """
    Generate a list of image IDs from the DataFrame.

    Parameters:
    df (pandas.DataFrame): The DataFrame to process.
    class_code (str): The class code to filter the images.

    Returns:
    set: A set of image IDs.
    """
    images = df['ImageID'][df.LabelName == class_code].values
    return set(images)


def apply_limit(images, limit):
    """
    Limit the number of images to the specified limit.

    Parameters:
    images (set): The set of image IDs.
    limit (int): The maximum number of images to include.

    Returns:
    set: A set of image IDs limited to the specified count.
    """
    return set(itertools.islice(images, limit))


def determine_class_name_list(class_list, class_name):
    """
    Determine the class name list for labeling.

    Parameters:
    class_list (list or None): List of classes.
    class_name (str): The name of the class.

    Returns:
    str: The class name list as a string.
    """
    return '_'.join(class_list) if class_list is not None else class_name

import os
import cv2

def get_label(folder, dataset_dir, class_name, class_code, df_val, class_list, args):
    """
    Generate label files for images.

    This function creates text files containing label information for each image
    in the specified dataset. It handles both single-class and multi-class scenarios.

    Parameters:
    folder (str): The type of dataset (e.g., 'train', 'validation', 'test').
    dataset_dir (str): The base directory where the dataset is stored.
    class_name (str): The name of the class.
    class_code (str): The code corresponding to the class.
    df_val (pandas.DataFrame): DataFrame containing image information.
    class_list (list): List of classes, used when multiple classes are involved.
    args (argparse.Namespace): Command-line arguments passed to the script.

    Returns:
    None
    """

    if not args.noLabels:
        print_label_creation_start_info(class_name, folder)

        # Determine the directories for download and labels.
        download_dir, label_dir = get_directories(dataset_dir, folder, class_name, class_list)

        # Get list of images that have been downloaded.
        downloaded_images_list = get_downloaded_images(download_dir)

        # Create labels for each image.
        create_labels(df_val, class_code, downloaded_images_list, download_dir, label_dir, class_name)

        print_label_creation_completion_info()


def get_directories(dataset_dir, folder, class_name, class_list):
    """
    Determine the download and label directories based on the dataset configuration.

    Parameters:
    dataset_dir (str): The base directory where the dataset is stored.
    folder (str): The type of dataset.
    class_name (str): The name of the class.
    class_list (list or None): List of classes if multi-class.

    Returns:
    tuple: Tuple containing the paths to the download and label directories.
    """
    if class_list is not None:
        download_dir = os.path.join(dataset_dir, folder, '_'.join(class_list))
        label_dir = os.path.join(dataset_dir, folder, '_'.join(class_list), 'Label')
    else:
        download_dir = os.path.join(dataset_dir, folder, class_name)
        label_dir = os.path.join(dataset_dir, folder, class_name, 'Label')

    os.makedirs(label_dir, exist_ok=True)  # Ensure label directory exists.
    return download_dir, label_dir


def get_downloaded_images(download_dir):
    """
    Retrieve a list of downloaded images from the download directory.

    Parameters:
    download_dir (str): The directory where images have been downloaded.

    Returns:
    list: List of downloaded image file names without the extension.
    """
    return [f.split('.')[0] for f in os.listdir(download_dir) if f.endswith('.jpg')]


def create_labels(df_val, class_code, images_list, download_dir, label_dir, class_name):
    """
    Create label files for each image.

    Parameters:
    df_val (pandas.DataFrame): DataFrame containing image information.
    class_code (str): The code corresponding to the class.
    images_list (list): List of image names to create labels for.
    download_dir (str): The directory where images are downloaded.
    label_dir (str): The directory where labels will be saved.
    class_name (str): The name of the class.
    """
    groups = df_val[df_val.LabelName == class_code].groupby('ImageID')

    for image in images_list:
        try:
            current_image_path = os.path.join(download_dir, image + '.jpg')
            dataset_image = cv2.imread(current_image_path)
            boxes = groups.get_group(image)[['XMin', 'XMax', 'YMin', 'YMax']].values.tolist()

            write_label_file(label_dir, image, boxes, dataset_image, class_name)
        except Exception as e:
            print(f"Error processing image {image}: {e}")


def write_label_file(label_dir, image, boxes, dataset_image, class_name):
    """
    Write the label information to a file for a single image.

    Parameters:
    label_dir (str): The directory where labels will be saved.
    image (str): The name of the image.
    boxes (list): List of bounding box coordinates.
    dataset_image (numpy.ndarray): The image array.
    class_name (str): The name of the class.
    """
    file_name = f'{image}.txt'
    file_path = os.path.join(label_dir, file_name)
    mode = 'a' if os.path.isfile(file_path) else 'w'

    with open(file_path, mode) as f:
        for box in boxes:
            normalized_box = normalize_box_coordinates(box, dataset_image)
            print(class_name, *normalized_box, file=f)


def normalize_box_coordinates(box, image):
    """
    Normalize the box coordinates to the size of the image.

    Parameters:
    box (list): List of box coordinates [XMin, XMax, YMin, YMax].
    image (numpy.ndarray): The image array.

    Returns:
    list: Normalized box coordinates.
    """
    x_min, x_max, y_min, y_max = box
    height, width = image.shape[:2]
    return [x_min * width, x_max * width, y_min * height, y_max * height]


def print_label_creation_start_info(class_name, folder):
    """
    Print information about the start of label creation.

    Parameters:
    class_name (str): The name of the class.
    folder (str): The type of dataset.
    """
    print(bc.INFO + f'Creating labels for {class_name} of {folder}.' + bc.ENDC)


def print_label_creation_completion_info():
    """
    Print information indicating the completion of label creation.
    """
    print(bc.INFO + 'Labels creation completed.' + bc.ENDC)

