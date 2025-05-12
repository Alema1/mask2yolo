import os
import cv2
import numpy as np

# === Directory paths ===
base_dir = r"D:\your-path"
images_dir = os.path.join(base_dir, "images")
labels_dir = os.path.join(base_dir, "labels")
yolo_labels_dir = os.path.join(base_dir, "yolo_labels")
os.makedirs(yolo_labels_dir, exist_ok=True)

# === Color-to-class mapping (BGR format) ===
color2class = {
    (0, 0, 128): 0,      # Red → Johnson grass
    (0, 128, 128): 1,    # Yellow → Field bindweed
    (128, 0, 0): 2       # Blue → Purslane
}

def get_class_id_from_color(color):
    """Convert a BGR color to a class ID."""
    bgr = tuple(int(c) for c in color)
    return color2class.get(bgr, None)

# === Process all segmentation masks ===
for filename in os.listdir(labels_dir):
    if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
        continue

    mask_path = os.path.join(labels_dir, filename)
    image_path = os.path.join(images_dir, filename)
    yolo_label_path = os.path.join(
        yolo_labels_dir, os.path.splitext(filename)[0] + ".txt"
    )

    # Load images
    mask = cv2.imread(mask_path)
    rgb_img = cv2.imread(image_path)
    h, w, _ = mask.shape

    # Convert to grayscale and binarize
    mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    _, mask_bin = cv2.threshold(mask_gray, 1, 255, cv2.THRESH_BINARY)

    # Find contours in binary mask
    contours_list, _ = cv2.findContours(
        mask_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    yolo_lines = []

    for contour in contours_list:
        x, y, box_w, box_h = cv2.boundingRect(contour)
        M = cv2.moments(contour)

        if M["m00"] == 0:
            continue

        # Get color from mask at contour center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        color = mask[cY, cX]
        class_id = get_class_id_from_color(color)

        if class_id is None:
            continue  # Skip unknown or background regions

        # Normalize bounding box to YOLO format
        x_center = (x + box_w / 2) / w
        y_center = (y + box_h / 2) / h
        width = box_w / w
        height = box_h / h

        yolo_line = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
        yolo_lines.append(yolo_line)

    # Save YOLO annotation file
    if yolo_lines:
        with open(yolo_label_path, "w") as f:
            f.write("\n".join(yolo_lines))

print("✅ Conversion completed! YOLO annotations saved to:", yolo_labels_dir)
