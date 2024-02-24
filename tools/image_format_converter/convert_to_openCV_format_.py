"""
 *************************************************************
 *                                                           *
 *    Author: Anthony Mercadante                             *
 *    Project: image_format_converter                        *
 *    Creation Date: February 23, 2024                       *
 *    Mohawk College Student - Student Number: 000361525     *
 *                                                           *
 *************************************************************
 
Converts image files in a specified directory to a format compatible with OpenCV. This script supports a wide range of
input image formats and converts them to either PNG or JPEG format, based on user preference. PNG is used for its
lossless compression, while JPEG can be chosen for its balance between quality and file size.

Dependencies:
- Pillow: For image processing tasks.

Usage:
    python convert_to_opencv_format.py <input_directory> <output_directory> [--format FORMAT]

Arguments:
- input_directory: Directory containing the images to be converted.
- output_directory: Directory where the converted images will be saved.
- --format: Optional. Specify 'PNG' or 'JPEG' as the output format. Defaults to 'PNG'.
"""

import os
from PIL import Image
import argparse

def convert_image_to_format(input_path, output_path, output_format='PNG', quality=95):
    """
    Converts a single image to the specified format.

    Args:
        input_path (str): Path to the input image.
        output_path (str): Path where the converted image will be saved.
        output_format (str): The format to convert the image to ('PNG' or 'JPEG').
        quality (int): The quality level for the output image (relevant for JPEG format).
    """
    try:
        with Image.open(input_path) as img:
            img.save(output_path, output_format, quality=quality)
        print(f"Converted and saved: {output_path}")
    except Exception as e:
        print(f"Failed to convert {input_path}: {e}")

def convert_images_in_directory(input_dir, output_dir, output_format='PNG'):
    """
    Converts all image files in the specified directory to the chosen format.

    Args:
        input_dir (str): Directory containing the images to convert.
        output_dir (str): Directory where the converted images will be saved.
        output_format (str): The format to convert the images to ('PNG' or 'JPEG').
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        output_filename = os.path.splitext(filename)[0] + '.' + output_format.lower()
        output_path = os.path.join(output_dir, output_filename)

        convert_image_to_format(input_path, output_path, output_format)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert images to a format compatible with OpenCV.")
    parser.add_argument("input_dir", type=str, help="Directory containing the images to convert.")
    parser.add_argument("output_dir", type=str, help="Directory where the converted images will be saved.")
    parser.add_argument("--format", type=str, default="PNG", choices=["PNG", "JPEG"],
                        help="Output format (PNG or JPEG). Defaults to PNG.")

    args = parser.parse_args()

    convert_images_in_directory(args.input_dir, args.output_dir, args.format.upper())
