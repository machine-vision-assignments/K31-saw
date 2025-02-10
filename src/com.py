import sys
import time
import threading
import queue
import copy
import logging

from readerwriterlock import rwlock
import grpc
import google.protobuf.empty_pb2
from google.protobuf.json_format import MessageToDict

sys.path.append('grpc_files/')
from grpc_files.K31_py import k31_pb2
from grpc_files.K31_py import k31_pb2_grpc


class Com():

    def __init__(self, address):
        self.ADDRESS = address
        self.wd = 1
        self.empty = google.protobuf.empty_pb2.Empty()
        self.received_data_lock = rwlock.RWLockFair()
        self.finish_lock = rwlock.RWLockFair()
        self.received_data = None
        self.finish = False
        self.send_queue = queue.SimpleQueue()

        threading.Thread(target=self._read_stream).start()
        threading.Thread(target=self._send_stream).start()

    def _get_stub(self):
        channel = grpc.insecure_channel(self.ADDRESS)
        return k31_pb2_grpc.PipeTrackingStub(channel)

    def _is_finished(self):
        with self.finish_lock.gen_rlock():
            if self.finish:
                return True
            else:
                return False

    def get_recieved_data(self):
        with self.received_data_lock.gen_rlock():
            if self.received_data is None:
                return None
            data = copy.deepcopy(MessageToDict(self.received_data))
        return data

    def _read_stream(self):
        stub = self._get_stub()
        while True:
            try:
                if self._is_finished(): break
                responses = stub.UpdatePLCData(self.empty)
                for resp in responses:
                    if self._is_finished(): break
                    with self.received_data_lock.gen_wlock():
                        self.received_data = resp
                    time.sleep(0.001)
            except:
                logging.info("Unable to read stream from remote grpc server.")
                time.sleep(3)

    def _send_stream(self):
        stub = self._get_stub()
        while True:
            try:
                if self._is_finished(): break
                stub.SendPositionData(iter(self.send_queue.get, None))
                time.sleep(0.001)
            except:
                logging.info("Unable to send message to remote grpc server.")
                time.sleep(1)

    def send(self, P1, P2):
        msg = self._form_request(P1, P2)
        self.send_queue.put(msg)

    def _form_request(self, P1, P2):
        self.wd += 1
        return k31_pb2.SituationData(
            WD=self.wd,
            P1=k31_pb2.SituationData.DetData(
                PosFront=P1.pos_front,
                PosBack=P1.pos_back,
                Status=k31_pb2.SituationData.EStatus.Value(P1.status),
                DropOff=False,
                Certainty=0,
                DetInFront=P1.zone.photocells[0].active,
                DetInBack=P1.zone.photocells[1].active
            ),
            P2=k31_pb2.SituationData.DetData(
                PosFront=P2.pos_front,
                PosBack=P2.pos_back,
                Status=k31_pb2.SituationData.EStatus.Value(P2.status),
                DropOff=False,
                Certainty=0,
                DetInFront=P2.zone.photocells[0].active,
                DetInBack=P2.zone.photocells[1].active
            ),
        )

    def _form_dummy_request(self):
        self.wd += 1
        return k31_pb2.SituationData(
            WD=self.wd,
            P1=k31_pb2.SituationData.DetData(
                PosFront=1,
                PosBack=2,
                Status=k31_pb2.SituationData.EStatus.STAT_NODETECT,
                DropOff=False
            ),
            P2=k31_pb2.SituationData.DetData(
                PosFront=3,
                PosBack=4,
                Status=k31_pb2.SituationData.EStatus.STAT_FULL,
                DropOff=False
            ),
        )

    def __del__(self):
        self.close()

    def close(self):
        with self.finish_lock.gen_wlock():
            self.finish = True
        self.send_queue.put(None)


if __name__ == "__main__":
    com = Com()
    for k in range(10):
        time.sleep(0.01)
        com.send()
        data = com.get_recieved_data()
        print(data.P2.Production)
    time.sleep(10)
    com.close()
