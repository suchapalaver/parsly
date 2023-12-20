pub mod message {
    tonic::include_proto!("message");
}

use tonic::Request;
use message::message_service_client::MessageServiceClient;
use message::TextRequest;
use tonic::transport::Endpoint;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let endpoint = Endpoint::from_static("http://[::]:50051");
    
    let mut client = MessageServiceClient::connect(endpoint).await?;

    let request = Request::new(TextRequest {
        text_data: "Hello from Rust!".to_string(),
    });

    let response = client.process_text(request).await?.into_inner();

    println!("Processed Text: {}", response.processed_text);

    Ok(())
}
