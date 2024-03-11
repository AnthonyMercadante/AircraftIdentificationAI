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
    

def test_yolo_model(model_path, images_folder, config_file):
    """
    Tests a YOLO model on a folder of unseen images to specifically identify "Avro Lancaster"
    or "Hawker Hurricane" after confirming an object is an "Aircraft".

    Args:
        model_path (str): Path to the trained model.
        images_folder (str): Directory containing unseen images to test the model on.
        config_file (str, optional): Path to the configuration file.
    """

    # Initialize the model from the model configuration used during training
    model = YOLO(model_path)
    
    aircraft_class_index = 0
    avro_lancaster_class_index = 1
    hawker_hurricane_class_index = 2
    
    # Load class names from config if provided
    if config_file:
        with open(config_file, 'r', encoding='utf-8-sig') as f:
            config = yaml.safe_load(f)
            class_names = config['names']
    else:
        # Default class names if config not provided or failed to load
        class_names = ['Aircraft', 'Avro Lancaster', 'Hawker Hurricane']

    # Iterate over images in the folder
    for image_name in os.listdir(images_folder):
        image_path = os.path.join(images_folder, image_name)
        results = model(image_path)  # This returns a Results object

        if hasattr(results, 'pred') and results.pred is not None:
            detections = results.pred[0]  # Assuming 'pred' contains detection results
            found_specific_aircraft = False

            for *box, conf, cls in detections:
                cls_index = int(cls)  # Ensuring class index is an integer
                if conf > 0.25 and cls_index in [avro_lancaster_class_index, hawker_hurricane_class_index]:
                    aircraft_type = class_names[cls_index]
                    print(f"Image: {image_name} - Detected {aircraft_type} with confidence: {conf:.2f}")
                    print(f"    Bounding box: {box}")
                    found_specific_aircraft = True

            if not found_specific_aircraft:
                print(f"Image: {image_name} - No Avro Lancaster or Hawker Hurricane Detected")






# Main Execution
# Checks if the script is the main program and calls the train_yolo_model function.
# This is a standard Python practice to ensure that the script runs only when it is executed directly,
# not when imported as a module in another script.
if __name__ == '__main__':
      train_yolo_model() # <-- FOR TRAINING THE MODEL ONLY
     # test_yolo_model('runs/detect/train7/weights/best.pt', 'dataset/images', 'test-config.yaml')
    
