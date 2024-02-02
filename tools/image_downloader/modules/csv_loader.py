import os
import sys
import time
import urllib.request
import pandas as pd

from modules.utilities import bcolors as bc

OID_URL = 'https://storage.googleapis.com/openimages/2018_04/'

def load_ttv_csv(csv_dir, filename, auto_download):
    """
    Load a specified CSV file for Train, Test, or Validation datasets.

    This function checks for the presence of the specified CSV file in the given directory,
    optionally downloads it if missing, and then reads it into a pandas DataFrame.

    Parameters:
    csv_dir (str): Directory where the CSV files are located.
    filename (str): Name of the CSV file to be loaded.
    auto_download (bool): Automatically download the file if it is missing.

    Returns:
    pandas.DataFrame: DataFrame created from the loaded CSV file.
    """
    return load_csv(csv_dir, filename, auto_download)


def load_csv(csv_dir, filename, auto_download):
    """
    Load a CSV file, downloading it if necessary.

    Parameters:
    csv_dir (str): Directory where the CSV files are stored.
    filename (str): Name of the CSV file to load.
    auto_download (bool): Flag to automatically download the file if missing.

    Returns:
    pandas.DataFrame: The loaded DataFrame from the CSV file.
    """
    csv_path = os.path.join(csv_dir, filename)
    if not os.path.isfile(csv_path):
        handle_missing_csv(csv_path, filename, auto_download)
    return pd.read_csv(csv_path)

def handle_missing_csv(csv_path, filename, auto_download):
    """
    Handle the case when a CSV file is missing.

    Parameters:
    csv_path (str): The path to the CSV file.
    filename (str): The name of the missing CSV file.
    auto_download (bool): Flag to automatically download the file if missing.

    Returns:
    None
    """
    print(bc.FAIL + f"Missing the {os.path.basename(filename)} file." + bc.ENDC)

    if auto_download or user_agrees_to_download():
        download_csv(filename, csv_path)
    else:
        sys.exit(1)

def user_agrees_to_download():
    """
    Prompt the user to agree to download the missing file.

    Returns:
    bool: True if the user agrees, False otherwise.
    """
    user_response = input(bc.OKBLUE + "Do you want to download the missing file? [Y/n] " + bc.ENDC)
    return user_response.strip().lower() == 'y'

def download_csv(filename, csv_path):
    """
    Download the specified CSV file.

    Parameters:
    filename (str): The name of the file to download.
    csv_path (str): The path where the file will be saved.

    Returns:
    None
    """
    folder = filename.split('-')[0]
    file_url = f"{OID_URL}{folder if folder != 'class' else ''}/{filename}"

    print(bc.OKBLUE + f"Automatic download of {filename}." + bc.ENDC)
    urllib.request.urlretrieve(file_url, csv_path, download_progress_hook)
    print(f'\n{bc.OKBLUE}File {filename} downloaded into {csv_path}.{bc.ENDC}')

def download_progress_hook(count, block_size, total_size):
    """
    Report hook for displaying the download progress.

    Parameters:
    count (int): Current block number.
    block_size (int): Size of each block.
    total_size (int): Total size of the file.

    Returns:
    None
    """
    global start_time
    if count == 0:
        start_time = time.time()
        return

    elapsed_time = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / ((1024 * elapsed_time) + 1e-5))
    percent = int(progress_size * 100 / (total_size + 1e-5))

    sys.stdout.write(f"\r...{percent}%, {progress_size / (1024 * 1024)} MB, {speed} KB/s, {int(elapsed_time)} seconds passed")
    sys.stdout.flush()
