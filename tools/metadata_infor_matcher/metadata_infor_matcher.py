# **************************************************************
# *                                                            *
# *    Author: Nguyen Quoc Nam Tran                            *
# *    Project: Aircraft Identification AI                     *
# *    Creation Date: February 17, 2024                        *
# *    Mohawk College Student - Student Number: 000876813      *
# *                                                            *
# **************************************************************
import pandas as pd
from openpyxl import Workbook, load_workbook 
import os
import pandas as pd
import re

def process_sheet(sheet_name): 

    # Get the current directory of the script
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Excel file path with a relative path
    excel_file = os.path.join(base_path, 'NAFMC Photographic Collection.xlsx')

    # Load the Excel workbook
    book = load_workbook(excel_file)

    # Replace hyphens with spaces in the sheet name
    correct_sheet_name = sheet_name.replace('-', ' ')

    # Get the specified sheet
    sheet = book[sheet_name]

    # Find the last row with data in column C which 3. We can extend them later. 
    last_row = sheet.max_row
    while not sheet.cell(row=last_row, column=3).value and last_row > 1:
        last_row -= 1

    # Path to the folder containing images with a relative path
    image_folder = os.path.join(base_path, 'Anthony_Nish_Adam_Nguyen_Group', 'NAFMC', correct_sheet_name)

    # Create an empty list to store image filenames
    image_files = []

    # Iterate through files in the specified image folder
    for file_name in os.listdir(image_folder):

        # Create the full path by joining the folder path and the file name
        full_path = os.path.join(image_folder, file_name)
        
        # Check if the current item in the iteration is correctly a file
        if os.path.isfile(full_path):

            # If it iss a file then add the filename to the list of image_files
            image_files.append(file_name)

    # Function to normalize date formats
    def normalize_date_format(date_str):
        return re.sub(r'\D', '', date_str)  # Remove non-alphanumeric characters

    # Dictionary to store matches for each date
    matches_dict = {}

    # Iterate through rows in the specified sheet. Because it starts at row 2 which is not including the title and using enumerate methods. 
    for i, (date_value) in enumerate(sheet.iter_rows(min_row=2, max_row=last_row, min_col=3, max_col=4, values_only=True), start=1):
        date_str = str(date_value[0])  # Extract the date string from the tuple

        # Check if the date value is a valid string or timestamp
        if isinstance(date_str, (str, pd.Timestamp)):
            # Normalize date format for both metadata and image filenames
            normalized_date = normalize_date_format(date_str)

            # Using list comprhensive to find image filenames matching the normalized (Numbers) date in the metadata
            matches = [image_filename for image_filename in image_files if normalized_date in normalize_date_format(image_filename).lower()]

            matches_dict[date_str] = matches
        else:
            print(f"Invalid date value at row {i}: {date_str}")


    # Print the matches between value in metadata and image files
    for date_value, matches in matches_dict.items():
        if matches:
            print(f"Matches found for date '{date_value}' in Metadata and image files: {matches}")
        else:
            print(f"No matches found for date '{date_value}' in Metadata")


    # # Print the image descriptions
    # for image_filename, description_value in image_descriptions.items():
    #     print(f"Image: {image_filename}, Description: {description_value}")

# List of sheet names. 
sheet_names = ['Doc Box 1', 'Doc Box 2', 'Doc Box 6', 'P-Box 1a', 'P-Box 1b', 'P-Box 1c', 'P-Box 1d', 'P-Box 1f']

# Process each sheet
for sheet_name in sheet_names:
    print(f"\nProcessing sheet: {sheet_name}")
    process_sheet(sheet_name)