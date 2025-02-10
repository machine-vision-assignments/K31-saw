import numpy as np

class Item():

    def __init__(self, bbox, score, label):
        self.bbox = np.array(bbox)
        self.len = self.bbox[3] - self.bbox[1]
        self.used = False
        self.score = score
        self.label = label
        self.zone = None

    def unpack(self):
        return self.bbox, self.score, self.label

    def __str__(self):
        return f"Item {self.label} with score {self.score} in zone {self.zone.name}"

    def __repr__(self):
        return self.__str__()
