import numpy as np
import cv2 as cv

from src.recorder import Recorder
from src.com import Com
from src.fake_com import FakeCom
from src.scene import Scene

from settings import PRODUCTION, GRPC_ADDRESS, WINDOW_POSITION, RECORD_PATH


class App():

    def __init__(self):
        if PRODUCTION:
            self.com = Com(GRPC_ADDRESS)
        else:
            self.com = FakeCom(RECORD_PATH + ".json")

        self.scene = Scene()
        self.recorder = Recorder()
        self.remote_data = None
        self.window_name = "Pily"

        cv.namedWindow(self.window_name)
        if PRODUCTION:
            cv.moveWindow(self.window_name, WINDOW_POSITION[0], WINDOW_POSITION[1])

    def update(self):
        # self.recorder.feed(frame, self.remote_data)

        frame = self.scene.update()

        self.remote_data = self.com.get_recieved_data()

        self._draw(frame)


    def __del__(self):
        # self.scene.cam.cam.release()
        cv.destroyAllWindows()


    def _draw(self, frame):

        image = frame.copy()
        size = frame.shape[0:2]

        cv.imshow(self.window_name, image)
        key = cv.waitKey(1)
        # if key == 32:
        #     self.recorder.switch(self.remote_data)
        
        
    #
    #     for zone in self.zones:
    #         # pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
    #         pts = zone.pts.reshape((-1,1,2))
    #         cv.polylines(image, [pts], True,(0,255,255))
    #
    #
    #     for item in self.items:
    #         bbox, score, label = item.unpack()
    #         bbox = bbox.round().astype(np.int32)
    #         cls_id = int(label)
    #         cls = self.CLASSES[cls_id]
    #
    #         # cv.circle(image, bbox[[0, 3]], 5, (255, 255, 255), -1)
    #
    #         if item.zone == None:
    #             color = (0, 0, 255)
    #         else:
    #             color = item.zone.color
    #
    #         thick = 3 if item.used else 1
    #         cv.rectangle(image, tuple(bbox[:2]), tuple(bbox[2:]), color, thick)
    #         cv.putText(image,
    #                    f'{cls}:{int(score * 100)}', (bbox[0], bbox[1] - 2),
    #                    cv.FONT_HERSHEY_SIMPLEX,
    #                    0.60, [225, 255, 255],
    #                    thickness=1)
    #
    #     for zone in self.zones:
    #         cv.putText(image,
    #                    f'{zone.name}  {zone.zone_model.status}', zone.params["text_box"],
    #                    cv.FONT_HERSHEY_SIMPLEX,
    #                    0.5, [0, 255, 0],
    #                    thickness=2)
    #         cv.putText(image,
    #                    f'{zone.zone_model.pos_back}, {zone.zone_model.pos_front}',
    #                    (zone.params["text_box"][0], zone.params["text_box"][1] + 25),
    #                    cv.FONT_HERSHEY_SIMPLEX,
    #                    0.5, [0, 255, 0],
    #                    thickness=2)
    #
    #     if self.recorder.running:
    #         cv.circle(image, (30, 380), 15, (0, 0, 255), -1)
    #
    #
    #     for zone in self.zones:
    #         delta = 30
    #         x = (image.shape[1] - delta) if zone.name == "P2" else delta
    #         for photocell in zone.photocells:
    #             color = (255, 255, 255) if photocell.active else (130, 125, 50)
    #             cv.circle(image, (x, photocell.level), 10, (150, 140, 0), -1)
    #             cv.circle(image, (x, photocell.level), 7, color, -1)
    #
    #
    #     s1 = self.remote_data["P1"].get("Speed", None)
    #     s2 = self.remote_data["P2"].get("Speed", None)
    #     p1a, p1b = (30, 400), (30, 440)
    #     p2a, p2b = (size[1] - 30, 400), (size[1] - 30, 440)
    #     if not s1 is None:
    #         pa, pb = (p1a, p1b) if s1 > 0 else (p1b, p1a)
    #         cv.arrowedLine(image, pa, pb,
    #                                 (0, 255, 0), 5, tipLength=0.5)
    #     if not s2 is None:
    #         pa, pb = (p2a, p2b) if 21 > 0 else (p2b, p2a)
    #         cv.arrowedLine(image, pa, pb,
    #                                 (0, 255, 0), 5, tipLength=0.5)
    #
    #     if self.remote_data["P1"].get("AutoMode", False):
    #         cv.putText(image,
    #                    f'AUTO', (10, 460),
    #                    cv.FONT_HERSHEY_SIMPLEX,
    #                    0.60, [0, 255, 0],
    #                    thickness=2)
    #     else:
    #         cv.putText(image,
    #                    f'MAN', (10, 460),
    #                    cv.FONT_HERSHEY_SIMPLEX,
    #                    0.60, [19, 166, 250],
    #                    thickness=2)
    #
    #     if self.remote_data["P2"].get("AutoMode", False):
    #         cv.putText(image,
    #                    f'AUTO', (400, 460),
    #                    cv.FONT_HERSHEY_SIMPLEX,
    #                    0.60, [0, 255, 0],
    #                    thickness=2)
    #     else:
    #         cv.putText(image,
    #                    f'MAN', (400, 460),
    #                    cv.FONT_HERSHEY_SIMPLEX,
    #                    0.60, [19, 166, 250],
    #                    thickness=2)
    #
    #     name = f"{self.window_name}"
    #     cv.imshow(name, image)
    #     key = cv.waitKey(1)
    #     if key == 32:
    #         self.recorder.switch(self.remote_data)
