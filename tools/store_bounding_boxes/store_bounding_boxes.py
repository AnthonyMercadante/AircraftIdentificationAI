"""
 *************************************************************
 *                                                           *
 *    Author: Anthony Mercadante                             *
 *    Project: Aircraft Identification AI                    *
 *    Creation Date: February 19, 2024                       *
 *    Mohawk College Student - Student Number: 000361525     *
 *                                                           *
 *************************************************************
 
This module contains the `store_bounding_boxes` function, 
which is designed to process a folder of images, 
detect objects within those images using a specified YOLO model, 
and store the bounding boxes of detected objects. 
Specifically, it focuses on detecting aircrafts and outputs the 
normalized bounding box coordinates to a labels folder within the 
specified output directory. It also saves the processed images to an output directory.

Parameters:
- model_path (str): Path to the trained YOLO model file.
- images_folder (str): Directory containing the images to be processed.
- output_file (str): Path to the file where the bounding box data will be stored (currently not used in the function).
- output_images_folder (str): Directory where the processed images and labels will be saved.
- config_file (Optional[str]): Path to a configuration file in YAML format containing class names. Default is None.

The script assumes that the 'Aircraft' class is at index 0 in the model's class definitions. 
If the class index is different, or multiple classes are to be processed, adjustments to the code will be necessary.
"""
import yaml
from ultralytics import YOLO
import os
import cv2

def store_bounding_boxes(model_path, images_folder, output_file, output_images_folder, config_file=None):
    """
    Processes images in a specified folder, detects objects using YOLO, and stores bounding boxes for aircraft detections.

    Args:
        model_path (str): Path to the trained YOLO model.
        images_folder (str): Folder containing images to process.
        output_file (str): Path to save bounding box data (not currently used).
        output_images_folder (str): Folder to save processed images and labels.
        config_file (str, optional): Path to a YAML config file specifying class names. Defaults to None.
    """
    print("Loading model...")
    model = YOLO(model_path)  # Load the YOLO model from the specified path

    aircraft_class_index = 0  # Index for 'Aircraft' class, adjust based on your model's class definitions
    class_names = None
    if config_file:
        # Load class names from the provided config file if available
        with open(config_file, 'r', encoding='utf-8-sig') as f:
            config = yaml.safe_load(f)
            class_names = config['names']
            print(f"Class names loaded from config: {class_names}")

    # Ensure the output directory for images exists, create if necessary
    if not os.path.exists(output_images_folder):
        os.makedirs(output_images_folder)
        print(f"Created output images folder: {output_images_folder}")

    # Create a subdirectory for labels within the output images folder
    labels_folder = os.path.join(output_images_folder, "labels")
    if not os.path.exists(labels_folder):
        os.makedirs(labels_folder)
        print(f"Created labels folder: {labels_folder}")

    # Process each image in the specified folder
    for image_name in os.listdir(images_folder):
        image_path = os.path.join(images_folder, image_name)
        # Skip files that are not images
        if not image_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            continue

        print(f"Processing image: {image_path}")
        image = cv2.imread(image_path)  # Load the image
        if image is None:
            print(f"Failed to load image: {image_path}")
            continue

        image_height, image_width = image.shape[:2]  # Get image dimensions
        results = model.predict(image, verbose=False)  # Run detection

        # Prepare to write detected bounding boxes to a label file
        label_file_path = os.path.join(labels_folder, os.path.splitext(image_name)[0] + '.txt')
        with open(label_file_path, 'w') as label_file:
            for result in results:
                # Filter detections for the aircraft class with confidence > 0.25
                for box, conf, cls in zip(result.boxes.xyxy, result.boxes.conf, result.boxes.cls):
                    if cls == aircraft_class_index and conf > 0.25:
                        # Normalize and write bounding box coordinates to the label file
                        x1, y1, x2, y2 = map(float, box)
                        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                        w, h = x2 - x1, y2 - y1
                        cx_norm, cy_norm = cx / image_width, cy / image_height
                        w_norm, h_norm = w / image_width, h / image_height

                        label_file.write(f"{int(cls)} {cx_norm} {cy_norm} {w_norm} {h_norm}\n")

        # Save the processed image to the output directory
        output_image_path = os.path.join(output_images_folder, image_name)
        if cv2.imwrite(output_image_path, image):
            print(f"Image saved: {output_image_path}")
        else:
            print(f"Error saving image: {output_image_path}")

# Example call to the function
store_bounding_boxes('../../runs/detect/train4/weights/best.pt', 'Single Engine', 'bounding_boxes.csv', 'output_images final single engine', 'test-config.yaml')
