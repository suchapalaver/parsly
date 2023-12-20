pub mod message {
    tonic::include_proto!("message");
}

use message::message_service_client::MessageServiceClient;
use message::TextRequest;
use pdf_extract::extract_text;
use tonic::{transport::Endpoint, Request};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let endpoint = Endpoint::from_static("http://[::]:50051");
    
    let mut client = MessageServiceClient::connect(endpoint).await?;

    let pdf_text = extract_text("file.pdf")?;

    println!("PDF Text: {}", pdf_text);
    println!();

    let request = Request::new(TextRequest {
        text_data: pdf_text,
    });

    let response = client.process_text(request).await?.into_inner();

    println!("'parsey' via OpenAI: {}", response.processed_text);
    println!();

    Ok(())
}
