# Aircraft Identifier AI: WWII to Modern Era

## Introduction
Welcome to the Aircraft Identifier AI project repository! This project, led by Nam, Nishkarsh, Adam, and Anthony, develops an AI model to identify aircraft in photographs. It's a collaboration with the National Air Force Museum of Canada, inspired by WWII RAF's training methods.

## Project Background
During WWII, the RAF used aircraft silhouette playing cards for training. We're modernizing this concept with AI, aiding the museum's digitization effort and enhancing public research capabilities.

## Current Challenge
The museum is digitizing its aircraft photo archive, but current search methods are limited and manual. Our AI aims to automate and improve this process.

## Project Goals
- Develop an AI model to identify aircraft types in photos.
- Focus on accurate plane detection, progressing to specific identifications.
- Stretch goal: Extract textual information like aircraft numbers from photos.

## Research Focus
We're exploring the number of labeled examples needed for effective training, considering various aircraft angles and perspectives. A key goal is to reduce processing time and enhance accuracy.

## Contributing
Contributions and suggestions are welcome! For inquiries, contact Stephen Adams at [stephen.adams5@mohawkcollege.ca](mailto:stephen.adams5@mohawkcollege.ca).

To include instructions for setting up the virtual environment in your project's README, you can add a section that guides users through the process of cloning the repository, setting up the virtual environment, installing dependencies, and running the project. Here's a suggested addition to your README:

---

## Getting Started

Follow these instructions to set up a local development environment, so you can contribute to the project or simply run it on your own machine.

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
   .\venv\Scripts\activate
   ```

4. **Install Dependencies**
   - Install the project's dependencies using the `requirements.txt` file.
   ```bash
   pip install -r requirements.txt
   ```

5. **Deactivate the Virtual Environment**
   - When you're done working, deactivate the virtual environment.
   ```bash
   deactivate
   ```
