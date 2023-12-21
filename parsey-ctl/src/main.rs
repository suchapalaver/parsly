mod cli;
use crate::cli::cli;

pub mod message {
    tonic::include_proto!("message");
}

use message::message_service_client::MessageServiceClient;
use message::BinaryRequest;
use tonic::{transport::Endpoint, Request};

use std::fs::read;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let matches = cli().get_matches();

    let endpoint: Endpoint = format!("http://[::]:{}", matches.get_one::<String>("port").unwrap())
        .try_into()
        .expect("Invalid url");

    let mut client = MessageServiceClient::connect(endpoint).await?;

    let pdf_bytes = read(matches.get_one::<String>("file").unwrap())?;

    let request = Request::new(BinaryRequest { pdf_bytes });

    let response = client.process_text(request).await?.into_inner();

    let json_value: serde_json::Value = serde_json::from_str(&response.processed_content)?;

    println!();
    println!("Received from 'parsey' via OpenAI:");
    println!();
    println!("{}", serde_json::to_string_pretty(&json_value).unwrap());

    Ok(())
}
