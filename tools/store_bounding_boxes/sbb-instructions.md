# Store Bounding Boxes Tool

The `store_bounding_boxes.py` script is designed to automate the process of detecting aircraft in images and generating annotation labels. These labels can then be used for training machine learning models, particularly for object detection tasks. This document provides detailed instructions on how to set up and use this script effectively.

## Purpose

The primary purpose of this tool is to process a directory of unannotated images, identify aircraft within these images using a pre-trained YOLO model, and generate corresponding annotation labels. These labels are saved in a format suitable for training purposes, facilitating the development of more accurate object detection models.

## Prerequisites

Before you start, ensure you have the following prerequisites installed on your system:

- Python 3.6 or higher
- OpenCV library (`cv2`)
- PyYAML for YAML file handling
- The Ultralytics YOLO package for object detection

You can install the required Python packages using pip:

```sh
pip install opencv-python pyyaml ultralytics
```

## Configuration

1. **Model Path**: You need a pre-trained YOLO model file. The path to this file is required as `model_path`.

2. **Images Folder**: The directory containing the images you want to process. Ensure all images are in formats supported by OpenCV (e.g., jpg, jpeg, png, bmp).

3. **Output Images Folder**: Specify a directory where processed images and generated labels will be stored. The script will create this directory if it does not exist.

4. **Config File (Optional)**: A YAML file specifying the names of the classes recognized by your model. This is optional but recommended for clarity.

## Usage

To use the `store_bounding_boxes.py` script, follow these steps:

1. Prepare your images by placing them in a designated folder.

2. Ensure your YOLO model file is accessible and note its path.

3. Decide on a folder where the output images and labels will be stored.

4. If you have a configuration file for class names, ensure it is formatted correctly and accessible.

5. Execute the script with the necessary arguments. Here is an example command:

    ```sh
    python store_bounding_boxes.py --model_path /path/to/yolo/model --images_folder /path/to/images --output_file /path/to/output/bounding_boxes.csv --output_images_folder /path/to/output/images --config_file /path/to/config.yaml
    ```

Replace the paths with those relevant to your setup.

## Output

The script will process each image in the specified folder, detect aircraft, and generate annotation labels. These labels are saved in a "labels" subfolder within the output images folder. Each label file corresponds to an image and contains the normalized bounding box coordinates and class index for detected aircraft.

Processed images are saved in the output images folder, allowing for visual verification of the detection results.

## Note

This script is configured to detect objects classified as "Aircraft" by default. If your model uses different classes or indexes, you will need to modify the script accordingly.