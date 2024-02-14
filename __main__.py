# *************************************************************
# *                                                           *
# *    Author: Anthony Mercadante                             *
# *    Project: Aircraft Identification AI                    *
# *    Creation Date: February 4, 2024                        *
# *    Mohawk College Student - Student Number: 000361525     *
# *                                                           *
# *************************************************************
import yaml
from ultralytics import YOLO
import torch
import os
from PIL import Image

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
        config_file (str, optional): Path to the configuration file (defaults to "config.yaml").
    """

    # Load the trained model without training mode
    model = YOLO(model_path).eval()  # `.eval()` ensures the model is in evaluation mode

    # Read configuration (if necessary)
    if config_file:
        with open(config_file, 'r', encoding='utf-8-sig') as f:
            config = yaml.safe_load(f) 

            # Access and store relevant configuration data
            data_path = config['path']
            train_images_path = os.path.join(data_path, config['train'])
            val_images_path = os.path.join(data_path, config['val'])

            # Extract class names (assuming index 0 is "Aircraft")
            class_names = config['names']
            aircraft_class_index = 0
            aircraft_class_name = class_names[aircraft_class_index]

    # Iterate over each image in the unseen images directory
    for image_name in os.listdir(images_folder):
        image_path = os.path.join(images_folder, image_name)
        # Load the image
        image = Image.open(image_path)

        # Predict using the model
        results = model(image)

        # Process the results
        predictions = results.pred[0]  # Assuming the first element contains predictions

        # Check if any "Aircraft" was detected
        aircraft_detected = any(prediction[5] == aircraft_class_index for prediction in predictions)

        # Print results and potentially process detections further
        print(f"Image: {image_name} - Aircraft Detected: {aircraft_detected}")
        if aircraft_detected:
            # Iterate and analyze specific "Aircraft" detections
            for i in range(len(predictions)):  # Iterate using an index 'i'
                prediction = predictions[i]
                if prediction[5] == aircraft_class_index:
                    bbox = results.xyxy[i]  # Now 'i' has a defined value
                    confidence = prediction[4]
                    print(f"  Detected {aircraft_class_name} with confidence: {confidence:.2f}")
                    print(f"    Bounding box: {bbox}")  # Assuming bbox format (x1, y1, x2, y2)



# Main Execution
# Checks if the script is the main program and calls the train_yolo_model function.
# This is a standard Python practice to ensure that the script runs only when it is executed directly,
# not when imported as a module in another script.
if __name__ == '__main__':
    # train_yolo_model()
    test_yolo_model('yolov8n.yaml', 'unseen_images/avro_lancaster', 'runs/detect/train4/weights/best.pt')
