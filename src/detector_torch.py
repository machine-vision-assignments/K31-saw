from ultralytics import YOLO

import numpy as np
import cv2 as cv
import os

import torch

from src.items import Item

class Detector():

    def __init__(self, model_path, model_classes, conf_threshold, iou_threshold):

        self.CONF_THRESHOLD = conf_threshold
        self.IOU_THRESHOLD = iou_threshold

        self.CLASSES = model_classes

        torch.cuda.set_device(0)

        model_path = os.path.join("model","best.pt")

        self.model = YOLO(model_path)


    def detect(self, image):
        results = self.model.predict(image, verbose=False, conf=self.CONF_THRESHOLD, iou=self.IOU_THRESHOLD)

        items = []
        for result in results:
            if len(result.cpu().boxes.xyxy) > 0:
                boxes = np.array(result.cpu().boxes.xyxy, dtype="int")
                labels = result.boxes.cls
                scores = result.boxes.conf
                for box, label, score in zip(boxes, labels, scores):
                    items.append(
                        Item(box, float(score), int(label))
                    )
        return items


