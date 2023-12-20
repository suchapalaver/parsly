fn main() {
    tonic_build::configure()
        .build_server(true)
        .compile(
            &["message.proto"],
            &["proto/"],
        )
        .unwrap();
}
