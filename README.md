# Aircraft Identifier AI: WWII to Modern Era

## Introduction
Welcome to the Aircraft Identifier AI project repository! This project, led by Nam, Nishkarsh, Adam, and Anthony, is a collaboration with the National Air Force Museum of Canada. We're developing an AI model to identify aircraft in photographs, inspired by WWII RAF's training methods using aircraft silhouette playing cards.

## Project Background
Our project modernizes the RAF's WWII training concept by using AI, aiding the museum's digitization effort and enhancing public research capabilities.

## Current Challenge
As the museum digitizes its aircraft photo archive, we face the challenge of limited and manual search methods. Our AI aims to automate and improve this process.

## Project Goals
- Develop an AI model to identify various aircraft types in photos.
- Focus on accurate aircraft detection, progressing to specific identifications.
- Stretch goal: Extract textual information like aircraft numbers from photos.

## Research Focus
We're investigating the number of labeled examples needed for effective training, considering different aircraft angles and perspectives. Our key goal is to enhance accuracy while reducing processing time.

## Tools Directory

In the `tools` directory, you'll find various tools developed to assist in the project. Each tool is designed to facilitate different aspects of data preparation and analysis for the project. Currently, the directory includes:

- **Batch Grayscale Converter**: Located at `tools/batch_grayscale_converter`, this Python script is used to convert all images in a specified folder to grayscale. It supports multiple image formats and is useful for preprocessing images for certain types of analysis or model training.

- **Label Conversion Tool**: Located at `tools/convert_labels_to_indices`, this script is essential for preparing the data labels for YOLOv8. The script converts class name strings in label files to indices, making it easier to work with numerical data in machine learning models.

- **Image Downloader Tool**: Located at `tools/image_downloader`, this tool helps in downloading a custom dataset from the Open Images Dataset V7 tailored for specific classes. It's essential for gathering training data that's relevant to your specific machine learning objectives.

- **Split Dataset Tool**: Located at `tools/split_folders`, this tool is used for splitting the downloaded dataset into training, validation, and testing sets. Ensuring your data is properly divided is crucial for training machine learning models effectively and evaluating their performance accurately.

- **Store Bounding Boxes Tool**: Located at `tools/store_bounding_boxes`, this script processes images in a specified folder, identifies aircraft within these images using a pre-trained YOLO model, and generates corresponding annotation labels. These labels are saved in a format suitable for further training purposes, facilitating the development of more accurate object detection models. This tool is particularly useful for creating annotation labels of unannotated aircraft images for later training purposes.

- **Image Format Converter**: Located at `tools/image_format_converter`, this Python script converts image files in a specified directory to a format compatible with OpenCV. It supports a wide range of input image formats and converts them to either PNG or JPEG format, based on user preference. PNG is chosen for its lossless compression, while JPEG is selected for its balance between quality and file size. This tool is crucial for preparing images for computer vision tasks that require specific image formats.

Each tool is accompanied by an instructions file that provides detailed instructions on how to use it, including any prerequisites, configuration details, and usage examples. Be sure to review these instructions carefully to maximize the effectiveness of each tool in your projects.

## Video Tutorial and Demonstration

We've created a detailed video tutorial to guide you through the use of our automation tools and demonstrate the process of model training. One of our team members will walk you through each step, providing insights and tips to help you get the most out of our project's resources.

🎥 **Watch the video here:** [Aircraft Identifier AI Tools and Training Demonstration](https://youtu.be/L8QHCNwK01g?si=VhGtoZ6cUJXfoAq5)

This video is an excellent resource for understanding the practical applications of our tools and the thought process behind our model training methodologies. 

## Dataset Generation and Preparation
**Important Note:** The dataset is not included in this repository. To prepare your dataset, follow these steps:
1. **Generate Dataset**: Use the **Image Downloader Tool** in `tools/image_downloader`. Refer to [`Instructions.md`](tools/image_downloader/Instructions.md) for guidance on creating your dataset.
2. **Prepare Data Labels**: Use the **Label Conversion Tool** in `tools/convert_labels_to_indices` to convert class name strings in label files to indices for YOLOv8. Detailed instructions are available in [`ConversionInstructions.md`](tools/convert_labels_to_indices/ConversionInstructions.md).
3. **Split Dataset**: After generating your dataset, split it into training, validation, and testing sets using the **Split Dataset Tool** in `tools/split_folders`. Follow the instructions in [`split_folders_instructions.md`](tools/split_folders/split_folders_instructions.md) for this process.

## Setting Up NVIDIA CUDA for GPU Acceleration
To utilize GPU acceleration during model training, follow these steps to set up NVIDIA CUDA:

### Prerequisites for GPU Acceleration
- An NVIDIA GPU (Ensure your hardware is CUDA-compatible).
- Updated NVIDIA GPU drivers.

### Install CUDA Toolkit
1. **Download CUDA Toolkit**: Visit [NVIDIA's CUDA Toolkit website](https://developer.nvidia.com/cuda-downloads) and download the appropriate version for your system.
2. **Install CUDA Toolkit**: Follow the installation instructions provided by NVIDIA.

### Install cuDNN
1. **Download cuDNN**: Go to [NVIDIA's cuDNN page](https://developer.nvidia.com/cudnn) and download the cuDNN version compatible with the installed CUDA Toolkit.
2. **Extract cuDNN Files**: After downloading, extract the cuDNN zip file to a known directory.
3. **Copy cuDNN Files**: Copy the extracted cuDNN files (from `bin`, `include`, and `lib` directories) into your CUDA Toolkit directory (typically found at `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\vX.X` on Windows).

### Verifying CUDA and cuDNN Installation
1. **Check Environment Variables**: Ensure the CUDA path is correctly set in your system's environment variables.
2. **Test CUDA Installation**: Use Python or command-line tools to verify that CUDA is recognized and functional.

### Note on GPU Usage
- The code in this project will default to CPU processing if no compatible GPU is found or if the GPU setup is not configured correctly.
- For optimal performance and faster training times, setting up CUDA and cuDNN is recommended when using an NVIDIA GPU.

## Contributing
Contributions and suggestions are welcome! For inquiries, contact Stephen Adams at [stephen.adams5@mohawkcollege.ca](mailto:stephen.adams5@mohawkcollege.ca).

## Getting Started
To contribute to the project or run it on your own

 machine, follow these steps to set up a local development environment.

### Prerequisites
- Python 3.x
- pip (Python package manager)
- Git (Version control system)

### Setup
1. **Clone the Repository**
   - Use Git to clone the project's repository to your local machine.
   ```bash
   git clone https://github.com/AnthonyMercadante/AircraftIdentificationAI.git
   cd AircraftIdentificationAI
   ```

2. **Create a Virtual Environment**
   - Navigate to the project directory and create a virtual environment.
   ```bash
   # For macOS and Linux:
   python3 -m venv venv

   # For Windows:
   python -m venv venv
   ```

3. **Activate the Virtual Environment**
   - Activate the newly created virtual environment.
   ```bash
   # For macOS and Linux:
   source venv/bin/activate

   # For Windows:
   ./venv/Scripts/activate
   ```

4. **Install Dependencies**
   - Install the project's dependencies using `requirements.txt`.
   ```bash
   pip install -r requirements.txt
   ```

5. **Deactivate the Virtual Environment**
   - Deactivate the virtual environment when you're done working.
   ```bash
   deactivate
   ```
---
