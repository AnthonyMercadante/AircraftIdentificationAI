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
- **Image Downloader Tool**: This tool, located at `tools/image_downloader`, facilitates downloading a custom dataset from the Open Images Dataset V7 tailored for specific classes. It's essential for gathering training data for our AI model.

## Dataset Generation
**Important Note:** The dataset is not included in this repository. You need to generate it on your own using the **Image Downloader Tool** located in `tools/image_downloader`. Please refer to the [`Instructions.md`](tools/image_downloader/Instructions.md) file in that directory to start creating the dataset for your local repository. The repository is configured to ignore the dataset files; however, upon generation, you may need to manually ignore additional dataset files depending on the class you use. For our project, we are using the aircraft dataset.

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

---

This update provides a direct link to the `Instructions.md` file, making it easier for users to access the necessary information for dataset generation.