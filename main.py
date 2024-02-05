from ultralytics import YOLO
import torch

# Check if GPU is available
if torch.cuda.is_available():
    print("Using GPU for training.")
    device = torch.device('cuda')
else:
    print("GPU not available, using CPU instead.")
    device = torch.device('cpu')

# Load a model
model = YOLO("yolov8n.yaml")  # build a new model from scratch

# Move the model to the specified device
model.to(device)

# Train the model
results = model.train(data="config.yaml", epochs=300)  # train the model
