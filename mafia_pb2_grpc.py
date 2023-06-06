# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import mafia_pb2 as mafia__pb2


class MafiaStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Connect = channel.unary_unary(
                '/mafia.Mafia/Connect',
                request_serializer=mafia__pb2.UserName.SerializeToString,
                response_deserializer=mafia__pb2.UserId.FromString,
                )
        self.Disconnect = channel.unary_unary(
                '/mafia.Mafia/Disconnect',
                request_serializer=mafia__pb2.UserId.SerializeToString,
                response_deserializer=mafia__pb2.DisconnectResponse.FromString,
                )
        self.GetUsers = channel.unary_stream(
                '/mafia.Mafia/GetUsers',
                request_serializer=mafia__pb2.GetUsersRequest.SerializeToString,
                response_deserializer=mafia__pb2.User.FromString,
                )


class MafiaServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Connect(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Disconnect(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUsers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MafiaServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Connect': grpc.unary_unary_rpc_method_handler(
                    servicer.Connect,
                    request_deserializer=mafia__pb2.UserName.FromString,
                    response_serializer=mafia__pb2.UserId.SerializeToString,
            ),
            'Disconnect': grpc.unary_unary_rpc_method_handler(
                    servicer.Disconnect,
                    request_deserializer=mafia__pb2.UserId.FromString,
                    response_serializer=mafia__pb2.DisconnectResponse.SerializeToString,
            ),
            'GetUsers': grpc.unary_stream_rpc_method_handler(
                    servicer.GetUsers,
                    request_deserializer=mafia__pb2.GetUsersRequest.FromString,
                    response_serializer=mafia__pb2.User.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mafia.Mafia', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Mafia(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Connect(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mafia.Mafia/Connect',
            mafia__pb2.UserName.SerializeToString,
            mafia__pb2.UserId.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Disconnect(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mafia.Mafia/Disconnect',
            mafia__pb2.UserId.SerializeToString,
            mafia__pb2.DisconnectResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetUsers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/mafia.Mafia/GetUsers',
            mafia__pb2.GetUsersRequest.SerializeToString,
            mafia__pb2.User.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)