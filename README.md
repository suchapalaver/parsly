# parsey

Parsey is a simple Python application leveraging natural language processing
functionalities. With built-in Docker support and a Makefile for convenient
development and deployment, the focus of the project is to serve as a proof of
concept for deploying AI agents on orchestration infrastructure such as
Kubernetes, with the ability to receive data to the service and respond via
[gRPC](https://grpc.io/).

## Installation

### Clone the Repository:

```terminal
git clone https://github.com/your-username/parsey.git
cd parsey
```

### Set Up OpenAI API Key:

- Obtain an API key from OpenAI.
- Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Replace `your_openai_api_key_here` with your actual OpenAI API key.

## Getting Started

Follow these instructions to get a copy of the project up and running on your
local machine for development and testing purposes.

### Prerequisites

- Docker
- Make (optional, but recommended for using the Makefile)
- [Rust and Cargo](https://www.rust-lang.org/tools/install) (for running the `parsey-ctl` Rust client)

### Building and Running the Docker Container (`parsey` App)

#### Build the Docker image:

```terminal
make build
```

This command builds the Docker image for the Parsey app.

#### Run the Docker container:

```terminal
make run
```

This command starts the Docker container, and your Parsey app's gRPC service
will be accessible at [http://localhost:50051](http://localhost:50051).

If things work, you should see this in your terminal:

```terminal
Starting 'parsey' server. Listening on port 50051.
```

#### Clean up:

```terminal
make clean
```

Use this command to stop and remove running containers, and remove the
Docker image.

### Manual Docker Commands (without Makefile)

If you prefer not to use the Makefile, you can use the following manual
commands:

#### Build the Docker image:

```terminal
docker build -t parsey-image .
```

#### Run the Docker container:

```terminal
docker run -it -p 50051:50051 --env-file .env parsey-image
```

#### Clean up:

```terminal
docker stop $$(docker ps -aq --filter ancestor=parsey-image) || true
docker rm $$(docker ps -aq --filter ancestor=parsey-image) || true
docker rmi parsey-image || true
```

## Running the Rust Client (`parsey-ctl`)

### Navigate to parsey-ctl directory:

```bash
cd parsey-ctl
```

### See the CLI Help Menu

```bash
cargo run -- --help
```

### Build and Run the Rust Client:

```bash
cargo run
```

This command compiles and runs the `parsey-ctl` Rust client, sending a
request to the `parsey` app's gRPC service.

By default, `parsey-ctl` listens for the `parsey` gRPC service on port
`50051`, and uses data from the `table.pdf` test file.

Using the default `table.pdf` file, you should output like this:

```terminal
Received from 'parsey' via OpenAI:

{
  "table": [
    {
      "Ballots Completed": 1,
      "Ballots Incomplete/Terminated": 4,
      "Category": "Completed",
      "Disability": "Blind",
      "Participants": 5,
      "Results Accuracy": "34.5%, n=1",
      "Time to complete": "1199 sec, n=1"
    },
    {
      "Ballots Completed": 2,
      "Ballots Incomplete/Terminated": 3,
      "Category": "Completed",
      "Disability": "Low Vision",
      "Participants": 5,
      "Results Accuracy": "98.3% n=2 (97.7%, n=3)",
      "Time to complete": "1716 sec, n=3 (1934 sec, n=2)"
    },
    {
      "Ballots Completed": 4,
      "Ballots Incomplete/Terminated": 1,
      "Category": "Completed",
      "Disability": "Dexterity",
      "Participants": 5,
      "Results Accuracy": "98.3%, n=4",
      "Time to complete": "1672.1 sec, n=4"
    },
    {
      "Ballots Completed": 3,
      "Ballots Incomplete/Terminated": 0,
      "Category": "Completed",
      "Disability": "Mobility",
      "Participants": 3,
      "Results Accuracy": "95.4%, n=3",
      "Time to complete": "1416 sec, n=3"
    }
  ]
}

```
