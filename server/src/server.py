# from generated import user_pb2, user_pb2_grpc

import grpc
from concurrent import futures
from users import user_pb2, user_pb2_grpc




class UserServiceServicer(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        # Implement your logic to get user information here
        user_id = request.user_id
        # Fetch user information from your data source
        user_info = {
            "user_id": user_id,
            "name": "John Doe",
            "email": "john.doe@example.com"
        }
        return user_pb2.UserResponse(**user_info)  # type: ignore



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started, listening on " + '[::]:50051')
    server.wait_for_termination()



if __name__ == "__main__":
    serve()