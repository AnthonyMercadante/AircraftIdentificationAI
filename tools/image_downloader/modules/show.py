import cv2
import os
import re
import numpy as np

class_list = []
color_dic = {}

def color_gen():
    """
    Generate a new RGB color. As the first color, it generates (0, 255, 0).
    Subsequent colors are generated randomly.
    """
    global color_dic
  
    if not color_dic:
        color_dic['initial'] = (0, 255, 0)
    else:
        color = tuple(np.random.randint(0, 256, 3))
        color_dic[f'color_{len(color_dic)}'] = color

    return color

def show(class_name, download_dir, label_dir, total_images, index):
    """
    Show the images with the labeled boxes.

    Parameters:
    class_name (str): Name of the class to be visualized.
    download_dir (str): Directory containing the images.
    label_dir (str): Directory containing the labels.
    total_images (int): Total number of images.
    index (int): Index of the current image.

    Returns:
    None
    """
    global class_list

    img_files = [f for f in os.listdir(download_dir) if f.endswith('.jpg')]
    if index >= len(img_files):
        print("Index out of range.")
        return

    img_file = img_files[index]
    current_image_path = os.path.join(download_dir, img_file)
    img = cv2.imread(current_image_path)

    label_file_name = os.path.splitext(img_file)[0] + '.txt'
    label_file_path = os.path.join(label_dir, label_file_name)

    with open(label_file_path, 'r') as f:
        window_name = f"Visualizer: {index + 1}/{total_images}"
        display_image_with_labels(img, f, window_name)

def display_image_with_labels(img, label_file, window_name):
    """
    Display the image with labels read from the label file.

    Parameters:
    img (numpy.ndarray): Image to be displayed.
    label_file (file object): File containing label information.
    window_name (str): Name of the window in which the image is displayed.

    Returns:
    None
    """
    for line in label_file:
        class_name, bbox = parse_label_line(line)
        if class_name not in class_list:
            class_list.append(class_name)
            color_gen()

        draw_label_on_image(img, class_name, bbox, color_dic[class_name])

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    resize_and_show_image(img, window_name)

def parse_label_line(line):
    """
    Parse a line from the label file.

    Parameters:
    line (str): A line from the label file.

    Returns:
    tuple: A tuple containing the class name and the bounding box coordinates.
    """
    match_class_name = re.compile('^[a-zA-Z]+(\s+[a-zA-Z]+)*').match(line)
    class_name = line[:match_class_name.span()[1]]
    bbox = [float(val) for val in line[match_class_name.span()[1]:].split()]
    return class_name, bbox

def draw_label_on_image(img, class_name, bbox, color):
    """
    Draw the label on the image.

    Parameters:
    img (numpy.ndarray): Image to be labeled.
    class_name (str): Name of the class.
    bbox (list): Bounding box coordinates.
    color (tuple): Color for the label.

    Returns:
    None
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    b, g, r = color
    cv2.putText(img, class_name, (int(bbox[0]) + 5, int(bbox[1]) - 7), font, 0.8, (b, g, r), 2, cv2.LINE_AA)
    cv2.rectangle(img, (int(bbox[2]), int(bbox[3])), (int(bbox[0]), int(bbox[1])), (b, g, r), 3)

def show(class_name, download_dir, label_dir,total_images, index):
    '''
    Show the images with the labeled boxes.

    :param class_name: self explanatory
    :param download_dir: folder that contains the images
    :param label_dir: folder that contains the labels
    :param index: self explanatory
    :return: None
    '''
 
    global class_list, color_dic

    if not os.listdir(download_dir)[index].endswith('.jpg'):
        index += 2
    img_file = os.listdir(download_dir)[index]
    current_image_path = str(os.path.join(download_dir, img_file))
    img = cv2.imread(current_image_path)
    file_name = str(img_file.split('.')[0]) + '.txt'
    file_path = os.path.join(label_dir, file_name)
    f = open(file_path, 'r')

    window_name = "Visualizer: {}/{}".format(index+1, total_images)

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    width = 500
    height = int((img.shape[0] * width) / img.shape[1])
    cv2.resizeWindow(window_name, width, height)

    for line in f:        
        # each row in a file is class_name, XMin, YMix, XMax, YMax
        match_class_name = re.compile('^[a-zA-Z]+(\s+[a-zA-Z]+)*').match(line)
        class_name = line[:match_class_name.span()[1]]
        ax = line[match_class_name.span()[1]:].lstrip().rstrip().split(' ')
	# opencv top left bottom right

        if class_name not in class_list:
            class_list.append(class_name)
            color = color_gen()     
            color_dic[class_name] = color  

        font = cv2.FONT_HERSHEY_SIMPLEX
        r ,g, b = color_dic[class_name]
        cv2.putText(img,class_name,(int(float(ax[0]))+5,int(float(ax[1]))-7), font, 0.8,(b, g, r), 2,cv2.LINE_AA)
        cv2.rectangle(img, (int(float(ax[-2])), int(float(ax[-1]))),
                      (int(float(ax[-4])),
                       int(float(ax[-3]))), (b, g, r), 3)

    cv2.imshow(window_name, img)

def resize_and_show_image(img, window_name):
    """
    Resize and show the image in a CV2 window.

    Parameters:
    img (numpy.ndarray): Image to be displayed.
    window_name (str): Name of the CV2 window.

    Returns:
    None
    """
    width = 500
    height = int((img.shape[0] * width) / img.shape[1])
    cv2.resizeWindow(window_name, width, height)
    cv2.imshow(window_name, img)
