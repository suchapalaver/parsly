IMAGE_NAME = parsly-image

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -it -p 50051:50051 --env-file .env $(IMAGE_NAME)

clean:
	docker stop $$(docker ps -aq --filter ancestor=$(IMAGE_NAME)) || true
	docker rm $$(docker ps -aq --filter ancestor=$(IMAGE_NAME)) || true
	docker rmi $(IMAGE_NAME) || true

.PHONY: build run clean
