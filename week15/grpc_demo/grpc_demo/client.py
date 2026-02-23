import grpc
import schema_pb2_grpc
import schema_pb2

if __name__ == "__main__":
  channel = grpc.insecure_channel("localhost:9000")
  stub = schema_pb2_grpc.CalculateServiceStub(channel)
  response = stub.Add(schema_pb2.AddRequest(lhs=2, rhs=3))
  print(f"result was: {response.result}")
  channel.close()


