import grpc
from concurrent import futures
import asyncio
from users import user_pb2, user_pb2_grpc
from agents_services import agent_pb2, agent_pb2_grpc  # type: ignore[attr-defined]
from agents_services.agent_runner import run_agent_query  # <-- import your agent logic

class UserServiceServicer(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        user_id = request.user_id
        user_info = {
            "user_id": user_id,
            "name": "John Doe",
            "email": "john.doe@example.com"
        }
        return user_pb2.UserResponse(**user_info)  # type: ignore[attr-defined]

class AgentServiceServicer(agent_pb2_grpc.AgentServiceServicer):
    def RunQuery(self, request, context):
        query = request.query
        # Run the agent asynchronously and wait for result
        response_text = asyncio.run(run_agent_query(query))
        return agent_pb2.AgentQueryResponse(response=response_text) # type: ignore[attr-defined]


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)
    agent_pb2_grpc.add_AgentServiceServicer_to_server(AgentServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started, listening on [::]:50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()