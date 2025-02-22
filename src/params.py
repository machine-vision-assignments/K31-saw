import numpy as np
import cv2 as cv

from settings import ZONE_OUT_SIZE

class Zone():

    STATUSES = {
        0: "STAT_NODETECT",  # Na snímku není nic
        1: "STAT_PARTIAL_FRONT",  # Na snímku je viditelný předek vývalku
        2: "STAT_PARTIAL_BACK",  # Na snímku je viditelný zadek vývalku
        3: "STAT_FULL",  # Vývalek zasahuje přes celý rozsah záběru
        4: "STAT_FULL_2SPLIT"  # Na snímku je vývalek a sochor - s mezerou
    }

    def __init__(self, zone):
        self.name = zone["name"]
        self.text_box = zone["text_box"]
        self._corners = zone["corners"]
        self._out_size = ZONE_OUT_SIZE
        self._init_transform()

        self.msg ={
            "PosFront": 0.0,
            "PosBack": 0.0,
            "Status": 0,
            "DropOff": False,
            "Certainty": 0.0,
            "DetInFront": False,
            "DetInBack": False
        }
        self.pos_front_px = 0
        self.pos_back_px = 0
        self._img = None
        self._position = (0, 0)

    def _init_transform(self):
        w, h = self._out_size
        new_pt = np.float32([
            (0, 0), (0, h), (w, h), (w, 0)
        ])
        orig_pt = np.float32(self._corners)
        self._perspective_transform = cv.getPerspectiveTransform(orig_pt, new_pt)
        self._inverse_perspective_transform = np.linalg.inv(self._perspective_transform)

    def read(self, image):
        return cv.warpPerspective(image, self._perspective_transform, self._out_size)

    def read_point(self, x, y, inverse=False) -> tuple[int, int]:
        if inverse:
            M = self._inverse_perspective_transform
        else:
            M = self._perspective_transform
        d = M[2, 0] * x + M[2, 1] * y + M[2, 2]
        return (
            int((M[0, 0] * x + M[0, 1] * y + M[0, 2]) / d), # x
            int((M[1, 0] * x + M[1, 1] * y + M[1, 2]) / d), # y
        )

    def _is(self, v):
        return True if v > 0.05 else False

    def get_status_text(self):
        return self.STATUSES[self.msg["Status"]]

    def update(self, img, data):
        #  * ZONE_OUT_SIZE[1]).astype("int")
        self._img = img

        self._position = data[0:2]

        self.pos_front_tr = data[0] * (ZONE_OUT_SIZE[1] - 1)
        self.pos_back_tr = data[1] * (ZONE_OUT_SIZE[1] - 1)

        state_id = data[2:].argmax()

        self.msg["Status"] = state_id




ZONES = [
    {
        "name": "P1",
        "corners": (  # cols, rows
            (140, 0),  # top left
            (30, 485),  # bottom left
            (200, 485),  # bottom right
            (265, 0),  # top right
        ),
        "text_box": (10, 50),
    },
    {
        "name": "P2",
        "corners": (  # cols, rows
            (360, 0),  # top left
            (465, 485),  # bottom left
            (650, 485),  # bottom right
            (490, 0),  # top right
        ),
        "text_box": (400, 50),
    }
]