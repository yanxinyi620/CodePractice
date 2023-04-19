from __future__ import print_function

import logging

import grpc
from code_wb.ppc_grpc.proto import helloworld_pb2, helloworld_pb2_grpc
from code_wb.ppc_grpc.proto.helloworld_pb2 import XbinRequest


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to greet world ...")
    # with open('D:/Github/CodePractice/code_wb/ppc_grpc/ca.crt', 'rb') as f:
    # with open('D:/Github/CodePractice/code_wb/ppc_grpc/key/server.pem', 'rb') as f:
    with open('D:/Github/CodePractice/code_wb/ppc_grpc/key/server.pem', 'rb') as f:
        creds = grpc.ssl_channel_credentials(f.read())
    # with grpc.secure_channel('localhost:50051', creds) as channel:
    with grpc.secure_channel('127.0.0.1:50051', creds) as channel:
    # with grpc.secure_channel('192.168.8.102:50051', creds) as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        # model_request = helloworld_pb2.XbinRequest()
        model_request = XbinRequest()
        model_request.job_id = '123'
        model_request.data=bytes(str([1,2,3]), 'utf-8')
        response = stub.sendXbin(model_request)
        # response = stub.sendXbin(helloworld_pb2.XbinRequest(job_id='123', data=bytes(str([1,2,3]), 'utf-8')))

    print("Greeter client received: " + response.job_id)


if __name__ == '__main__':
    logging.basicConfig()
    run()
