import json

class FakeCom():

    def __init__(self, path):
        with open(path, "r") as fh:
            self.data = json.load(fh)
        self.idx = 0

    def get_recieved_data(self):
        msg = self.data[self.idx]
        self.idx += 1
        return msg

    def send(self, P1, P2):
        pass
