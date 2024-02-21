import yaml
from ultralytics import YOLO
import os
import cv2

def store_bounding_boxes(model_path, images_folder, output_file, output_images_folder, config_file=None):
    print("Loading model...")
    model = YOLO(model_path)

    aircraft_class_index = 0  # Assuming 'Aircraft' is at index 0, adjust if necessary
    class_names = None
    if config_file:
        with open(config_file, 'r', encoding='utf-8-sig') as f:
            config = yaml.safe_load(f)
            class_names = config['names']
            print(f"Class names loaded from config: {class_names}")

    # Create output_images folder if it doesn't exist
    if not os.path.exists(output_images_folder):
        os.makedirs(output_images_folder)
        print(f"Created output images folder: {output_images_folder}")

    # Create labels folder inside the output_images folder
    labels_folder = os.path.join(output_images_folder, "labels")
    if not os.path.exists(labels_folder):
        os.makedirs(labels_folder)
        print(f"Created labels folder: {labels_folder}")

    for image_name in os.listdir(images_folder):
        image_path = os.path.join(images_folder, image_name)
        if not image_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            continue

        print(f"Processing image: {image_path}")
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to load image: {image_path}")
            continue

        image_height, image_width = image.shape[:2]
        results = model.predict(image, verbose=False)

        label_file_path = os.path.join(labels_folder, os.path.splitext(image_name)[0] + '.txt')
        with open(label_file_path, 'w') as label_file:
            for result in results:
                for box, conf, cls in zip(result.boxes.xyxy, result.boxes.conf, result.boxes.cls):
                    if cls == aircraft_class_index and conf > 0.25:
                        x1, y1, x2, y2 = map(float, box)
                        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                        w, h = x2 - x1, y2 - y1
                        cx_norm, cy_norm = cx / image_width, cy / image_height
                        w_norm, h_norm = w / image_width, h / image_height

                        label_file.write(f"{int(cls)} {cx_norm} {cy_norm} {w_norm} {h_norm}\n")

        output_image_path = os.path.join(output_images_folder, image_name)
        if cv2.imwrite(output_image_path, image):
            print(f"Image saved: {output_image_path}")
        else:
            print(f"Error saving image: {output_image_path}")

store_bounding_boxes('../../runs/detect/train4/weights/best.pt', '../../dataset/unseen_images/avro_lancaster', 'bounding_boxes.csv', 'output_images', 'test-config.yaml')
