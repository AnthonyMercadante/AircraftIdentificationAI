# How to Use `convert_labels_to_indices.py`

This document provides instructions on how to use the `convert_labels_to_indices.py` script. The purpose of this script is to convert class name strings in label files to their corresponding indices, which is a common requirement for machine learning models, especially object detection models like YOLO.

## Prerequisites

Before using this script, ensure that you have:
- A Python environment set up.
- Label files where the class names need to be replaced with indices.

## Setup

1. **Locate the Script**: Ensure that `convert_labels_to_indices.py` is in a known directory on your system.

2. **Prepare the Label Files**: Your label files should be in a format where each line starts with a class name followed by bounding box coordinates. For example:
   ```
   Aircraft 0.5 0.5 0.1 0.1
   ```

## Usage

1. **Edit the Script (if necessary)**: 
   - Open `convert_labels_to_indices.py` in a text editor.
   - Modify the `label_dir` variable to point to the directory containing your label files.
   - If needed, update the `class_mapping` dictionary to reflect your class names and their corresponding indices.

2. **Run the Script**: 
   - Open a terminal or command prompt.
   - Navigate to the directory containing the script.
   - Run the script using Python:
     ```
     python convert_labels_to_indices.py
     ```

3. **Verify the Changes**: 
   - After running the script, check a few of your label files to ensure that the class names have been replaced with the correct indices.

## Example

Before running the script:
```
Aircraft 0.5 0.5 0.1 0.1
Aircraft 0.6 0.6 0.2 0.2
```

After running the script:
```
0 0.5 0.5 0.1 0.1
0 0.6 0.6 0.2 0.2
```

In this example, all occurrences of `Aircraft` have been replaced with `0`.

## Notes

- The script currently supports replacing one class name. If you have multiple classes, you will need to expand the `class_mapping` dictionary accordingly.
- Always back up your original label files before running the script to prevent data loss.

