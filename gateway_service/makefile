# Local Development Tasks

# Install dependencies locally
install:
	npm install

# Run the app locally using Node.js
run:
	npm start

# Run tests locally
test:
	npm test

# Clean up node_modules (remove and reinstall dependencies)
clean:
	rm -rf node_modules

# Deploy locally: install and run in one command
deploy:
	make install
	make run


# Docker-related Tasks

# Build the Docker image
docker-build:
	docker build -t $(DOCKER_IMAGE_NAME) .

# Run the Docker container
docker-run:
	docker run -p $(PORT):$(PORT) --name $(DOCKER_CONTAINER_NAME) $(DOCKER_IMAGE_NAME)

# Stop and remove the Docker container
docker-stop:
	docker stop $(DOCKER_CONTAINER_NAME)
	docker rm $(DOCKER_CONTAINER_NAME)

# Clean up Docker (remove container and image)
docker-clean:
	docker rmi $(DOCKER_IMAGE_NAME)
	docker stop $(DOCKER_CONTAINER_NAME)
	docker rm $(DOCKER_CONTAINER_NAME)

# Deploy with Docker: build and run the Docker container in one command
docker-deploy: docker-build docker-run
