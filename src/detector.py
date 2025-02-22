import numpy as np
import cv2 as cv
import os

import torch

from model.model import ModelV1

from settings import MODEL_PATH, DETECTOR_DEVICE

class Detector():

    def __init__(self):
        self._device = DETECTOR_DEVICE
        self._model = ModelV1()
        self._model.load_state_dict(torch.load(MODEL_PATH, weights_only=True))
        self._model.to(self._device)
        self._model.eval()

    def detect(self, image_list):
        images = np.array(image_list).astype(np.float32) / 255.0
        inputs = torch.tensor(images).permute(0, 3, 1, 2).float().to(self._device)
        with torch.no_grad():
            outputs = self._model(inputs)
        return outputs.cpu().numpy()

