import grpc
import json
import message_pb2
import message_pb2_grpc
import os
import PyPDF2
import time
from concurrent.futures import ThreadPoolExecutor  # Import ThreadPoolExecutor from concurrent.futures
from io import BytesIO
from openai import OpenAI

class Utils:
    @staticmethod
    def show_json(obj):
        print(json.loads(obj.model_dump_json()))

    @staticmethod
    def create_pdf_from_bytes(pdf_bytes):
        pdf_writer = PyPDF2.PdfWriter()
        buffer = BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(buffer)

        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])
        
        new_pdf_buffer = BytesIO()
        pdf_writer.write(new_pdf_buffer)
        new_pdf_buffer.seek(0)

        data_folder = 'data'
        file_path = os.path.join(data_folder, 'file.pdf')

        os.makedirs(data_folder, exist_ok=True)

        with open(file_path, 'wb') as new_pdf_file:
            new_pdf_file.write(new_pdf_buffer.read())

class MessageServiceServicer(message_pb2_grpc.MessageServiceServicer):
    def ProcessText(self, request, context):
        pdf_bytes = request.pdf_bytes
        Utils.create_pdf_from_bytes(pdf_bytes)
        
        client = OpenAI()
        
        assistant = self.setup_openai_assistant(client)
        file = self.create_assistant_file(client)
        self.update_assistant_with_file(client, assistant, file)
        thread = self.create_assistant_thread(client)
        message = self.create_assistant_message(client, thread)
        run = self.create_assistant_run(client, thread, assistant)
        self.wait_for_run_completion(client, thread, run)
        response_text = self.get_assistant_response(client, thread)

        return message_pb2.TextResponse(processed_content=json.dumps(response_text))
    
    def setup_openai_assistant(self, client):
        assistant = client.beta.assistants.create(
            name="PDF Text Content Tabular Data Parser",
            instructions="""You specialize in parsing tabular data from pdf file content.
                            You produce a JSON object, similar to an abstract syntax tree, with the parsed results.
                            Read the PDF file. When you read it you are particularly attentive to data in tables 
                            and you ensure that the fields of tables and their data are represented in the JSON data structure that you produce, 
                            for example: `{ \"field\": \"value\" }`. 
                            When you extract the PDF data you parse to JSON, you will not save it as a JSON file but serialize the JSON to string and provide it as the only content of your response. 
                            You need to provide the entire JSON representation. 
                            It is extremely important that you only provide the entire JSON structure in your response. 
                            Do not add any comments or additional text to your response. 
                            Remember, you must return the JSON, do not save the extracted JSON content to a file.""",
            tools=[{"type": "retrieval"}],
            model="gpt-4-1106-preview"
        )
        
        print()
        print("ASSISTANT:")
        Utils.show_json(assistant)
        
        return assistant
    
    def create_assistant_file(self, client):
        file = client.files.create(
            file=open("./data/file.pdf", "rb"),
            purpose='assistants'
        )
        return file
    
    def update_assistant_with_file(self, client, assistant, file):
        assistant = client.beta.assistants.update(
            assistant.id,
            tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
            file_ids=[file.id],
        )
        
        print()
        print("UPDATED ASSISTANT WITH FILE:")
        Utils.show_json(assistant)

    def create_assistant_thread(self, client):
        thread = client.beta.threads.create()
        
        print()
        print("THREAD:")
        Utils.show_json(thread)
        
        return thread
    
    def create_assistant_message(self, client, thread):
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content="Please perform your task on this PDF file."
        )
        print()
        print("MESSAGE:")
        Utils.show_json(message)
        
        return message

    def create_assistant_run(self, client, thread, assistant):
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )
        return run
    
    def wait_for_run_completion(self, client, thread, run):
        print()
        print("WAITING FOR RUN TO COMPLETE...")
        while run.status == "queued" or run.status == "in_progress":
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)

    def get_assistant_response(self, client, thread):
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        
        print()
        print("MESSAGES:")
        Utils.show_json(messages)
        
        response_text = [msg.content[0].text.value for msg in messages if msg.content]
        return response_text[0] if response_text else None

def serve():
    print("Starting 'parsey' server. Listening on port 50051.")
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    message_pb2_grpc.add_MessageServiceServicer_to_server(
        MessageServiceServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
