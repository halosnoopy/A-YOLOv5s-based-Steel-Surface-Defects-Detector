# A-YOLOv5s-based-Steel-Surface-Defects-Detector

---

## Overview
This project implements an automated **steel surface defect detection system** using the **YOLOv5s** model. The goal is to detect and classify surface defects such as scratches, patches, and inclusions on hot-rolled steel strips from the NEU-DET dataset.

Traditional visual inspection is time-consuming and error-prone. By applying deep learning–based object detection, this project provides a robust, real-time, and scalable solution to improve product quality and manufacturing reliability.

---

## Objectives
- Develop a real-time system to identify surface defects on steel strips.  
- Implement and fine-tune the YOLOv5s architecture for six defect categories.  
- Evaluate model performance using precision, recall, and mean Average Precision (mAP).  
- Build a graphical user interface (GUI) to simulate defect detection in images.  
<img width="940" height="167" alt="image" src="https://github.com/user-attachments/assets/c56a1d7b-37ea-4437-8c5e-bf64b915590d" />

---

## Dataset
**NEU-DET (Northeastern University Surface Defect Dataset)**  

- Total: **1800 grayscale images** (200×200 pixels)  
- Six classes of defects:  
  - Rolled-in Scale (Rs)  
  - Patches (P)  
  - Crazing (Cr)  
  - Pitted Surface (Ps)  
  - Inclusion (In)  
  - Scratches (Sc)  

Each class includes **300 samples** of real industrial surface images.  
Reference: Song, K., & Yan, Y. (2013). *Applied Surface Science, 285*, 858–864.

---

## YOLOv5s Model
The YOLOv5s network was selected due to its balance between **speed and accuracy**.  
It is the smallest version in the YOLOv5 family, optimized for lightweight, real-time applications.
<img width="940" height="328" alt="image" src="https://github.com/user-attachments/assets/1a68b6a6-c4bf-4563-b869-393951db70c2" />

**Architecture highlights:**
- Input stage with mosaic data augmentation  
- Backbone: CSPDarknet structure for feature extraction  
- Neck: PANet with CSP2_x blocks for feature fusion  
- Output: GIOU loss for bounding box regression  
- Trained using PyTorch with configurable batch size and image resolution  

---

## Project Structure
| File/Folder | Description |
|--------------|-------------|
| `dataset.zip` | Contains the NEU-DET dataset (to be extracted before training). |
| `xml2txt` | Converts annotation files from XML to YOLO `.txt` format. |
| `train_val_split` | Splits the dataset into training, validation, and testing subsets. |
| `data_generate.py` | Prepares data and annotations for YOLOv5 training. |
| `yolov5/` | Folder containing the YOLOv5 source code and configuration files. |
| `neu.yaml` | Dataset configuration file specifying paths to images and labels. |
| `defects_detector.py` | GUI-based script for testing trained YOLOv5 models. |
| `package.yaml` | Environment dependencies list (install using `conda install --file package.yaml`). |

---

## Reference
Khanam, R., & Hussain, M. (2024). *What is YOLOv5: A deep look into the internal features of the popular object detector.* arXiv preprint arXiv:2407.20892.
