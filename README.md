# parsey

Parsey is a simple Python app using the OpenAI library for powerful natural
language processing capabilities. It comes with Docker support and a Makefile
for convenient development and deployment.

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

### Building and Running the Docker Container

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
docker run -p 50051:50051 --env-file .env parsey-image
```

#### Clean up:

```terminal
docker stop $$(docker ps -aq --filter ancestor=parsey-image) || true
docker rm $$(docker ps -aq --filter ancestor=parsey-image) || true
docker rmi parsey-image || true
```
