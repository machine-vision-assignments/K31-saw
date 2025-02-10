import cv2 as cv

from settings import RECORD_PATH

class Camera():

    def __init__(self):
        self.cam = None
        self._setup()

    def _setup(self):
        raise NotImplementedError

    def read(self):
        ret, frame = self.cam.read()
        if not ret: # TODO catch
            raise
        return frame


class FakeCamera(Camera):

    def _setup(self):
        self.cam = cv.VideoCapture(RECORD_PATH + ".avi")


class RealCamera(Camera):

    def _setup(self):
        self.cam = cv.VideoCapture(0, cv.CAP_DSHOW)