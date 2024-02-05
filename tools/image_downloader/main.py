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

class ExtractData:
    def __init__(self, file_path, data_type, params):
        self.file_path = file_path
        self.data_type = data_type
        self.params = params

    @staticmethod
    def correct_bbox_values(xmin, xmax, ymin, ymax):
        xmin, xmax = min(xmin, xmax), max(xmin, xmax)
        ymin, ymax = min(ymin, ymax), max(ymin, ymax)
        return xmin, xmax, ymin, ymax

    def Download(self):
        required_params, class_names = ParamSettings(self.params)

        labels = dict()
        img_ids = set()

        with open(self.file_path, newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row

            for row in reader:
                img_id, class_name, xmin, xmax, ymin, ymax = row[0], row[2], float(row[4]), float(row[5]), float(row[6]), float(row[7])
                img_params = row[8:]
                img_params[4] = img_params[4][0]

                is_matched = all(param == img_param or param == '2' for param, img_param in zip(required_params, img_params))

                if class_name in class_names and is_matched:
                    img_ids.add(img_id)
                    xmin, xmax, ymin, ymax = self.correct_bbox_values(xmin, xmax, ymin, ymax)
                    x_center, y_center, width, height = (xmin + xmax) / 2, (ymin + ymax) / 2, xmax - xmin, ymax - ymin
                    labels.setdefault(img_id, []).append([class_names[class_name], x_center, y_center, width, height])

        path_to_img_ids = "../../dataset/img_ids.txt"
        with open(path_to_img_ids, 'w') as fp:
            for img_id in img_ids:
                fp.write(f"{self.data_type}/{img_id}\n")

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
    parser = argparse.ArgumentParser(description='Download and process data from OpenImages')
    parser.add_argument('--isOccluded', type=int, default=2, help='Flag for occlusion (default: 2)')
    parser.add_argument('--isTruncated', type=int, default=2, help='Flag for truncation (default: 2)')
    parser.add_argument('--isGroupOf', type=int, default=2, help='Flag for group of objects (default: 2)')
    parser.add_argument('--isDepiction', type=int, default=2, help='Flag for depiction (default: 2)')
    parser.add_argument('--isInside', type=int, default=2, help='Flag for inside (default: 2)')
    parser.add_argument('--classes', nargs='+', type=str, required=True, help='List of classes to download')
    
    args = vars(parser.parse_args())

    PrepareFolders()
    ExtractData("oidv6-train.csv", 'train', args).Download()
    ExtractData("oidv7-validation.csv", 'validation', args).Download()
    ExtractData("oidv7-test.csv", 'test', args).Download()

