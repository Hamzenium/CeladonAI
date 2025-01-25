# Variables
APP_NAME := queue_service
CMD_DIR := ./cmd
MAIN_FILE := $(CMD_DIR)/main.go
BUILD_DIR := ./bin
OUTPUT_FILE := $(BUILD_DIR)/$(APP_NAME)

# Default target
all: build

# Build the application
build:
	@echo "Building the application..."
	@mkdir -p $(BUILD_DIR)
	go build -o $(OUTPUT_FILE) $(MAIN_FILE)

# Run the application
run: build
	@echo "Running the application..."
	@$(OUTPUT_FILE)

# Run tests
test:
	@echo "Running tests..."
	go test ./...

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	@rm -rf $(BUILD_DIR)

# Format the code
format:
	@echo "Formatting code..."
	go fmt ./...

# Lint the code
lint:
	@echo "Linting code..."
	go vet ./...

# Install dependencies
deps:
	@echo "Installing dependencies..."
	go mod tidy

# Help message
help:
	@echo "Makefile commands:"
	@echo "  make build    - Build the application"
	@echo "  make run      - Run the application"
	@echo "  make test     - Run tests"
	@echo "  make clean    - Clean build artifacts"
	@echo "  make format   - Format the code"
	@echo "  make lint     - Lint the code"
	@echo "  make deps     - Install dependencies"
