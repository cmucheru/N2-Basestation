# Clean docker files
clean: stop remove-files

# This pull build and starts docker container
all: clean pull build start

# Pull docker images form dockerhub
pull:
	docker-compose pull

# Currenlty, it build our message broker, rabbitmq
build:
	docker-compose build

# Starts our docker containers
start:
	docker-compose up -d

# Stops our docker containers
stop:
	docker-compose down

# Remove files
remove-files:
	docker system prune -a
	docker volume prune

# Watch logs of the deployment
logs:
	watch docker-compose logs


