# from generated import user_pb2, user_pb2_grpc

import grpc
from concurrent import futures
from users import user_pb2, user_pb2_grpc
from agents import agent_pb2, agent_pb2_grpc # type: ignore[attr-defined]




class UserServiceServicer(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
       
        user_id = request.user_id
        # Fetch user information from the data source
        user_info = {
            "user_id": user_id,
            "name": "John Doe",
            "email": "john.doe@example.com"
        }
        return user_pb2.UserResponse(**user_info)  # type: ignore[attr-defined]


class AgentServiceServicer(agent_pb2_grpc.AgentServiceServicer):
    def RunQuery(self, request, context):
        # Implement agent logic
        query = request.query
        # Call the agent (from main.py or refactored agent code)
        response_text = "Agent response for: " + query  # Replace with real agent call
        return agent_pb2.AgentQueryResponse(response=response_text)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)
    agent_pb2_grpc.add_AgentServiceServicer_to_server(AgentServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started, listening on " + '[::]:50051')
    server.wait_for_termination()



if __name__ == "__main__":
    serve()