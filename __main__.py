from ultralytics import YOLO
import torch

def train_yolo_model():
    # Check if GPU is available and set the device accordingly
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")

    # Load a model
    model = YOLO("yolov8n.yaml")  # build a new model from scratch

    # Train the model
    results = model.train(data="config.yaml", epochs=300)  # train the model

if __name__ == '__main__':
    train_yolo_model()
