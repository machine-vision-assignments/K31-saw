import numpy as np
import cv2 as cv

from settings import ZONE_OUT_SIZE

class Zone():

    def __init__(self, zone):
        self.name = zone["name"]
        self._corners = zone["corners"]
        self._out_size = ZONE_OUT_SIZE
        self._init_transform()

    def _init_transform(self):
        w, h = self._out_size
        new_pt = np.float32([
            (0, 0), (0, h), (w, h), (w, 0)
        ])
        orig_pt = np.float32(self._corners)
        self._perspective_transform = cv.getPerspectiveTransform(orig_pt, new_pt)

    def read(self, image):
        return cv.warpPerspective(image, self._perspective_transform, self._out_size)

    def read_point(self, x, y) -> tuple[int, int]:
        M = self._perspective_transform
        d = M[2, 0] * x + M[2, 1] * y + M[2, 2]
        return (
            int((M[0, 0] * x + M[0, 1] * y + M[0, 2]) / d), # x
            int((M[1, 0] * x + M[1, 1] * y + M[1, 2]) / d), # y
        )


ZONES = [
    {
        "name": "P1",
        "corners": (  # cols, rows
            (140, 0),  # top left
            (30, 485),  # bottom left
            (200, 485),  # bottom right
            (265, 0),  # top right
        ),
    },
    {
        "name": "P2",
        "corners": (  # cols, rows
            (360, 0),  # top left
            (465, 485),  # bottom left
            (650, 485),  # bottom right
            (490, 0),  # top right
        ),
    }
]