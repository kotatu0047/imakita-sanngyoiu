#!/bin/bash

# Discord Bot Maintenance Script
# Performs routine maintenance tasks

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[MAINTENANCE]${NC} $1"
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

# Function to check disk space
check_disk_space() {
    print_status "Checking disk space..."

    DISK_USAGE=$(df -h . | awk 'NR==2 {print $5}' | sed 's/%//')

    if [ "$DISK_USAGE" -gt 90 ]; then
        print_error "Disk usage is ${DISK_USAGE}% - Critical!"
        return 1
    elif [ "$DISK_USAGE" -gt 80 ]; then
        print_warning "Disk usage is ${DISK_USAGE}% - High"
    else
        print_success "Disk usage is ${DISK_USAGE}% - OK"
    fi
}

# Function to clean up old logs
cleanup_logs() {
    print_status "Cleaning up old logs..."

    if [ -d "logs" ]; then
        # Keep logs from last 30 days
        find logs/ -name "*.log" -type f -mtime +30 -delete 2>/dev/null || true
        print_success "Old logs cleaned up"
    else
        print_status "No logs directory found"
    fi
}

# Function to clean up old exports
cleanup_exports() {
    print_status "Cleaning up old exports..."

    if [ -d "exports" ]; then
        # Count files older than 7 days
        OLD_FILES=$(find exports/ -name "*.txt" -type f -mtime +7 | wc -l)

        if [ "$OLD_FILES" -gt 0 ]; then
            print_status "Found $OLD_FILES export files older than 7 days"
            find exports/ -name "*.txt" -type f -mtime +7 -delete
            print_success "Old export files cleaned up"
        else
            print_status "No old export files to clean up"
        fi
    else
        print_status "No exports directory found"
    fi
}

# Function to check container health
check_container_health() {
    print_status "Checking container health..."

    if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
        print_success "Bot container is running"

        # Check container resources
        CONTAINER_NAME=$(docker-compose -f docker-compose.prod.yml ps --services)
        if [ ! -z "$CONTAINER_NAME" ]; then
            MEMORY_USAGE=$(docker stats --no-stream --format "table {{.MemUsage}}" "$CONTAINER_NAME" 2>/dev/null | tail -n +2 | head -n 1)
            if [ ! -z "$MEMORY_USAGE" ]; then
                print_status "Container memory usage: $MEMORY_USAGE"
            fi
        fi
    else
        print_error "Bot container is not running!"
        return 1
    fi
}

# Function to clean Docker system
cleanup_docker() {
    print_status "Cleaning up Docker system..."

    # Remove unused Docker images, containers, and networks
    docker system prune -f > /dev/null 2>&1 || true

    print_success "Docker system cleaned up"
}

# Function to backup important files
create_backup() {
    print_status "Creating backup..."

    if [ -f "scripts/backup.sh" ]; then
        chmod +x scripts/backup.sh
        ./scripts/backup.sh
    else
        print_warning "Backup script not found, skipping backup"
    fi
}

# Main maintenance function
main() {
    print_status "Starting maintenance routine..."
    echo "======================================"

    # Run maintenance tasks
    check_disk_space
    echo "--------------------"

    cleanup_logs
    echo "--------------------"

    cleanup_exports
    echo "--------------------"

    check_container_health
    echo "--------------------"

    cleanup_docker
    echo "--------------------"

    create_backup
    echo "======================================"

    print_success "Maintenance routine completed!"
}

# Run maintenance
main