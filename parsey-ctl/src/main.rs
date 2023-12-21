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

    let pdf_bytes = read("table.pdf")?;

    let request = Request::new(BinaryRequest {
        pdf_bytes,
    });

    let response = client.process_text(request).await?.into_inner();

    let json_value: serde_json::Value = serde_json::from_str(&response.processed_content)?;

    println!("Received from 'parsey' via OpenAI:\n\n");
    println!("{}", serde_json::to_string_pretty(&json_value).unwrap());

    Ok(())
}
