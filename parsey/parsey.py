import grpc
import message_pb2
import message_pb2_grpc
from concurrent.futures import ThreadPoolExecutor  # Import ThreadPoolExecutor from concurrent.futures
from openai import OpenAI

class MessageServiceServicer(message_pb2_grpc.MessageServiceServicer):
    def ProcessText(self, request, context):
        text_data = request.text_data
        client = OpenAI()
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Say this is a test"}],
            stream=True,
        )
        for chunk in stream:
            print(chunk.choices[0].delta.content or "", end="")

def serve():
    print("Starting server. Listening on port 50051.")
    server = grpc.server(ThreadPoolExecutor(max_workers=10))  # Use ThreadPoolExecutor from concurrent.futures
    message_pb2_grpc.add_MessageServiceServicer_to_server(
        MessageServiceServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
