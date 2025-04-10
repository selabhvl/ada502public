import grpc
from concurrent import futures
import grpc_demo.schema_pb2 as schema_pb2
import grpc_demo.schema_pb2_grpc as schema_pb2_grpc

class CalcService(schema_pb2_grpc.CalculateServiceServicer):

  def Add(self, request, context):
    result = request.lhs + request.rhs
    return schema_pb2.Result(result=result)

if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    schema_pb2_grpc.add_CalculateServiceServicer_to_server(CalcService(), server)
    server.add_insecure_port("127.0.0.1:9000")
    server.start()
    print("listening on :9000")
    server.wait_for_termination()
