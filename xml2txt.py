
import xml.etree.ElementTree as ET
import os
from os import getcwd
from tqdm import tqdm
import shutil

img_file_name = 'IMAGES'
labels_file_name = 'ANNOTATIONS'
new_label_file_name = 'LABELS'


img_path = './%s/'%(img_file_name)
lb_path = './%s/'%(labels_file_name)
new_lb_path = './%s/'%(new_label_file_name)


classes = ["crazing", "inclusion", "patches", "pitted_surface", "rolled-in_scale", "scratches"]


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(image_id):
    in_file = lb_path + '%s.xml' % (image_id)
    out_file = open(new_lb_path + '%s.txt' % (image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


def check_and_copy_folders(source_folder, destination_folder):
    # Check if 'ANNOTATIONS' and 'IMAGES' folders exist in the current folder
    annotations_exist = os.path.exists(os.path.join(destination_folder, 'ANNOTATIONS'))
    images_exist = os.path.exists(os.path.join(destination_folder, 'IMAGES'))

    if not annotations_exist or not images_exist:
        # If either 'ANNOTATIONS' or 'IMAGES' folder doesn't exist, copy them from 'dataset' folder
        dataset_annotations_path = os.path.join(source_folder, 'ANNOTATIONS')
        dataset_images_path = os.path.join(source_folder, 'IMAGES')

        # Check if 'dataset' folder exists
        if os.path.exists(dataset_annotations_path) and os.path.exists(dataset_images_path):
            # Copy 'ANNOTATIONS' and 'IMAGES' folders from 'dataset' to the current folder
            if not annotations_exist:
                shutil.copytree(dataset_annotations_path, os.path.join(destination_folder, 'ANNOTATIONS'))
            if not images_exist:
                shutil.copytree(dataset_images_path, os.path.join(destination_folder, 'IMAGES'))
        else:
            print("'ANNOTATIONS' or 'IMAGES' folders not found in the current directory or 'dataset' folder does not exist.")
    else:
        print("Both 'ANNOTATIONS' and 'IMAGES' folders exist in the current directory.")


def remove_folders(directory, folders):
    """Remove specified folders in the given directory."""
    for folder in folders:
        try:
            if os.path.isdir(folder):
                shutil.rmtree(folder)
                print(f"Folder '{folder}' removed successfully.")
            else:
                print(f"Folder '{folder}' does not exist.")
        except Exception as e:
            print(f"Failed to remove folder '{folder}': {str(e)}")



if __name__ == "__main__":
    
    wd = getcwd()
    source_dataset_directory = os.path.join(wd, 'dataset')
    check_and_copy_folders(source_dataset_directory, wd)
    
    if os.path.exists(new_lb_path):
        files = os.listdir(new_lb_path)
        for file in files:
            os.remove(os.path.join(new_lb_path, file))  # Remove each file in the directory
    else:
        os.makedirs(new_lb_path)

    image_ids = os.listdir(img_path)
    for image_id in tqdm(image_ids):
        convert_annotation(image_id.split('.')[0])
        
    remove_folders(wd, [lb_path])


print('Label Formating Finished!')





# In[ ]:





# In[ ]:




