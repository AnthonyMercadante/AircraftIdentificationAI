# *************************************************************
# *                                                           *
# *    Author: Anthony Mercadante                             *
# *    Project: image_downloader tool                         *
# *    Creation Date: February 4, 2024                        *
# *    Mohawk College Student - Student Number: 000361525     *
# *                                                           *
# *************************************************************


import argparse
from concurrent import futures
import os
import re
import sys

import boto3
import botocore
import tqdm

# Constants for bucket name and regular expression pattern for image validation
BUCKET_NAME = 'open-images-dataset'
IMAGE_PATTERN_REGEX = r'(test|train|validation|challenge2018)/([a-fA-F0-9]*)'


def check_and_homogenize_one_image(image):
    """
    Validates and processes one image string.

    This function uses a regular expression to validate and extract the image split
    and ID from the given image string.

    Args:
        image (str): The image string to be processed.

    Yields:
        tuple: A tuple containing the split and image ID.
    """
    split, image_id = re.match(IMAGE_PATTERN_REGEX, image).groups()
    yield split, image_id


def check_and_homogenize_image_list(image_list):
    """
    Processes and validates a list of image strings.

    This function iterates over an image list, validating and processing each image
    string. If an image string is invalid, it raises a ValueError.

    Args:
        image_list (list): The list of image strings to process.

    Yields:
        Generator: A generator of tuples containing the split and image ID.
    """
    for line_number, image in enumerate(image_list):
        try:
            yield from check_and_homogenize_one_image(image)
        except (ValueError, AttributeError):
            raise ValueError(
                f'ERROR in line {line_number} of the image list. The following image '
                f'string is not recognized: "{image}".')


def read_image_list_file(image_list_file):
    """
    Reads an image list file.

    This function opens and iterates over an image list file, yielding each line
    after stripping whitespace and removing the '.jpg' extension.

    Args:
        image_list_file (str): The filename of the image list file.

    Yields:
        str: The processed line from the file.
    """
    with open(image_list_file, 'r') as file:
        for line in file:
            yield line.strip().replace('.jpg', '')


def download_one_image(bucket, split, image_id, download_folder):
    """
    Downloads a single image from the S3 bucket.

    This function attempts to download an image from the S3 bucket based on the
    provided split and image ID. If the download fails, it exits the program.

    Args:
        bucket (boto3.Bucket): The S3 bucket object.
        split (str): The dataset split (e.g., 'train', 'test').
        image_id (str): The ID of the image.
        download_folder (str): The folder where the image will be downloaded.
    """
    try:
        bucket.download_file(
            f'{split}/{image_id}.jpg', os.path.join(download_folder, f'{image_id}.jpg'))
    except botocore.exceptions.ClientError as exception:
        sys.exit(
            f'ERROR when downloading image `{split}/{image_id}`: {str(exception)}')


def download_all_images(args):
    """
    Downloads all images as specified in the input file.

    This function sets up the S3 bucket connection, prepares the download folder,
    reads and processes the image list file, and then uses concurrent futures
    to download all images in parallel.

    Args:
        args (dict): A dictionary of command-line arguments.
    """
    # Setup S3 bucket connection
    bucket = boto3.resource(
        's3', config=botocore.config.Config(
            signature_version=botocore.UNSIGNED)).Bucket(BUCKET_NAME)

    # Determine download folder and create if it doesn't exist
    download_folder = args['download_folder'] or os.getcwd()
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Read and process image list file
    try:
        image_list = list(
            check_and_homogenize_image_list(
                read_image_list_file(args['image_list'])))
    except ValueError as exception:
        sys.exit(exception)

    # Download images using concurrent futures
    progress_bar = tqdm.tqdm(
        total=len(image_list), desc='Downloading images', leave=True)
    with futures.ThreadPoolExecutor(max_workers=args['num_processes']) as executor:
        download_futures = [
            executor.submit(download_one_image, bucket, split, image_id, download_folder)
            for (split, image_id) in image_list
        ]
        for future in futures.as_completed(download_futures):
            future.result()
            progress_bar.update(1)
    progress_bar.close()


if __name__ == '__main__':
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(
        description='Script to download images from Open Images Dataset',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'image_list',
        type=str,
        help=('Filename containing the split and image IDs of the images to '
              'download.'))
    parser.add_argument(
        '--num_processes',
        type=int,
        default=5,
        help='Number of parallel processes to use for downloading images (default is 5).')
    parser.add_argument(
        '--download_folder',
        type=str,
        help='Folder to download the images (default is the current working directory).')

    # Parse and pass arguments to the download function
    download_all_images(vars(parser.parse_args()))

