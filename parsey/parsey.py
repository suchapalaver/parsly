import grpc
import json
import message_pb2
import message_pb2_grpc
import PyPDF2
import time
from concurrent.futures import ThreadPoolExecutor  # Import ThreadPoolExecutor from concurrent.futures
from io import BytesIO
from openai import OpenAI

def show_json(obj):
    print(json.loads(obj.model_dump_json()))

def create_pdf_from_bytes(pdf_bytes):
    pdf_writer = PyPDF2.PdfWriter()
    buffer = BytesIO(pdf_bytes)
    pdf_reader = PyPDF2.PdfReader(buffer)
    for page_num in range(len(pdf_reader.pages)):
        pdf_writer.add_page(pdf_reader.pages[page_num])
    new_pdf_buffer = BytesIO()
    pdf_writer.write(new_pdf_buffer)
    new_pdf_buffer.seek(0)
    with open('file.pdf', 'wb') as new_pdf_file:
        new_pdf_file.write(new_pdf_buffer.read())

class MessageServiceServicer(message_pb2_grpc.MessageServiceServicer):
    def ProcessText(self, request, context):
        pdf_bytes = request.pdf_bytes
        create_pdf_from_bytes(pdf_bytes)

        client = OpenAI()
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
        PDF_FILE_PARSER = assistant.id
        print("ASSISTANT:")
        show_json(assistant)

        file = client.files.create(
            file=open("file.pdf", "rb"),
            purpose='assistants'
        )

        assistant = client.beta.assistants.update(
            PDF_FILE_PARSER,
            tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
            file_ids=[file.id],
        )
        print("UPDATED ASSISTANT WITH FILE:")
        show_json(assistant)

        thread = client.beta.threads.create()
        print("THREAD:")
        show_json(thread)

        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content="Please perform your task on this PDF file."
        )
        print("MESSAGE:")
        show_json(message)

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )
        show_json(run)

        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

        print("WAITING FOR RUN TO COMPLETE...")
        while run.status == "queued" or run.status == "in_progress":
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)
        print("RUN:")
        show_json(run)

        messages = client.beta.threads.messages.list(thread_id=thread.id)
        print("MESSAGES:")
        show_json(messages)

        response_text = []
        for msg in messages:
            content_value = msg.content[0].text.value
            response_text.append(content_value)
            break

        return message_pb2.TextResponse(processed_content=json.dumps(response_text))

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
