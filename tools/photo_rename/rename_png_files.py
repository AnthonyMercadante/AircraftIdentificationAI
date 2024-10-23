import os
import uuid

def rename_png_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.png'):
            old_file_path = os.path.join(folder_path, filename)
            # Generate a new unique filename
            unique_name = f"{uuid.uuid4()}.png"
            new_file_path = os.path.join(folder_path, unique_name)
            # Ensure the new filename doesn't already exist
            while os.path.exists(new_file_path):
                unique_name = f"{uuid.uuid4()}.png"
                new_file_path = os.path.join(folder_path, unique_name)
            os.rename(old_file_path, new_file_path)
            print(f"Renamed '{filename}' to '{unique_name}'")

if __name__ == '__main__':
    # Manually specify the folder name (replace 'photos' with your folder name)
    folder_name = 'jet_renders'
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the folder
    folder_path = os.path.join(script_dir, folder_name)
    # Call the function with the specified folder path
    rename_png_files(folder_path)
