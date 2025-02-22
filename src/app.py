import numpy as np
import cv2 as cv

from src.recorder import Recorder
from src.com import Com
from src.scene import Scene

from settings import PRODUCTION, GRPC_ADDRESS, WINDOW_POSITION, RECORD_PATH


class App():

    def __init__(self):
        if PRODUCTION:
            self.com = Com(GRPC_ADDRESS) # TODO fix the address
        else:
            from src.fake_com import FakeCom
            self.com = FakeCom()

        self.scene = Scene()
        self.recorder = Recorder()
        self.remote_data = None
        self.window_name = "Pily"

        cv.namedWindow(self.window_name)
        if PRODUCTION:
            cv.moveWindow(self.window_name, WINDOW_POSITION[0], WINDOW_POSITION[1])

    def update(self):
        # self.recorder.feed(frame, self.remote_data) # TODO fix

        frame = self.scene.update()

        self.remote_data = self.com.get_recieved_data()

        self._draw(frame)


    def __del__(self):
        # self.scene.cam.cam.release()
        cv.destroyAllWindows()


    def _draw(self, frame):

        image = frame.copy()
        size = frame.shape[0:2]


        # if key == 32:
        #     self.recorder.switch(self.remote_data)




        for zone in self.scene.zones:

            cv.putText(image,
                       f'{zone.name}  {zone.get_status_text()}', zone.text_box,
                       cv.FONT_HERSHEY_SIMPLEX,
                       0.5, [0, 255, 0],
                       thickness=2)
            # cv.putText(image,
            #            f'{zone.zone_model.pos_back}, {zone.zone_model.pos_front}',
            #            (zone.params["text_box"][0], zone.params["text_box"][1] + 25),
            #            cv.FONT_HERSHEY_SIMPLEX,
            #            0.5, [0, 255, 0],
            #            thickness=2)



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
        if self.remote_data["P1"].get("AutoMode", False):
            cv.putText(image,
                       f'AUTO', (10, 460),
                       cv.FONT_HERSHEY_SIMPLEX,
                       0.60, [0, 255, 0],
                       thickness=2)
        else:
            cv.putText(image,
                       f'MAN', (10, 460),
                       cv.FONT_HERSHEY_SIMPLEX,
                       0.60, [19, 166, 250],
                       thickness=2)

        if self.remote_data["P2"].get("AutoMode", False):
            cv.putText(image,
                       f'AUTO', (400, 460),
                       cv.FONT_HERSHEY_SIMPLEX,
                       0.60, [0, 255, 0],
                       thickness=2)
        else:
            cv.putText(image,
                       f'MAN', (400, 460),
                       cv.FONT_HERSHEY_SIMPLEX,
                       0.60, [19, 166, 250],
                       thickness=2)
    #
    #     name = f"{self.window_name}"
    #     cv.imshow(name, image)
    #     key = cv.waitKey(1)
    #     if key == 32:
    #         self.recorder.switch(self.remote_data)

        cv.imshow(self.window_name, image)
        key = cv.waitKey(1)
