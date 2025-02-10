import onnxruntime as ort
import numpy as np
import cv2 as cv
import os

from src.items import Item

class Detector():

    def __init__(self, model_path, model_classes, conf_threshold, iou_threshold):

        self.CONF_THRESHOLD = conf_threshold
        self.IOU_THRESHOLD = iou_threshold

        self.CLASSES = model_classes
        self.session = ort.InferenceSession(model_path, providers=["CUDAExecutionProvider"])
        ort.set_default_logger_severity(0)

        model_inputs = self.session.get_inputs()
        self.input_names = [model_inputs[i].name for i in range(len(model_inputs))]
        input_shape = model_inputs[0].shape
        self.img_height, self.img_width = input_shape[2:]
        self.input_shape = np.array([
            self.img_width, self.img_height, self.img_width, self.img_height
        ])


        model_output = self.session.get_outputs()
        self.output_names = [model_output[i].name for i in range(len(model_output))]

    def _get_area(self, boxes):
        return [(box[2] - box[0]) * (box[3] - box[1]) for box in boxes]

    def _nms(self, boxes, scores, iou_threshold):
        sorted_indices = np.argsort(scores)[::-1]
        keep_boxes = []
        while sorted_indices.size > 0:
            # Pick the last box
            box_id = sorted_indices[0]
            keep_boxes.append(box_id)

            # Compute IoU of the picked box with the rest
            ious = self._compute_iou(boxes[box_id, :], boxes[sorted_indices[1:], :])

            # Remove boxes with IoU over the threshold
            keep_indices = np.where(ious < iou_threshold)[0]

            # print(keep_indices.shape, sorted_indices.shape)
            sorted_indices = sorted_indices[keep_indices + 1]

        return keep_boxes

    def _compute_iou(self, box, boxes):
        # Compute xmin, ymin, xmax, ymax for both boxes
        xmin = np.maximum(box[0], boxes[:, 0])
        ymin = np.maximum(box[1], boxes[:, 1])
        xmax = np.minimum(box[2], boxes[:, 2])
        ymax = np.minimum(box[3], boxes[:, 3])

        # Compute intersection area
        intersection_area = np.maximum(0, xmax - xmin) * np.maximum(0, ymax - ymin)

        # Compute union area
        box_area = (box[2] - box[0]) * (box[3] - box[1])
        boxes_area = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
        union_area = box_area + boxes_area - intersection_area # original
        iou = intersection_area / union_area # that was original solution
        return iou

    def _xywh2xyxy(self, x):
        # Convert bounding box (x, y, w, h) to bounding box (x1, y1, x2, y2)
        y = np.copy(x)
        y[..., 0] = x[..., 0] - x[..., 2] / 2
        y[..., 1] = x[..., 1] - x[..., 3] / 2
        y[..., 2] = x[..., 0] + x[..., 2] / 2
        y[..., 3] = x[..., 1] + x[..., 3] / 2
        return y

    def detect(self, image):
        image_draw = image.copy()
        image_height, image_width = image.shape[:2]
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        resized = cv.resize(image, (self.img_width, self.img_height))

        input_image = resized / 255.0
        input_image = input_image.transpose(2, 0, 1)
        input_tensor = input_image[np.newaxis, :, :, :].astype(np.float32)

        outputs = self.session.run(self.output_names, {self.input_names[0]: input_tensor})[0]

        predictions = np.squeeze(outputs).T
        scores = np.max(predictions[:, 4:], axis=1)
        predictions = predictions[scores > self.CONF_THRESHOLD, :]
        scores = scores[scores > self.CONF_THRESHOLD]

        class_ids = np.argmax(predictions[:, 4:], axis=1)
        boxes = predictions[:, :4]
        boxes = np.divide(boxes, self.input_shape, dtype=np.float32)
        boxes *= np.array([image_width, image_height, image_width, image_height])
        boxes = boxes.astype(np.int32)

        boxes = self._xywh2xyxy(boxes)

        indices = self._nms(boxes, scores, self.IOU_THRESHOLD)

        return [Item(boxes[idx], scores[idx], class_ids[idx]) for idx in indices]
