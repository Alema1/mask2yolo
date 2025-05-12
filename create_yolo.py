import os
import random
import shutil

# Function to randomly split a dataset into train, validation, and test sets
def split_dataset(images, split_ratio_train=0.8, split_ratio_val=0.1):
    random.shuffle(images)
    total_images = len(images)
    train_idx = int(total_images * split_ratio_train)
    val_idx = int(total_images * split_ratio_val)

    # Slicing image list into train/val/test sets
    train_images = images[:train_idx]
    val_images = images[train_idx:train_idx + val_idx]
    test_images = images[train_idx + val_idx:]

    return train_images, val_images, test_images

# Function to copy image and label pairs into the appropriate directories
def copy_images_and_labels(images, dest_images_dir, dest_labels_dir, labels_dir):
    for image_path in images:
        image_name = os.path.basename(image_path)
        label_name = os.path.splitext(image_name)[0] + ".txt"
        label_path = os.path.join(labels_dir, label_name)

        # Copy image
        shutil.copy(image_path, dest_images_dir)

        # Copy label only if it exists
        if os.path.exists(label_path):
            shutil.copy(label_path, dest_labels_dir)

# Function to generate the YOLO-compatible data.yaml file
def generate_yaml(output_dir, num_classes, class_names):
    yaml_content = f"""
train: ../train/images
val: ../val/images
test: ../test/images

nc: {num_classes}

names:
"""
    for idx, name in enumerate(class_names):
        yaml_content += f"  {idx}: '{name}'\n"

    with open(os.path.join(output_dir, "data.yaml"), "w") as yaml_file:
        yaml_file.write(yaml_content)
    print(f"✅ data.yaml file successfully generated!")

# Base dataset directory (containing 'images', 'labels', 'classes.txt')
base_dir = r"D:\your-path"
images_dir = os.path.join(base_dir, "images")
labels_dir = os.path.join(base_dir, "labels")

# Output directory to store the split dataset
output_dir = os.path.join(base_dir, "dataset_yolo_split")
os.makedirs(output_dir, exist_ok=True)

# Create subdirectories for train/val/test splits
train_dir = os.path.join(output_dir, "train")
val_dir = os.path.join(output_dir, "val")
test_dir = os.path.join(output_dir, "test")

for split in [train_dir, val_dir, test_dir]:
    os.makedirs(os.path.join(split, "images"), exist_ok=True)
    os.makedirs(os.path.join(split, "labels"), exist_ok=True)

# Load class names from classes.txt
classes_file = os.path.join(base_dir, "classes.txt")
with open(classes_file, "r") as f:
    class_names = [line.strip() for line in f.readlines()]

# Collect all image files
image_files = [
    os.path.join(images_dir, f)
    for f in os.listdir(images_dir)
    if f.lower().endswith((".png", ".jpg", ".jpeg"))
]

# Ask the user for train and validation split ratios
train_ratio = float(input("Enter train split (0 to 1, e.g., 0.8 for 80%): "))
val_ratio = float(input("Enter validation split (0 to 1, e.g., 0.1 for 10%): "))

# Perform dataset split
train_images, val_images, test_images = split_dataset(image_files, train_ratio, val_ratio)

# Copy images and corresponding labels to the respective folders
copy_images_and_labels(train_images, os.path.join(train_dir, "images"), os.path.join(train_dir, "labels"), labels_dir)
copy_images_and_labels(val_images, os.path.join(val_dir, "images"), os.path.join(val_dir, "labels"), labels_dir)
copy_images_and_labels(test_images, os.path.join(test_dir, "images"), os.path.join(test_dir, "labels"), labels_dir)

# Generate the YAML config file for YOLO training
generate_yaml(output_dir, len(class_names), class_names)

print("✅ Dataset split and configuration complete. Output saved in:", output_dir)
