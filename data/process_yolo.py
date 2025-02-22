import os
import sys

import cv2 as cv

sys.path.append("..")
from src.params import ZONES, Zone

zones = [Zone(zone) for zone in ZONES]


# Paths to your dataset folders
images_folder = "dataset/train/images"
labels_folder = "dataset/train/labels"

# Load class names (if a classes.txt file exists)
classes_file = "classes.txt"
if os.path.exists(classes_file):
    with open(classes_file, "r") as f:
        class_names = f.read().strip().split("\n")
else:
    class_names = None

# Iterate over images in the "images" folder
for idx, image_file in enumerate(os.listdir(images_folder)):
    if not image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue

    # Read the image
    image_path = os.path.join(images_folder, image_file)
    image = cv.imread(image_path)
    orig_image = image.copy()
    height, width, _ = image.shape

    # Corresponding label file
    label_file = os.path.join(labels_folder, os.path.splitext(image_file)[0] + ".txt")
    if not os.path.exists(label_file):
        print(f"No label file for {image_file}")
        continue


    imgs = [zone.read(image) for zone in zones]

    # Read bounding boxes from the label file
    p1_items = []
    p2_items = []
    with open(label_file, "r") as f:
        for line in f:
            data = line.strip().split()
            if len(data) < 5:
                print(f"Malformed line in {label_file}: {line}")
                continue

            class_id, x_center, y_center, box_width, box_height = map(float, data[:5])

            x_center, y_center = x_center * width, y_center * height
            box_width, box_height = box_width * width, box_height * height
            x1, y1 = int(x_center - box_width / 2), int(y_center - box_height / 2)
            x2, y2 = int(x_center + box_width / 2), int(y_center + box_height / 2)

            if class_id == 1:
                x1w, y1w = zones[0].read_point(x1, y1)
                x2w, y2w = zones[0].read_point(x2, y2)
                if x_center / width > 0.5:
                    p2_items.append([y1w / height, y2w / height])
                else:
                    p1_items.append([y1w / height, y2w / height])


            # Draw the bounding box and label
            color = (0, 255, 0)  # Green color for boxes
            cv.rectangle(image, (x1, y1), (x2, y2), color, 2)
            if class_names and int(class_id) < len(class_names):
                label = class_names[int(class_id)]
                cv.putText(image, label, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


    for label, items, img_clean in zip(["P1", "P2"], [p1_items, p2_items], imgs):
        o1 = 0
        o2 = 0
        st = 0
        valid = True
        img = img_clean.copy()
        for item in items:
            y1, y2 = int(item[0] * height), int(item[1] * height)
            img[y1:y2, 0:5] = (0, 125, 255)
            img[y1, :] = (0, 125, 255)
            img[y2-1, :] = (0, 125, 255)
            if not (item[0] < 0.05 or item[1] > 0.95):
                valid = False
            elif item[0] < 0.05 and item[1] > 0.95:
                o1, o2 = img.shape[0], 0
            elif item[0] < 0.05:
                o1 = y2
            elif item[1] > 0.95:
                o2 = img.shape[0] - y1

        # asign state
        if o1 > 0.99 * 480 and not o2 > 0.01 * 480:
            st = 3
        elif not o1 > 0.01 * 480 and not o2 > 0.01 * 480:
            st = 0
        elif o1 > 0.01 * 480 and not o2 > 0.01 * 480:
            st = 1 # front
        elif not o1 > 0.01 * 480 and o2 > 0.01 * 480:
            st = 2 # back
        elif o1 > 0.01 * 480 and o2 > 0.01 * 480:
            st = 4

        cv.imshow(label, img)

        if valid:
            name = f"new_data/image_{idx}-{o1}_{o2}_{st}-valid.jpg"
            cv.imwrite(name, img_clean)
            name = f"orig_data/image_{idx}-{o1}_{o2}_{st}-valid.jpg"
            cv.imwrite(name, orig_image)
            print(name)
        # else:
        #     key = cv.waitKey(10000)


    # Show the image with bounding boxes
    # cv.imshow("P1", imgs[0])
    # cv.imshow("P2", imgs[1])
    cv.imshow("orig", image)
    key = cv.waitKey(1)  # Press any key to move to the next image
    if key == 27:  # Exit on pressing ESC
        break

cv.destroyAllWindows()