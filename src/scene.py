import numpy as np
import cv2 as cv

from settings import PRODUCTION, ZONE_OUT_SIZE
from src.params import ZONES, Zone
from src.detector import Detector

if PRODUCTION:
    from src.camera import RealCamera as Camera
else:
    from src.camera import FakeCamera as Camera

class Scene():

    def __init__(self):
        self.cam = Camera()
        self.zones = [Zone(zone) for zone in ZONES]
        self.display = np.zeros((ZONE_OUT_SIZE[1], (ZONE_OUT_SIZE[0] * 2) + 30, 3), dtype="uint8")
        self._detector = Detector()


    def update(self):
        frame = self.cam.read()

        images = [zone.read(frame) for zone in self.zones]

        zone_data = self._detector.detect(images)

        for zone, data, img in zip(self.zones, zone_data, images):
            zone.update(img, data)


        for zone, image in zip(self.zones, images):
            t1 = zone.pos_front_tr
            t2 = zone.pos_back_tr
            # image[0:int(t1), 0:wi] = (0, 1, 0)
            # image[480 - int(t2):-1, wi:2 * wi] = (0, 1, 0)
            image[int(t1) - 1] = (0, 255, 0)
            image[479 - int(t2)] = (0, 255, 0)



        self.display[:, 0:ZONE_OUT_SIZE[0]] = images[0]
        self.display[:, ZONE_OUT_SIZE[0] + 30:] = images[1]

        cv.imshow("Detail", self.display)




        return frame
