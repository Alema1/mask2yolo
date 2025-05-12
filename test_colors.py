import os
import cv2
import numpy as np

labels_dir = r"D:\Treinamento\datasets\Cofly\CoFly-WeedDB\labels"

unique_colors = set()

for filename in os.listdir(labels_dir):
    if filename.lower().endswith((".png", ".jpg")):
        mask = cv2.imread(os.path.join(labels_dir, filename))
        for row in mask:
            for pixel in row:
                unique_colors.add(tuple(pixel))

print("Cores únicas encontradas nas máscaras:")
for color in sorted(unique_colors):
    print(color)
