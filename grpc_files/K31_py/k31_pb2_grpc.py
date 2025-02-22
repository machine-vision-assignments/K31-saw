# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import k31_pb2 as k31__pb2


class PipeTrackingStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetSignal = channel.unary_stream(
                '/K31_grpcsrv.PipeTracking/GetSignal',
                request_serializer=k31__pb2.CaptureFilter.SerializeToString,
                response_deserializer=k31__pb2.CaptureSignal.FromString,
                )
        self.SendResult = channel.unary_unary(
                '/K31_grpcsrv.PipeTracking/SendResult',
                request_serializer=k31__pb2.OcrResult.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.UpdatePLCData = channel.unary_stream(
                '/K31_grpcsrv.PipeTracking/UpdatePLCData',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=k31__pb2.ProductionData.FromString,
                )
        self.SendPositionData = channel.stream_unary(
                '/K31_grpcsrv.PipeTracking/SendPositionData',
                request_serializer=k31__pb2.SituationData.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class PipeTrackingServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetSignal(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendResult(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdatePLCData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendPositionData(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PipeTrackingServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetSignal': grpc.unary_stream_rpc_method_handler(
                    servicer.GetSignal,
                    request_deserializer=k31__pb2.CaptureFilter.FromString,
                    response_serializer=k31__pb2.CaptureSignal.SerializeToString,
            ),
            'SendResult': grpc.unary_unary_rpc_method_handler(
                    servicer.SendResult,
                    request_deserializer=k31__pb2.OcrResult.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'UpdatePLCData': grpc.unary_stream_rpc_method_handler(
                    servicer.UpdatePLCData,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=k31__pb2.ProductionData.SerializeToString,
            ),
            'SendPositionData': grpc.stream_unary_rpc_method_handler(
                    servicer.SendPositionData,
                    request_deserializer=k31__pb2.SituationData.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'K31_grpcsrv.PipeTracking', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PipeTracking(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetSignal(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/K31_grpcsrv.PipeTracking/GetSignal',
            k31__pb2.CaptureFilter.SerializeToString,
            k31__pb2.CaptureSignal.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendResult(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/K31_grpcsrv.PipeTracking/SendResult',
            k31__pb2.OcrResult.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdatePLCData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/K31_grpcsrv.PipeTracking/UpdatePLCData',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            k31__pb2.ProductionData.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendPositionData(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/K31_grpcsrv.PipeTracking/SendPositionData',
            k31__pb2.SituationData.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
