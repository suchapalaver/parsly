import grpc
import message_pb2
import message_pb2_grpc
import os
import PyPDF2
from concurrent.futures import ThreadPoolExecutor  # Import ThreadPoolExecutor from concurrent.futures
from io import BytesIO
from llama_index import VectorStoreIndex, SimpleDirectoryReader

class Utils:
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

        documents = SimpleDirectoryReader("data").load_data()
        index = VectorStoreIndex.from_documents(documents)

        query_engine = index.as_query_engine()
        response = query_engine.query("""
                                      If you find tables in the PDF file, 
                                      please parse them and return the data as a JSON object. 
                                      Only return the JSON object as your response without writing anything else other than the JSON
                                      """
                                    )
        
        return message_pb2.TextResponse(processed_content=response.response)

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
