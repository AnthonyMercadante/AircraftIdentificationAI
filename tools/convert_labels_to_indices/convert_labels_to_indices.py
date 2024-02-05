import os

# Define the directory containing your label files
label_dir = '../../dataset/labels'  # Update this with the path to your label files

# Define your class mapping
class_mapping = {
    'Aircraft': '0'
}

# Function to replace class names with indices
def replace_class_names(file_path, class_mapping):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        for class_name, class_index in class_mapping.items():
            line = line.replace(class_name, class_index)
        new_lines.append(line)

    with open(file_path, 'w') as file:
        file.writelines(new_lines)

# Iterate over each file in the directory and apply the function
for filename in os.listdir(label_dir):
    if filename.endswith('.txt'):
        file_path = os.path.join(label_dir, filename)
        replace_class_names(file_path, class_mapping)

print("Class names replaced with indices.")
