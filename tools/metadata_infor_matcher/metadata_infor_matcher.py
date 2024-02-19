"""
File Name: Metadata Information Matcher Script
Desc: This script matches metadata from the planes Excel sheet to the photos
      We are able to identify each plane by its metadata, as well a description on what each image is

      To-Do:
      - Display photo information instead of metadata
      - Fix suffix logic
      - Create a dict for most common words (will help us see what plane names appear frequently)
      - Dynamically generate sheet names, instead of hardcoding

Authors: Nguyen Quoc Nam Tran, Adam Calleja
IDs: 000876813, 000862779
School: Mohawk College
Date Created: February 17th, 2024
"""
import pandas as pd
from openpyxl import Workbook, load_workbook
import os
import pandas as pd
import re

def get_suffix_list(suffix):
    """
    This function creates a list of all the suffix values from the starting to ending value The function will
    check to see how long the suffix is (i.e. a-g or a-aa) and handle accordingly The function will ensure that all
    values from the start to the end are displayed in a list Used when dealing with metadata such as 1984.19.47.a-s
    which signifies that there are photos with the same date with suffixes from a-s

    Params:
    - suffix (string): Suffix value used to signify different photos from the same snapshot date

    Return:
    - suffix_list (array): Array of all the suffix values from the start to the end of the suffix
    """
    if not suffix or '-' not in suffix:
        return [suffix]
    start, end = suffix.split('-')
    suffix_list = []
    if len(start) == 1 and len(end) == 1:  # single character range (ex: a-g, a-b)
        suffix_list = [chr(i) for i in range(ord(start), ord(end) + 1)]
    elif len(start) == 1 and len(end) == 2:  #start = single value, end = double value (ex: a-gg, a-ab)
        for i in range(ord(start), ord('z') + 1):
            suffix_list.append(chr(i))
        for i in range(ord('a'), ord(end[0]) + 1):
            for j in range(ord('a'), ord('z') + 1):
                suffix_list.append(f"{chr(i)}{chr(j)}")
                if f"{chr(i)}{chr(j)}" == end:
                    return suffix_list
    return suffix_list

#Testing logic for making sure suffix works
#retest with corrected logic
#test_range = "a-g"
#suffixes_generated = get_suffix_list(test_range)
#print(f"Suffixes generated for the range '{test_range}': {suffixes_generated}")

#handling the extended range without causing errors
#test_range_extended = "a-gg"
#suffixes_generated_extended = get_suffix_list(test_range_extended)
#print(f"Suffixes generated for the range '{test_range_extended}': {suffixes_generated_extended}")

def normalize_date_format(date_str):
    """
    This function normalizes the data so that it is processed in uniform
    Ensures that the dates are all separated by .'s, and that we break apart the date with the suffix
    If no suffix exists for the date, we return back nothing

    Params:
    date_str (string): Metadata String that we want to format

    Return:
    standardized_date_str (string): Updated and formatted date
    suffix (string): Suffix that follows the date, blank or letter value
    """
    standardized_date_str = date_str.replace('-', '.')
    match = re.match(r'(\d+\.\d+\.\d+)(\s*[a-zA-Z]*-?[a-zA-Z]*)?$', standardized_date_str)
    if match:
        numeric_part = match.group(1)  # Date
        suffix = match.group(2).strip().lower() if match.group(2) else '' # Suffix
        return numeric_part, suffix
    else:
        return standardized_date_str, '' #Date w/ no suffix

def find_matches(normalized_date, image_files):
    """
    This function checks if there is a match between the normalized date, and the image files
    Image file names are normalized to ensure that the metadata and files are the same format
    If there are matches between the filename and the metadata, it is added to the array and returned back.

    Params:
    normalized_date (tuple): information about the normalized date (date/suffix)
    image_files (array): file names of the aircraft photos

    Returns:
    matches(array): Any metadata that matches a filename is added to the matches array


    """
    date, suffix = normalized_date
    matches = []
    for image_filename in image_files:
        standardized_filename = image_filename.replace('-', '.').lower()
        file_date, file_suffix = normalize_date_format(standardized_filename)

        # Modify the check to ensure exact match by confirming the match is followed by a non-digit or end of string
        pattern = f"^{date}([^0-9]|$)"
        if re.match(pattern, file_date) and (not suffix or suffix == file_suffix):
            matches.append(image_filename)
    return matches


def process_sheet(sheet_name):
    """
    This function processes the Excel file and the photo data
    The file will output where the matches occur, as well as a description of the image if the metadata and image name correlate

    Params:
    sheet_name (csv): Excel sheet with metadata on aircraft
    """

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

    # Dictionary to store matches for each date
    matches_dict = {}

    # Iterate through rows in the specified sheet. Because it starts at row 2 which is not including the title and using enumerate methods.
    for i, row in enumerate(sheet.iter_rows(min_row=2, max_row=last_row, min_col=3, max_col=4, values_only=True), start=1):
        date_str, description = str(row[0]), row[1]  # Extract the date string from the tuple

        # Check if the date value is a valid string or timestamp
        if isinstance(date_str, (str, pd.Timestamp)):
            normalized_date = normalize_date_format(date_str)
            matches = find_matches(normalized_date, image_files)
            if matches:  # If there are matches, store them with their description
                matches_dict[date_str] = [(match, description) for match in matches]
            else:
                print(f"No matches found for date '{date_str}' in Metadata")
        else:
            print(f"Invalid date value at row {i}: {date_str}")


    # Print the matches between value in metadata and image files
    for date_value, matches in matches_dict.items():
        if matches:
            print(f"Matches found for date '{date_value}' in Metadata and image files: {matches}")
        else:
            print(f"No matches found for date '{date_value}' in Metadata")

# List of sheet names.
sheet_names = ['Doc Box 1', 'Doc Box 2', 'Doc Box 6', 'P-Box 1a', 'P-Box 1b', 'P-Box 1c', 'P-Box 1d', 'P-Box 1f']

# Process each sheet
for sheet_name in sheet_names:
    print(f"\nProcessing sheet: {sheet_name}")
    process_sheet(sheet_name)