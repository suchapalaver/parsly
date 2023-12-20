fn main() {
    tonic_build::configure()
        .build_server(true)
        .compile(
            &["message.proto"], // Add the path to your Protobuf file(s)
            &["proto/"], // Set the Protobuf includes directory
        )
        .unwrap();
}
