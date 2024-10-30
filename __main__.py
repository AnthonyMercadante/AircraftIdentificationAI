# *************************************************************
# *                                                           *
# *    Author: Anthony Mercadante                             *
# *    Project: Aircraft Identification AI                    *
# *    Creation Date: February 4, 2024                        *
# *    Mohawk College Student - Student Number: 000361525     *
# *                                                           *
# *************************************************************
import ultralytics
import yaml
from ultralytics import YOLO
import torch
import json
import os

def train_yolo_model():
    """
    Trains a YOLO model using the Ultralytics framework.

    This function sets up the training environment (device selection), loads the model
    configuration from a YAML file, and initiates the training process. It's designed to
    work with YOLO models, particularly suited for real-time object detection tasks.
    """

    # Device Configuration
    # Checks if a GPU is available for training and sets the device accordingly.
    # Using a GPU (cuda) is recommended for faster training, but if unavailable, it defaults to CPU.
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")

    # Model Initialization
    # Loads a YOLO model defined in 'yolov8n.yaml'.
    # This YAML file should contain the model architecture. You need to specify the correct path
    # and filename according to your model configuration.
    model = YOLO("runs/detect/train4/weights/best.pt")  # Build a new model from scratch

    # Model Training
    # Starts the training process of the model using the data and configuration specified in 'config.yaml'.
    # The 'epochs' parameter defines the number of training cycles the model will undergo.
    # The 'config.yaml' should contain the necessary training configurations, including dataset path, 
    # batch size, learning rate, etc.
    results = model.train(data="training-config.yaml", epochs=300)  # Train the model
    
    # Saving the Model
    save_path = 'AircraftIdentificationAI.pth'

    # There are two common ways to save a model in PyTorch:
    # 1. Save the entire model using `torch.save(model, save_path)`
    # 2. Save only the state dictionary using `torch.save(model.state_dict(), save_path)`

    # Option 2: Recommended for flexibility
    torch.save(model.state_dict(), save_path)
    print(f"Model saved to {save_path}")
    

def test_yolo_model(model_path, images_folder, config_file=None):
    """
    Tests a YOLO model on a folder of unseen images and stores the results in a JSON file.

    Args:
        model_path (str): Path to the trained model.
        images_folder (str): Directory containing unseen images to test the model on.
        config_file (str, optional): Path to the configuration file.
    """

     # Initialize the model
    model = YOLO(model_path)

    # Load class names from the config file
    if config_file:
        with open(config_file, 'r', encoding='utf-8-sig') as f:
            config = yaml.safe_load(f)
            class_names_dict = config['names']
            # Convert class names dict to a list where index corresponds to class index
            class_names = [None] * len(class_names_dict)
            for key_str, name in class_names_dict.items():
                index = int(key_str)
                class_names[index] = name
    else:
        # Default class names if config not provided
        class_names = ['Aircraft', 'Jet', 'Multi Engine', 'Single Engine']

    # Prepare to collect results
    results_list = []

    # Define supported image extensions
    supported_extensions = ('.bmp', '.dng', '.jpeg', '.jpg', '.mpo', '.png', '.tif', '.tiff', '.webp', '.pfm')

    # Iterate over images in the folder
    for image_name in os.listdir(images_folder):
        image_path = os.path.join(images_folder, image_name)
        # Check if the file has a supported image extension
        if image_name.lower().endswith(supported_extensions):
            try:
                # Run inference
                results = model(image_path)

                # Process results
                image_results = {
                    'image_name': image_name,
                    'detections': []
                }

                for result in results:
                    boxes = result.boxes  # Boxes object for bbox outputs
                    for box in boxes:
                        cls_index = int(box.cls.item())
                        conf = float(box.conf.item())
                        coords = box.xyxy.tolist()  # [x1, y1, x2, y2]

                        detection = {
                            'class_index': cls_index,
                            'class_name': class_names[cls_index],
                            'confidence': conf,
                            'bbox': coords  # [x1, y1, x2, y2]
                        }
                        image_results['detections'].append(detection)

                # Append image results to the main results list
                results_list.append(image_results)

                # Optionally, print out detections for this image
                if image_results['detections']:
                    print(f"Image: {image_name} - Detections:")
                    for det in image_results['detections']:
                        print(f"    Detected {det['class_name']} with confidence {det['confidence']:.2f}")
                        print(f"        Bounding box: {det['bbox']}")
                else:
                    print(f"Image: {image_name} - No detections")
            except Exception as e:
                print(f"Error processing image {image_name}: {e}")
                continue  # Skip this image and continue with the next
        else:
            print(f"Skipping file {image_name}: Unsupported file extension")
            continue  # Skip this file and continue with the next

    # After processing all images, save results to a JSON file
    output_file = 'test_results.json'
    with open(output_file, 'w') as f:
        json.dump(results_list, f, indent=4)
    print(f"Results saved to {output_file}")






# Main Execution
# Checks if the script is the main program and calls the train_yolo_model function.
# This is a standard Python practice to ensure that the script runs only when it is executed directly,
# not when imported as a module in another script.
if __name__ == '__main__':
      #train_yolo_model() # <-- FOR TRAINING THE MODEL ONLY
     test_yolo_model('runs/detect/train12/weights/best.pt', 'dataset/unseen_images', 'test-config.yaml')
    
