# mask2yolo

Converts a segmentation dataset (with color-coded masks) into object detection labels in YOLO format using bounding boxes derived from contour detection.

## 🧠 Overview

This tool reads segmentation masks where each object class is represented by a unique RGB color. It detects object contours, computes bounding boxes, and saves YOLO-format `.txt` annotation files compatible with YOLOv5, YOLOv8, and other detection frameworks.

Example input:
- Images: `images/`
- Masks: `labels/` (color-coded PNG masks)

Output:
- YOLO annotations: `yolo_labels/`
- Optional: `classes.txt` for mapping class IDs to names

## 📁 Dataset structure (input)

```
your-dataset/
├── images/
│ ├── image1.png
│ ├── image2.png
│ └── ...
├── labels/
│ ├── image1.png
│ ├── image2.png
│ └── ...
```

## ⚙️ How to use

1. Edit the script and configure:
   - The path to your dataset
   - The color-to-class mapping

```python
color2class = {
    (0, 0, 128): 0,      # Johnson grass (red)
    (0, 128, 128): 1,    # Field bindweed (yellow)
    (128, 0, 0): 2       # Purslane (blue)
}
```
---------------------------------------------------------------------------------------------
✅ Tip: To identify the exact BGR colors used in your masks, run the included helper script:

python test_colors.py

---------------------------------------------------------------------------------------------

# YOLO Dataset Split Script

This repository contains a Python script to split an image dataset with YOLO-format annotations into training, validation, and test sets.

## 📁 Dataset Split Script (`create_yolo.py`)

This script automates the preparation of a dataset for training YOLO-based object detection models. It performs the following steps:

1. **Reads image and label files** from a YOLO-style dataset structure.
2. **Prompts the user** to define the split ratio for training and validation.
3. **Shuffles and splits the dataset** into training, validation, and test sets.
4. **Creates a new output directory** (`dataset_yolo_split/`) containing the final dataset:
   - `train/images` & `train/labels`
   - `val/images` & `val/labels`
   - `test/images` & `test/labels`
5. **Copies only images that have annotations** (i.e., labels) to avoid inconsistencies.
6. **Generates a `data.yaml`** file with relative paths (`../`) pointing to each split, ready for YOLO training frameworks like Ultralytics.

### ✅ Expected Folder Structure (after execution):

```
dataset_yolo_split/
├── train/
│   ├── images/
│   └── labels/
├── val/
│   ├── images/
│   └── labels/
├── test/
│   ├── images/
│   └── labels/
└── data.yaml
```

### 📝 Usage

1. Place the script in your base dataset folder.
2. Make sure you have:
   - An `images/` folder containing `.jpg`, `.png`, or `.jpeg` files.
   - A `labels/` folder with YOLO-format `.txt` annotations matching each image.
   - A `classes.txt` file listing class names (one per line).
3. Run the script:

```bash
python create_yolo_split.py
```

4. Enter the desired train/validation split percentages when prompted.

## 📦 Requirements

This script uses only Python standard libraries:
- `os`
- `shutil`
- `random`

No additional packages are needed.
