# Image Format Converter for OpenCV

This script converts images from various formats into PNG, ensuring compatibility with OpenCV. It processes all images within a specified input directory, converting each to PNG format, and saves them in a designated output directory with the same filenames.

## Requirements

Before running this script, ensure you have Python and Pillow installed on your system. Pillow is a Python Imaging Library that provides easy-to-use image processing capabilities.

You can install Pillow using pip:

```bash
pip install Pillow
```

## Usage

To use the script, follow the command structure below:

```bash
python convert_to_png.py <input_directory> <output_directory>
```

Replace `<input_directory>` with the path to the directory containing your original images and `<output_directory>` with the path where you want the converted PNG images to be saved.

### Arguments

- `input_dir`: The directory containing the images you want to convert. This script will process all recognized image files within this directory.
- `output_dir`: The directory where the converted PNG images will be saved. If this directory does not exist, the script will create it.

## Example

```bash
python convert_to_png.py /path/to/my/images /path/to/save/pngs
```

This command will convert all supported images in `/path/to/my/images` to PNG format and save them in `/path/to/save/pngs`.

## Supported Formats

The script can convert images from the following formats to PNG:

- JPG/JPEG
- BMP
- TIFF/TIF
- and other common image formats that are not natively supported by OpenCV.

## Note

- The script overwrites files with the same name in the output directory. Ensure you have backups or are using a new directory to avoid accidental data loss.
- Only image files are processed. Non-image files in the input directory are ignored.