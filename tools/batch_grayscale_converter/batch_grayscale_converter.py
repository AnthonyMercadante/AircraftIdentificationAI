# *************************************************************
# *                                                           *
# *    Author: Anthony Mercadante                             *
# *    Project: batch_grayscale_converter tool                *
# *    Creation Date: February 6, 2024                        *
# *    Mohawk College Student - Student Number: 000361525     *
# *                                                           *
# *************************************************************

import os
from PIL import Image

def grayscale_images_in_folder(folder_path):
    """
    Convert all images in the specified folder to grayscale.

    This function iterates through all image files in the given folder,
    converts them to grayscale, and saves the grayscale images in the
    same folder with a '_grayscale' suffix in the filename.

    Supported image formats: .png, .jpg, .jpeg, .tiff, .bmp, .gif

    Parameters:
    folder_path (str): Path to the folder containing images.

    Returns:
    None
    """
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            file_path = os.path.join(folder_path, filename)
            try:
                with Image.open(file_path) as img:
                    grayscale_img = img.convert('L')
                    grayscale_filename = f"{os.path.splitext(filename)[0]}_grayscale.jpg"
                    grayscale_img.save(os.path.join(folder_path, grayscale_filename))
                print(f"Converted '{filename}' to grayscale.")
            except Exception as e:
                print(f"Failed to convert '{filename}'. Error: {e}")

if __name__ == "__main__":
    # Example usage: Replace 'your_folder_path' with the actual folder path
    folder_path = 'your_folder_path'
    grayscale_images_in_folder(folder_path)

