import os
from multiprocessing.pool import ThreadPool
from tqdm import tqdm

def images_options(df_val, args):
    """
    Filter a DataFrame based on image attributes.

    This function filters the provided DataFrame based on specific image attributes
    specified in the arguments. It removes rows where the image attributes do not
    match the specified criteria.

    Parameters:
    df_val (pandas.DataFrame): DataFrame containing image information.
    args (argparse.Namespace): Arguments specifying filtering criteria.

    Returns:
    pandas.DataFrame: The filtered DataFrame.
    """

    # List of image attributes to check.
    image_attrs = [
        'image_IsOccluded', 'image_IsTruncated', 'image_IsGroupOf',
        'image_IsDepiction', 'image_IsInside'
    ]

    # Apply filtering for each attribute if specified in args.
    for attr in image_attrs:
        df_val = filter_dataframe(df_val, args, attr)

    return df_val

def mkdirs(Dataset_folder, csv_folder, classes, type_csv):
    '''
    Make the folder structure for the system.

    :param Dataset_folder: The base folder for the dataset
    :param csv_folder: Folder path for storing CSV files
    :param classes: List of class names to download
    :param type_csv: One of 'train', 'validation', 'test' or 'all' 
    :return: None
    '''

    directory_list = ['train', 'validation', 'test']
    
    if type_csv != 'all':
        for class_name in classes:
            if not Dataset_folder.endswith('_nl'):
                folder = os.path.join(Dataset_folder, type_csv, class_name, 'Label')
            else:
                folder = os.path.join(Dataset_folder, type_csv, class_name)
            if not os.path.exists(folder):
                os.makedirs(folder)
            filelist = [f for f in os.listdir(folder) if f.endswith(".txt")]
            for f in filelist:
                os.remove(os.path.join(folder, f))

    else:
        for directory in directory_list:
            for class_name in classes:
                if not Dataset_folder.endswith('_nl'):
                    folder = os.path.join(Dataset_folder, directory, class_name, 'Label')
                else:
                    folder = os.path.join(Dataset_folder, directory, class_name)
                if not os.path.exists(folder):
                    os.makedirs(folder)
                filelist = [f for f in os.listdir(folder) if f.endswith(".txt")]
                for f in filelist:
                    os.remove(os.path.join(folder, f))

    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

def filter_dataframe(df, args, attribute):
    """
    Filter the DataFrame based on a specific attribute.

    If the attribute is specified in the arguments, this function filters
    out rows in the DataFrame where the attribute does not match the
    specified value.

    Parameters:
    df (pandas.DataFrame): The DataFrame to filter.
    args (argparse.Namespace): Arguments containing the filter criteria.
    attribute (str): The name of the attribute to filter by.

    Returns:
    pandas.DataFrame: The filtered DataFrame.
    """

    attr_value = getattr(args, attribute, None)
    if attr_value is not None:
        # Construct the DataFrame column name (e.g., 'IsOccluded' from 'image_IsOccluded').
        column_name = attribute.split('_')[1]
        # Find IDs to reject based on the attribute.
        rejected_ids = df.ImageID[df[column_name] != int(attr_value)].values
        # Filter out the rejected IDs.
        df = df[~df.ImageID.isin(rejected_ids)]

    return df

def logo(command):
    """
    Print a simple header for the downloader and the visualizer when selected.

    Parameters:
    command (str): The command for which the logo is being printed ('downloader', 'visualizer', etc.).
    """
    bc = bcolors

    # Generic welcome message
    print(bc.OKGREEN + "Welcome to the Open Image Tool!" + bc.ENDC)

    # Specific messages based on the command
    if command == 'downloader':
        print(bc.OKGREEN + "Downloader Module Activated" + bc.ENDC)
    elif command == 'visualizer':
        print(bc.OKGREEN + "Visualizer Module Activated" + bc.ENDC)
    elif command == 'downloader_ill':
        print(bc.OKGREEN + "Illustrative Downloader Module Activated" + bc.ENDC)
    else:
        print(bc.OKGREEN + "Command Not Recognized" + bc.ENDC)


class bcolors:
    """
    This class defines color codes for terminal output formatting.

    It provides a range of colors suitable for different types of messages,
    enhancing the readability and distinction of console output.
    """

    # Header color: Magenta, suitable for titles or headers.
    HEADER = '\033[95m'

    # Info message prefix: Cyan, for general informational messages.
    INFO = '\033[96m[INFO] | '

    # Download message prefix: Blue, indicating download processes or related information.
    DOWNLOAD = '\033[94m[DOWNLOAD] | '

    # Warning message prefix: Yellow, for warnings or important notices.
    WARNING = '\033[93m[WARN] | '

    # Error message prefix: Red, for errors or critical issues.
    ERROR = '\033[91m[ERROR] | '

    # Success or OK messages: Green, indicating successful operations or statuses.
    OKGREEN = '\033[92m'

    # End of color code: Resets the color to default terminal color.
    ENDC = '\033[0m'

def download_img(folder, dataset_dir, class_name, images_list, threads):
    """
    Download images concurrently using multiple threads.

    This function downloads a list of images into a specified directory,
    organizing them by class. It uses multiple threads to speed up the download process.

    Parameters:
    folder (str): The type of dataset (e.g., 'train', 'validation', 'test').
    dataset_dir (str): The base directory where datasets are stored.
    class_name (str): The name of the class to which the images belong.
    images_list (list): A list of image identifiers to download.
    threads (int): The number of threads to use for concurrent downloads.

    Returns:
    None
    """

    # Create the directory path where images will be downloaded.
    download_dir = os.path.join(dataset_dir, folder, class_name)

    # Ensure the directory exists.
    os.makedirs(download_dir, exist_ok=True)

    # Determine which images need to be downloaded.
    existing_images = [f.split('.')[0] for f in os.listdir(download_dir)]
    images_to_download = list(set(images_list) - set(existing_images))

    # Set up a thread pool for concurrent downloads.
    pool = ThreadPool(threads)

    # Download images if there are any to download.
    if images_to_download:
        print_download_start_info(len(images_to_download), folder)

        # Prepare download commands for each image.
        commands = prepare_download_commands(images_to_download, folder, download_dir)

        # Execute download commands using multiple threads.
        list(tqdm(pool.imap(os.system, commands), total=len(commands)))

        print_download_completion_info()
        pool.close()
        pool.join()
    else:
        print_no_download_needed_info()


def print_download_start_info(number_of_images, folder):
    """
    Print information about the start of the download process.

    Parameters:
    number_of_images (int): The number of images to download.
    folder (str): The dataset folder where images will be downloaded.
    """
    print(bcolors.INFO + f'Download of {number_of_images} images in {folder}.' + bcolors.ENDC)


def prepare_download_commands(images, folder, download_dir):
    """
    Prepare system commands for downloading each image.

    Parameters:
    images (list): List of image IDs to download.
    folder (str): The dataset folder where images will be downloaded.
    download_dir (str): The directory where images will be saved.

    Returns:
    list: A list of system commands for downloading images.
    """
    commands = []
    for image in images:
        file_path = os.path.join(folder, f'{image}.jpg')
        destination = f'"{download_dir}"'
        command = f'aws s3 --no-sign-request --only-show-errors cp s3://open-images-dataset/{file_path} {destination}'
        commands.append(command)

    return commands


def print_download_completion_info():
    """
    Print information indicating the completion of the download process.
    """
    print(bcolors.INFO + 'Done!' + bcolors.ENDC)


def print_no_download_needed_info():
    """
    Print information indicating that no downloads are needed.
    """
    print(bcolors.INFO + 'All images already downloaded.' + bcolors.ENDC)

