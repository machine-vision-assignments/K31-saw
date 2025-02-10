import json
import os
from datetime import datetime

#from google.protobuf.json_format import MessageToJson
import cv2 as cv

class Recorder():

    def __init__(self):
        self.running = False
        self.size = (640, 480)
        self.fps = 20
        self.filename = None
        if not os.path.exists('recordings'):
            os.makedirs('recordings')

    def feed(self, frame, data):
        if self.running:
            self.writer.write(frame)
            if not os.path.isfile(self.filename + ".json"):
                with open(self.filename + ".json", "a") as fh:
                    fh.write("[")
                    json_data = json.dumps(data, indent=4, sort_keys=True)
                    # json_data = MessageToJson(data)
                    fh.write(json_data)
            else:
                with open(self.filename + ".json", "a") as fh:
                    # json_data = MessageToJson(data)
                    json_data = json.dumps(data, indent=4, sort_keys=True)
                    fh.write("," + json_data)

    def switch(self, data):
        if self.running:
            self.running = False
            self.writer.release()
            with open(self.filename + ".json", "a") as fh:
                fh.write("]")
        else:
            self.running = True
            date_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            if not data is None:
                s1 = data["P1"].get("Size", 0)
                s2 = data["P2"].get("Size", 0)
                size = int(max(s1, s2))
            else:
                size = "x"
            self.filename = os.path.join("recordings", f"data-{size}-{date_time}")
            self.writer = cv.VideoWriter(self.filename + ".avi",
                                         cv.VideoWriter_fourcc(*'DIVX'), self.fps, self.size)
