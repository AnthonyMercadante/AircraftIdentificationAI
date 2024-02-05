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
In the `tools` directory, you'll find various tools developed to assist in the project. Currently, it includes:
- **Image Downloader Tool**: Located at `tools/image_downloader`, this tool helps in downloading a custom dataset from the Open Images Dataset V7 tailored for specific classes, essential for gathering training data.
- **Split Dataset Tool**: Located at `tools/split_folders`, this tool is used for splitting the downloaded dataset into training, validation, and testing sets. It's crucial for preparing the dataset for machine learning model training.
- **Label Conversion Tool**: Located at `tools/convert_labels_to_indices`, this script is essential for preparing the data labels for YOLOv8. The script converts class name strings in label files to indices.

## Dataset Generation and Preparation
**Important Note:** The dataset is not included in this repository. To prepare your dataset, follow these steps:
1. **Generate Dataset**: Use the **Image Downloader Tool** in `tools/image_downloader`. Refer to [`Instructions.md`](tools/image_downloader/Instructions.md) for guidance on creating your dataset.
2. **Prepare Data Labels**: Use the **Label Conversion Tool** in `tools/convert_labels_to_indices` to convert class name strings in label files to indices for YOLOv8. Detailed instructions are available in [`ConversionInstructions.md`](tools/convert_labels_to_indices/ConversionInstructions.md).
3. **Split Dataset**: After generating your dataset, split it into training, validation, and testing sets using the **Split Dataset Tool** in `tools/split_folders`. Follow the instructions in [`split_folders_instructions.md`](tools/split_folders/split_folders_instructions.md) for this process.


## Contributing
Contributions and suggestions are welcome! For inquiries, contact Stephen Adams at [stephen.adams5@mohawkcollege.ca](mailto:stephen.adams5@mohawkcollege.ca).

## Getting Started

To contribute to the project or run it on your own machine, follow these steps to set up a local development environment.

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