# *************************************************************
# *                                                           *
# *    Author: Anthony Mercadante                             *
# *    Project: Aircraft Identification AI                    *
# *    Creation Date: February 20, 2024                        *
# *    Mohawk College Student - Student Number: 000361525     *
# *                                                           *
# *************************************************************

import yaml
from ultralytics import YOLO
import os
import csv
import cv2 


def store_bounding_boxes(model_path, images_folder, output_file, output_images_folder, config_file=None):
    """
    Detects aircraft in an unseen dataset, draws bounding boxes around them, stores bounding 
    box data in a CSV file, and saves the images with bounding boxes to a specified folder.
    """

    print("Loading model...")
    model = YOLO(model_path)

    aircraft_class_index = 4  # Assuming 'Aircraft' is at index 4
    class_names = None
    if config_file:
        with open(config_file, 'r', encoding='utf-8-sig') as f:
            config = yaml.safe_load(f)
            class_names = config['names']
            print(f"Class names loaded from config: {class_names}")

    if not os.path.exists(output_images_folder):
        os.makedirs(output_images_folder)
        print(f"Created output images folder: {output_images_folder}")

    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['image_path', 'x1', 'y1', 'x2', 'y2', 'class_name'])

        for image_name in os.listdir(images_folder):
            image_path = os.path.join(images_folder, image_name)
            if not image_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                continue

            print(f"Processing image: {image_path}")
            image = cv2.imread(image_path)
            if image is None:
                print(f"Failed to load image: {image_path}")
                continue

            results = model.predict(image, verbose=False)

            # Assuming results is a list of detection results
            for result in results:
                # Assuming result has the attributes boxes, conf, and cls
                for box, conf, cls in zip(result.boxes.xyxy, result.boxes.conf, result.boxes.cls):
                    print(f"Class ID: {int(cls)}, Confidence: {conf.item():.4f}, Class Name: {class_names.get(int(cls), 'Unknown')}")
                    if cls == aircraft_class_index and conf > 0.25:
                        x1, y1, x2, y2 = map(int, box)
                        class_name = class_names[int(cls)] if class_names else "Aircraft"
                        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(image, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                        csv_writer.writerow([image_path, x1, y1, x2, y2, class_name])
                        print(f"Bounding box drawn: {x1}, {y1}, {x2}, {y2}, Class: {class_name}")

            output_image_path = os.path.join(output_images_folder, image_name)
            if cv2.imwrite(output_image_path, image):
                print(f"Image saved: {output_image_path}")
            else:
                print(f"Error saving image: {output_image_path}")
                

store_bounding_boxes('../../yolov8n.pt', '../../dataset/unseen_images/avro_lancaster', 'bounding_boxes.csv', 'output_images', 'test-config.yaml')