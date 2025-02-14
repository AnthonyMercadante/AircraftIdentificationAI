# Image Downloader

## Overview

Download a custom dataset from the [Open Images Dataset V7](https://storage.googleapis.com/openimages/web/index.html), tailored for specific classes.

## Installation

Clone the repository and install dependencies in a Python environment (version >= 3.7.0).

```bash
pip3 install -r requirements.txt  # Install dependencies
```

## Download Custom Dataset

Specify class names for the dataset. The `--classes` argument is required.

**Required Argument:**
  - `--classes`: Class names to download (e.g., Aircraft).

Optional arguments to customize bounding box parameters are set to `2` by default.

**Optional Arguments:**
  - `--isOcclud`
  - `--isTruncated`
  - `--isGroupOf`
  - `--isDepiction`
  - `--isInside`

Run `main.py` to start the download process for the specified classes:

```bash
python3 main.py --classes Aircraft # Downloads dataset for Aircraft class
```

The script manages the download of necessary files and organizes them in the following directory structure:

```
root_directory
│
├───tools
│   └───image_downloader
│       │   main.py
│       │   downloader.py
│       │   settings.py
│       │   ...
│
└───dataset
    │   img_ids.txt
    │
    ├───images
    │   │   0fdea8a716155a8e.jpg
    │   │   2fe4f21e409f0a56.jpg
    │   │   ...
    │
    └───labels
        │   0fdea8a716155a8e.txt
        │   2fe4f21e409f0a56.txt
        │   ...
```

## Next Steps

After you have successfully downloaded and organized your dataset, the next step is to split it into training, validation, and testing sets. This is crucial for preparing your dataset for machine learning model training.

Navigate to the `split_folders` directory and follow the instructions in [`split_folders_instructions.md`](../split_folders/split_folders_instructions.md) to proceed with splitting your dataset into the appropriate subsets.
