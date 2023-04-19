import logging
from concurrent import futures
import grpc
from code_wb.ppc_grpc.proto import helloworld_pb2, helloworld_pb2_grpc


class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)

    def SayHelloAgain(self, request, context):
        return helloworld_pb2.HelloReply(message=f'Hello again, {request.name}!')


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # with open('D:/Github/CodePractice/code_wb/ppc_grpc/ssl.key', 'rb') as f:
    with open('D:/Github/CodePractice/code_wb/ppc_grpc/key/server.key', 'rb') as f:
        private_key = f.read()
    # with open('D:/Github/CodePractice/code_wb/ppc_grpc/ssl.crt', 'rb') as f:
    with open('D:/Github/CodePractice/code_wb/ppc_grpc/key/server.pem', 'rb') as f:
        certificate_chain = f.read()
    server_credentials = grpc.ssl_server_credentials([(private_key, certificate_chain)])
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_secure_port('[::]:' + port, server_credentials)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
