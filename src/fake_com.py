import json

from settings import RECORD_PATH

class FakeCom():

    def __init__(self):
        path = RECORD_PATH + ".json"
        with open(path, "r") as fh:
            self.data = json.load(fh)
        self.idx = 0

    def get_recieved_data(self):
        msg = self.data[self.idx]
        self.idx += 1
        return msg

    def send(self, P1, P2):
        pass
