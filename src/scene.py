import numpy as np
import cv2 as cv

from settings import PRODUCTION, ZONE_OUT_SIZE
from src.params import ZONES, Zone

if PRODUCTION:
    from src.camera import RealCamera as Camera
else:
    from src.camera import FakeCamera as Camera

class Scene():

    def __init__(self):
        self.cam = Camera()
        self.zones = [Zone(zone) for zone in ZONES]
        self.display = np.zeros((ZONE_OUT_SIZE[1], (ZONE_OUT_SIZE[0] * 2) + 30, 3), dtype="uint8")

    def update(self):
        frame = self.cam.read()

        imgs = [zone.read(frame) for zone in self.zones]

        self.display[:, 0:ZONE_OUT_SIZE[0]] = imgs[0]
        self.display[:, ZONE_OUT_SIZE[0] + 30:] = imgs[1]

        cv.imshow("Detail", self.display)




        return frame
