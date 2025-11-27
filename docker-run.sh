#!/bin/bash

# Script to run the Flask app in Docker detached mode

echo "🐳 Building and starting Docker containers in detached mode..."

# Build and start all services in detached mode
docker-compose up -d --build

echo ""
echo "✅ Containers started in detached mode!"
echo ""
echo "📋 Container status:"
docker-compose ps

echo ""
echo "📱 Access the application at: http://localhost:5001"
echo "🗄️  MinIO Admin at: http://localhost:9001"
echo ""
echo "📊 View logs: docker-compose logs -f"
echo "🛑 Stop containers: docker-compose down"
echo "🔄 Restart containers: docker-compose restart"

