#!/bin/bash

# Build the Docker image
echo "Building Docker image..."
docker build -t langgraph-app .

# Stop and remove existing container if it exists
echo "Stopping existing container if running..."
docker stop free_code 2>/dev/null || true
docker rm free_code 2>/dev/null || true

# Run the container with volume mounting for hot reload
echo "Starting container with hot reload..."
docker run -d \
  --name free_code \
  -v "$(pwd):/app" \
  -w /app \
  langgraph-app

echo "Container 'free_code' is running!"
echo "To access the container, run: docker exec -it free_code bash"
echo "Then you can run: python graph.py"
echo ""
echo "Your code changes will be reflected immediately in the container."
