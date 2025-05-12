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

```python
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
✅ Tip: To identify the exact BGR colors used in your masks, run the included helper script:

python test_colors.py
