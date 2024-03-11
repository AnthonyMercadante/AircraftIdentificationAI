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
    model = YOLO("yolov8n.yaml")  # Build a new model from scratch

    # Model Training
    # Starts the training process of the model using the data and configuration specified in 'config.yaml'.
    # The 'epochs' parameter defines the number of training cycles the model will undergo.
    # The 'config.yaml' should contain the necessary training configurations, including dataset path, 
    # batch size, learning rate, etc.
    results = model.train(data="training-config.yaml", epochs=300)  # Train the model
    

def test_yolo_model(model_path, images_folder, config_file):
    """
    Tests a YOLO model on a folder of unseen images and identifies "Aircraft" (class index 0).

    Args:
        model_path (str): Path to the trained model.
        images_folder (str): Directory containing unseen images to test the model on.
        config_file (str, optional): Path to the configuration file.
    """

    # Load the trained model
    model = YOLO(model_path)  # Removed .eval() as it might not be necessary or correct depending on the API

    # Default class index and name for "Aircraft" & Avro Lancaster
    aircraft_class_index = 0
    aircraft_class_name = "Aircraft"
    avro_lancaster_class_index = 1
    avro_lancaster_class_name = "Avro Lancaster"

    # Read configuration if provided
    if config_file:
        with open(config_file, 'r', encoding='utf-8-sig') as f:
            config = yaml.safe_load(f)
            class_names = config['names']
            # Use the integer index directly without converting to string
            aircraft_class_name = class_names[aircraft_class_index]

    # Iterate over images in the folder
    for image_name in os.listdir(images_folder):
        image_path = os.path.join(images_folder, image_name)

        # Perform inference and process results
        results = model(image_path)  # This returns a Results object

        # If results is directly accessible, we may need to iterate or directly access its properties
        # This assumes 'results' is properly a Results object or a structure you can directly access
        if hasattr(results, 'pred') and results.pred is not None:
            detections = results.pred[0]  # Assuming 'pred' contains detection results and is structured accordingly
            aircraft_detected = False

            for *box, conf, cls in detections:
                # Check for Aircraft
                if cls == aircraft_class_index and conf > 0.25:
                    print(f"Image: {image_name} - Detected {aircraft_class_name} with confidence: {conf:.2f}")
                    print(f"    Bounding box: {box}")
                # Check for Avro Lancaster
                elif cls == avro_lancaster_class_index and conf > 0.25:
                    print(f"Image: {image_name} - Detected {avro_lancaster_class_name} with confidence: {conf:.2f}")
                    print(f"    Bounding box: {box}")

            if not aircraft_detected:
                print(f"Image: {image_name} - No Aircraft Detected")





# Main Execution
# Checks if the script is the main program and calls the train_yolo_model function.
# This is a standard Python practice to ensure that the script runs only when it is executed directly,
# not when imported as a module in another script.
if __name__ == '__main__':
     train_yolo_model() # <-- FOR TRAINING THE MODEL ONLY
     # test_yolo_model('runs/detect/train4/weights/best.pt', 'dataset/unseen_images/avro_lancaster', 'test-config.yaml')
    
