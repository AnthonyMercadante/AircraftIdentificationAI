# *************************************************************
# *                                                           *
# *    Author: Anthony Mercadante                             *
# *    Project: image_downloader tool                         *
# *    Creation Date: February 4, 2024                        *
# *    Mohawk College Student - Student Number: 000361525     *
# *                                                           *
# *************************************************************

import argparse
import os
import csv
from downloader import download_all_images
from settings import PrepareFolders, ParamSettings

# Class definition for extracting and processing data from a CSV file.
class ExtractData:
    def __init__(self, file_path, data_type, params):
        """
        Initializes the ExtractData object.

        Parameters:
        file_path (str): Path to the CSV file containing image data.
        data_type (str): Type of data (e.g., 'train', 'validation', 'test').
        params (dict): Parameters for filtering and downloading images.
        """
        self.file_path = file_path
        self.data_type = data_type
        self.params = params

    @staticmethod
    def correct_bbox_values(xmin, xmax, ymin, ymax):
        """
        Corrects bounding box values to ensure xmin < xmax and ymin < ymax.

        Parameters:
        xmin, xmax, ymin, ymax (float): Coordinates of the bounding box.

        Returns:
        tuple: Corrected coordinates of the bounding box.
        """
        xmin, xmax = min(xmin, xmax), max(xmin, xmax)
        ymin, ymax = min(ymin, ymax), max(ymin, ymax)
        return xmin, xmax, ymin, ymax

    def Download(self):
        """
        Processes the CSV file, filters images based on specified parameters,
        downloads the images, and writes the image IDs and labels to files.
        """
        required_params, class_names = ParamSettings(self.params)

        labels = dict()
        img_ids = set()

        with open(self.file_path, newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row

            for row in reader:
                # Extract and process image and bounding box data from each row
                img_id, class_name, xmin, xmax, ymin, ymax = row[0], row[2], float(row[4]), float(row[5]), float(row[6]), float(row[7])
                img_params = row[8:]
                img_params[4] = img_params[4][0]

                is_matched = all(param == img_param or param == '2' for param, img_param in zip(required_params, img_params))

                if class_name in class_names and is_matched:
                    img_ids.add(img_id)
                    xmin, xmax, ymin, ymax = self.correct_bbox_values(xmin, xmax, ymin, ymax)
                    x_center, y_center, width, height = (xmin + xmax) / 2, (ymin + ymax) / 2, xmax - xmin, ymax - ymin
                    labels.setdefault(img_id, []).append([class_names[class_name], x_center, y_center, width, height])
        # Write image IDs and labels to respective files
        path_to_img_ids = "../../dataset/img_ids.txt"
        with open(path_to_img_ids, 'w') as fp:
            for img_id in img_ids:
                fp.write(f"{self.data_type}/{img_id}\n")
        # Initiates the download of images using the downloader module
        download_all_images({
            'image_list': path_to_img_ids,
            'download_folder': "../../dataset/images",
            'num_processes': 5
        })

        for img_name, bbox_data in labels.items():
            with open(f"../../dataset/labels/{img_name}.txt", 'w') as f:
                for data in bbox_data:
                    f.write(f"{' '.join(map(str, data))}\n")

if __name__ == "__main__":
    # Command-line interface for the script
    parser = argparse.ArgumentParser(description='Download and process data from OpenImages')
    # Define command-line arguments for image filtering parameters and classes
    parser.add_argument('--isOccluded', type=int, default=2, help='Flag for occlusion (default: 2)')
    parser.add_argument('--isTruncated', type=int, default=2, help='Flag for truncation (default: 2)')
    parser.add_argument('--isGroupOf', type=int, default=2, help='Flag for group of objects (default: 2)')
    parser.add_argument('--isDepiction', type=int, default=2, help='Flag for depiction (default: 2)')
    parser.add_argument('--isInside', type=int, default=2, help='Flag for inside (default: 2)')
    parser.add_argument('--classes', nargs='+', type=str, required=True, help='List of classes to download')
    
    args = vars(parser.parse_args())
    # Prepare folders for storing downloaded data
    PrepareFolders()
    # Create ExtractData instances for training, validation, and test data and start download process
    ExtractData("oidv6-train.csv", 'train', args).Download()
    ExtractData("oidv7-validation.csv", 'validation', args).Download()
    ExtractData("oidv7-test.csv", 'test', args).Download()

