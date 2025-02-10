import copy

import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from src.items import Item

class Ruler():

    def __init__(self, coeffs, ruler):
        self.zero = ruler[2]
        self.c = np.array(coeffs)

    def calc_distance(self, value):
        value -= self.zero
        return self.c[0] + (self.c[1] * value) + (self.c[2] * value ** 2)


class PhotoCell():

    def __init__(self, level):
        self.level = level
        self.active = False

    def update(self, items):
        self.active = False
        for item in items:
            if item.bbox[1] < self.level < item.bbox[3]:
                self.active = True
                return

class ZoneModel():

    NONE = -120000

    def __init__(self, zone):
        """
        status = STAT_NODETECT | STAT_FULL | STAT_FULL_2SPLIT | STAT_PARTIAL_FRONT | STAT_PARTIAL BACK

        :param zone:
        """
        self.zone = zone
        self.status = "STAT_NODETECT"
        self.pos_front = None
        self.pos_back = None
        self.data = {}

    def update(self, msg):
        self.status = msg["Status"]
        self.pos_front = msg.get("PosFront", self.NONE)
        self.pos_back = msg.get("PosBack", self.NONE)
        self.data = msg


class Zone():

    def __init__(self, data):
        self.zone_model = ZoneModel(self)
        self.photocells = [PhotoCell(level) for level in data["photocells"]]
        self.name = data["name"]
        self.pts = np.array(data["corners"], np.int32)
        self.ruler = Ruler(data["ruler_equation"], data["ruler"])
        self.key = data["key_idx"]
        self.color = (255, 0, 0)
        self.poly = Polygon(self.pts)
        self.bottom_level = data["bottom_level"]
        self.top_level = data["top_level"]
        self.params = data

    def evaluate(self, items):
        self.items = []
        for item in items:
            if self.contains(item):
                self.items.append(item)
                item.zone = self
                item.top = self._is_at_top(item)
                item.bottom = self._is_at_bottom(item)

        # self.items.append(copy.deepcopy(self.items[0]))
        # self.items.append(copy.deepcopy(self.items[0]))
        # self.items.append(copy.deepcopy(self.items[0]))
        # # self.items.append(copy.deepcopy(self.items[0]))
        # self.items[0].score = 0
        # self.items[2].score = 0.5

        rods = [item for item in self.items if item.label == 1 and (item.top or item.bottom)]
        rods.sort(key=lambda rod: rod.score * rod.len, reverse=True) # TODO is the multiplication smart?

        for photocell in self.photocells:
            photocell.update(rods)


        targets = {}


        for rod in rods:
            if not "full" in targets and rod.top and rod.bottom:
                rod.used = True
                targets["full"] = rod
            elif not "top" in targets and rod.top and not rod.bottom:
                rod.used = True
                targets["top"] = rod
            elif not "bottom" in targets and not rod.top and rod.bottom:
                rod.used = True
                targets["bottom"] = rod
            # else:
            #     targets["middle"] = rod

        if "full" in targets: # TODO rod.used should be here to avoid FULL + something combo
            msg = self._process_full(targets["full"])
        elif not "full" in targets and "bottom" in targets and not "top" in targets:
            msg = self._process_back(targets["bottom"])
        elif not "full" in targets and not "bottom" in targets and "top" in targets:
            msg = self._process_front(targets["top"])
        elif not "full" in targets and "bottom" in targets and "top" in targets:
            msg = self._process_full_2split(targets["top"], targets["bottom"])
        else:
            msg = self._process_none()
        print(msg)
        self.zone_model.update(msg)





    def _process_none(self):
        return {
            "Status": "STAT_NODETECT",
            "Certainty": 0,
        }

    def _process_full(self, rod):
        return {
            "Status": "STAT_FULL",
            "Certainty": 0,
        }

    def _process_front(self, rod):
        pos = self.ruler.calc_distance(rod.bbox[3])
        return {
            "Status": "STAT_PARTIAL_FRONT",
            "PosFront": round(pos, 1),
            "Certainty": 0,
        }

    def _process_back(self, rod):
        pos = self.ruler.calc_distance(rod.bbox[1])
        return {
            "Status": "STAT_PARTIAL_BACK",
            "PosBack": round(pos, 1),
            "Certainty": 0,
        }

    def _process_full_2split(self, rod_bottom, rod_top):
        return {
            "Status": "STAT_FULL_2SPLIT",
            "PosFront": self.ruler.calc_distance(rod_top.bbox[3]),
            "PosBack": self.ruler.calc_distance(rod_bottom.bbox[1]),
            "Certainty": 0,
        }

    # def _is_above(self):
    #     """Above saw"""
    #     return

    def _is_at_bottom(self, item):
        return item.bbox[3] > self.bottom_level

    def _is_at_top(self, item):
        return item.bbox[1] < self.top_level

    def contains(self, item):
        point = Point(item.bbox[self.key])
        return self.poly.contains(point)
