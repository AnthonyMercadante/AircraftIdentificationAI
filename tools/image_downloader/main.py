import argparse
import os
from downloader import download_all_images
from settings import PrepareFolders, ParamSettings

class ExtractData:
    def __init__(self, file_path, data_type, params):
        self.file_path = file_path
        self.data_type = data_type
        self.params = params
    
    def Download(self):
        """
        Processes and downloads images based on specified parameters and data types.

        This method extracts image data from a specified file, filters images based
        on provided class names and parameters, downloads these images, and creates
        labels in YOLOv5 format.
        """
        # Extract required classes and parameters
        required_params, class_names = ParamSettings(self.params)

        # Read and process the CSV file for image information
        with open(self.file_path, 'r') as file:
            lines = file.readlines()[1:]

        # Dictionary to hold label information and a set for unique image IDs
        labels = dict()
        img_ids = set()
        
        # Process each line in the file
        for line in lines:
            info = line.split(',')
            img_id, class_name, *bbox = info[0], info[2], info[4:8]
            img_params = info[8:]
            img_params[4] = img_params[4][0]

            # Check if image matches required parameters
            is_matched = all(param == img_param or param == '2' for param, img_param in zip(required_params, img_params))
            
            # Add image to the set and update labels if conditions are met
            if class_name in class_names and is_matched:
                img_ids.add(img_id)
                bbox_labels = [class_names[class_name], *bbox]
                labels.setdefault(img_id, []).append(bbox_labels)

        # Write image IDs to a file for download
        path_to_img_ids = "dataset/img_ids.txt"
        with open(path_to_img_ids, 'w') as fp:
            for img_id in img_ids:
                fp.write(f"{self.data_type}/{img_id}\n")

        # Download images using the downloader module
        download_all_images({
            'image_list': path_to_img_ids,
            'download_folder': "dataset/images",
            'num_processes': 5
        })

        # Create labels in YOLOv5 format
        for img_name, classes in labels.items():
            with open(f"dataset/labels/{img_name}.txt", 'w') as f:
                for class_label in classes:
                    class_id, *bbox_coords = class_label
                    x, y, w, h = [float(coord) for coord in bbox_coords]
                    x_center = (x + w) / 2
                    y_center = (y + h) / 2
                    width = w - x
                    height = h - y
                    f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")


if __name__ == "__main__":
    # Set up argument parser for command-line options
    parser = argparse.ArgumentParser(description='Download and process data from OpenImages')
    parser.add_argument('--isOccluded', type=int, default=2, help='Flag for occlusion (default: 2)')
    parser.add_argument('--isTruncated', type=int, default=2, help='Flag for truncation (default: 2)')
    parser.add_argument('--isGroupOf', type=int, default=2, help='Flag for group of objects (default: 2)')
    parser.add_argument('--isDepiction', type=int, default=2, help='Flag for depiction (default: 2)')
    parser.add_argument('--isInside', type=int, default=2, help='Flag for inside (default: 2)')
    parser.add_argument('--classes', nargs='+', type=str, required=True, help='List of classes to download')

    args = vars(parser.parse_args())

    # Prepare folders and download labels
    PrepareFolders()

    # Process and download data for each dataset split
    ExtractData("oidv6-train.csv", 'train', args).Download()
    ExtractData("oidv7-validation.csv", 'validation', args).Download()
    ExtractData("oidv7-test.csv", 'test', args).Download()
