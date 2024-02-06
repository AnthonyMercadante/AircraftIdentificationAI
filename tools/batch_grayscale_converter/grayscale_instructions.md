# Batch Grayscale Converter

The `batch_grayscale_converter.py` script is used to convert all images in a specified folder to grayscale. It supports various image formats including `.png`, `.jpg`, `.jpeg`, `.tiff`, `.bmp`, and `.gif`.

## Usage

1. **Place the Script in an Accessible Location**
   
   Download or copy the `batch_grayscale_converter.py` script to a known location on your system.

2. **Specify the Folder Path**
   
   Open the script in a text editor and locate the following line:

   ```python
   folder_path = 'your_folder_path'
   ```

   Replace `'your_folder_path'` with the path to the folder containing the images you want to convert. For example:

   ```python
   folder_path = '/path/to/your/images'
   ```

3. **Run the Script**
   
   Open a terminal or command prompt, navigate to the location of the script, and run:

   ```bash
   python batch_grayscale_converter.py
   ```

   The script will process all images in the specified folder, converting them to grayscale and saving them in the same folder with a `_grayscale` suffix.

4. **Check the Results**
   
   After the script finishes execution, you will find the grayscale images in the same folder as the original images. Each grayscale image will have the same name as its original with `_grayscale` added before the file extension.