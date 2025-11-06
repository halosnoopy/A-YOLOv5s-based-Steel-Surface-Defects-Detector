
import os
import random
import shutil


LABELS_PATH = './LABELS/'
IMAGES_PATH = './IMAGES/'
VALID_PATH = './val/'
TRAIN_PATH = './train/'
TEST_PATH = './test/'


def empty_directory(path):
    if os.path.exists(path):
        # If the path exists, empty it
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        # If the path doesn't exist, create it
        os.makedirs(path)


def split_train_val_sets(class_name, train_ratio = 0.9, random_seed = None):
    random.seed(random_seed)
    image_files = [file for file in os.listdir(IMAGES_PATH) if file.startswith(class_name) and file.endswith('.jpg')]
    label_files = [file for file in os.listdir(LABELS_PATH) if file.startswith(class_name) and file.endswith('.txt')]

    if len(image_files) < 1:
        return  # No images for this class, exit function

    num_test_val_files = int(len(image_files) * (1-train_ratio))
    num_test_files = int(num_test_val_files * 0.3)  # 30% of test_val for test set
    num_val_files = num_test_val_files - num_test_files  # Remaining for validation set

    test_val_files = random.sample(list(zip(image_files, label_files)), num_test_val_files)
    test_files = random.sample(test_val_files, num_test_files)
    val_files = [file for file in test_val_files if file not in test_files]

    for img, lbl in test_files:
        shutil.move(os.path.join(IMAGES_PATH, img), os.path.join(TEST_PATH, 'images', img))
        shutil.move(os.path.join(LABELS_PATH, lbl), os.path.join(TEST_PATH, 'labels', lbl))

    for img, lbl in val_files:
        shutil.move(os.path.join(IMAGES_PATH, img), os.path.join(VALID_PATH, 'images', img))
        shutil.move(os.path.join(LABELS_PATH, lbl), os.path.join(VALID_PATH, 'labels', lbl))

    for img, lbl in zip(image_files, label_files):
        if (img, lbl) not in test_val_files:
            shutil.move(os.path.join(IMAGES_PATH, img), os.path.join(TRAIN_PATH, 'images', img))
            shutil.move(os.path.join(LABELS_PATH, lbl), os.path.join(TRAIN_PATH, 'labels', lbl))


def remove_folders(directory, folders):
    """Remove specified folders in the given directory."""
    for folder in folders:
        # folder_path = os.path.join(directory, folder)
        try:
            if os.path.isdir(folder):
                os.rmdir(folder)
                print(f"Folder '{folder}' removed successfully.")
            else:
                print(f"Folder '{folder}' does not exist.")
        except Exception as e:
            print(f"Failed to remove folder '{folder}': {str(e)}")

empty_directory(VALID_PATH)
empty_directory(TRAIN_PATH)
empty_directory(TEST_PATH)


os.makedirs(os.path.join(VALID_PATH, 'images'), exist_ok=True)
os.makedirs(os.path.join(VALID_PATH, 'labels'), exist_ok=True)
os.makedirs(os.path.join(TRAIN_PATH, 'images'), exist_ok=True)
os.makedirs(os.path.join(TRAIN_PATH, 'labels'), exist_ok=True)
os.makedirs(os.path.join(TEST_PATH, 'images'), exist_ok=True)
os.makedirs(os.path.join(TEST_PATH, 'labels'), exist_ok=True)


class_names = ["crazing", "inclusion", "patches", "pitted_surface", "rolled-in_scale", "scratches"]
classes = {str(i): class_names[i] for i in range(len(class_names))}


train_ratio = 0.9
random_seed = 42
for image_file in os.listdir(IMAGES_PATH):
    if image_file.endswith('.jpg'):
        class_name = image_file.split('_')[0]  # Extract class name from the file name
        split_train_val_sets(class_name, train_ratio, random_seed)


folders_to_remove = [LABELS_PATH, IMAGES_PATH]
wd = os.getcwd()
remove_folders(wd, folders_to_remove)






