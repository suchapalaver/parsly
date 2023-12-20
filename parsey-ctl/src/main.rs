pub mod message {
    tonic::include_proto!("message");
}

use message::message_service_client::MessageServiceClient;
use message::BinaryRequest;
use tonic::{transport::Endpoint, Request};

use std::fs::read;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let endpoint = Endpoint::from_static("http://[::]:50051");
    
    let mut client = MessageServiceClient::connect(endpoint).await?;

    let pdf_bytes = read("file.pdf")?;

    let request = Request::new(BinaryRequest {
        pdf_bytes,
    });

    let response = client.process_text(request).await?.into_inner();

    println!("'parsey' via OpenAI: {}", response.processed_content);
    println!();

    Ok(())
}
