#!/bin/bash

# Discord Bot VPS Deployment Script
set -e

echo "🚀 Starting Discord Bot deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env file exists
if [ ! -f .env ]; then
    print_error ".env file not found!"
    print_status "Creating .env template..."
    cp .env.example .env
    print_warning "Please edit .env file with your Discord bot token and configuration"
    print_status "Then run this script again"
    exit 1
fi

# Create necessary directories
print_status "Creating directories..."
mkdir -p exports logs

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed!"
    print_status "Installing Docker..."

    # Update package index
    sudo apt update

    # Install dependencies
    sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

    # Add Docker GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

    # Add Docker repository
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

    # Install Docker
    sudo apt update
    sudo apt install -y docker-ce

    # Add current user to docker group
    sudo usermod -aG docker $USER

    print_success "Docker installed successfully!"
    print_warning "Please log out and log back in for Docker group membership to take effect"
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed!"
    print_status "Installing Docker Compose..."

    # Download Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

    # Make it executable
    sudo chmod +x /usr/local/bin/docker-compose

    print_success "Docker Compose installed successfully!"
fi

# Stop existing containers
print_status "Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down 2>/dev/null || true

# Build and start the bot
print_status "Building Docker image..."
docker-compose -f docker-compose.prod.yml build

print_status "Starting Discord bot..."
docker-compose -f docker-compose.prod.yml up -d

# Wait a moment for the container to start
sleep 5

# Check if container is running
if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    print_success "Discord bot is now running!"
    print_status "Container status:"
    docker-compose -f docker-compose.prod.yml ps

    print_status "To view logs: docker-compose -f docker-compose.prod.yml logs -f"
    print_status "To stop: docker-compose -f docker-compose.prod.yml down"
    print_status "Exported files will be saved to: $(pwd)/exports/"
else
    print_error "Failed to start Discord bot!"
    print_status "Check logs: docker-compose -f docker-compose.prod.yml logs"
    exit 1
fi

print_success "Deployment completed successfully! 🎉"