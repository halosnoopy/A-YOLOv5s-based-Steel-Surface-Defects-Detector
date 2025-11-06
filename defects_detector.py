import tkinter as tk
from tkinter import filedialog
import subprocess
import threading
import os
from PIL import Image, ImageTk

# Global variable to indicate detection completion
detection_completed = threading.Event()

# Global variable to hold the reference to the image label
image_label = None

def browse_weight():
    weight_path = filedialog.askopenfilename(initialdir="./yolov5/runs/train", filetypes=[("Weight files", "*.pt")])
    weight_entry.delete(0, tk.END)
    weight_entry.insert(0, weight_path)


def browse_source():
    source_paths = filedialog.askopenfilenames(initialdir="./test/images", filetypes=[("Image files", "*.jpg")])
    source_entry.delete(0, tk.END)
    source_entry.insert(0, ", ".join(source_paths))


def run_detection_thread():
    weight = weight_entry.get()
    source = source_entry.get().split(", ")
    conf_thres = conf_thres_entry.get()

    for image_path in source:
        cmd = f"python **fill_your_own_path**/detect.py --weight {weight} --source {image_path} --conf-thres {conf_thres} --project ./yolov5/neu_output --imgsz 200"
        subprocess.run(cmd, shell=True)

    # Scan the neu_output folder for new folders and display the images
    scan_neu_output()


def scan_neu_output():
    output_folder = "./yolov5/neu_output"
    # Scan the neu_output folder for new folders
    subfolders = [f.path for f in os.scandir(output_folder) if f.is_dir()]
    # Sort subfolders based on their creation time
    subfolders.sort(key=lambda x: os.path.getctime(x), reverse=True)
    for folder in subfolders:
        # Check if the folder contains images
        images = [f.path for f in os.scandir(folder) if f.is_file() and f.name.endswith(('.jpg', '.jpeg', '.png'))]
        if images:
            # Display the first image in the folder
            image_path = images[0]
            display_image(image_path)
            # Break the loop after displaying the image from the most recent folder
            break

    # Enable the "Run Detection" button again
    run_button.config(text="Run Detection", state=tk.NORMAL)


def display_image(image_path):
    global image_label

    # Open the image using PIL
    img = Image.open(image_path)
    # Resize image to fit the GUI window if necessary
    img.thumbnail((400, 400))
    # Convert PIL image to Tkinter PhotoImage
    img_tk = ImageTk.PhotoImage(img)

    # If there is already an image label, update it with the new image
    if image_label:
        image_label.config(image=img_tk)
        image_label.image = img_tk  # Keep reference to the image to prevent garbage collection
    else:
        # Create a new label for the image
        image_label = tk.Label(root, image=img_tk)
        image_label.grid(row=4, columnspan=3, pady=10)

    # Optionally, you can resize the window to fit the image
    root.geometry(f"{img.width}x{img.height + 200}")  # Adjust the window height to fit the image


def run_detection():
    def run_detection_thread_wrapper():
        # Clear previous detection completion indication
        detection_completed.clear()
        # Start detection in a separate thread
        threading.Thread(target=run_detection_thread, daemon=True).start()
        # Update GUI to indicate detection in progress
        run_button.config(text="Running Detection...", state=tk.DISABLED)

    run_detection_thread_wrapper()


def check_detection_completion():
    if detection_completed.is_set():
        # Optionally, show a message or perform any other action upon detection completion
        pass


def end_gui():
    root.destroy()


# Create the main window
root = tk.Tk()
root.title("Defects Detector")

# Fix the window size
root.minsize(width=600, height=400)
root.maxsize(width=600, height=400)
root.resizable(False, False)

# Create labels and entry widgets for weight, source, and conf-thres
default_weight_path = './yolov5/runs/train/exp7/weights/best.pt'
weight_label = tk.Label(root, text="Weight Path:")
weight_label.grid(row=0, column=0, sticky="w")
weight_entry = tk.Entry(root, width=50)
weight_entry.insert(0, default_weight_path)
weight_entry.grid(row=0, column=1, padx=5, pady=5)
browse_weight_button = tk.Button(root, text="Browse", command=browse_weight)
browse_weight_button.grid(row=0, column=2)

default_source_path = './test/images/patches_211.jpg'
source_label = tk.Label(root, text="Source Path:")
source_label.grid(row=1, column=0, sticky="w")
source_entry = tk.Entry(root, width=50)
source_entry.insert(0, default_source_path)
source_entry.grid(row=1, column=1, padx=5, pady=5)
browse_source_button = tk.Button(root, text="Browse", command=browse_source)
browse_source_button.grid(row=1, column=2)

default_conf = 0.5
conf_thres_label = tk.Label(root, text="Confidence Threshold:")
conf_thres_label.grid(row=2, column=0, sticky="w")
conf_thres_entry = tk.Entry(root)
conf_thres_entry.insert(0, default_conf)
conf_thres_entry.grid(row=2, column=1, padx=5, pady=5)

# Button to run detection
run_button = tk.Button(root, text="Run Detection", command=run_detection)
run_button.grid(row=3, columnspan=3, pady=10)

# Create image label
image_label = tk.Label(root)
image_label.grid(row=4, columnspan=3, pady=10)

# Check detection completion periodically
root.after(100, check_detection_completion)

# Button to end GUI
end_button = tk.Button(root, text="End", command=end_gui)
end_button.grid(row=5, columnspan=3, pady=10)

root.mainloop()