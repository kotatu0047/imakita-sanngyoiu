#!/bin/bash

# Discord Bot Update Script
# Updates the bot with latest code changes

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[UPDATE]${NC} $1"
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

# Function to check if git repo
check_git_repo() {
    if [ ! -d ".git" ]; then
        print_error "Not a git repository! Cannot update via git."
        print_status "Please manually upload your updated files to the VPS."
        exit 1
    fi
}

# Function to backup current state
backup_current_state() {
    print_status "Creating backup before update..."

    if [ -f "scripts/backup.sh" ]; then
        ./scripts/backup.sh
    else
        print_warning "Backup script not found, continuing without backup"
    fi
}

# Function to update code
update_code() {
    print_status "Updating code from repository..."

    # Stash any local changes
    git stash push -m "Auto-stash before update $(date)" 2>/dev/null || true

    # Pull latest changes
    git pull origin main || git pull origin master || {
        print_error "Failed to pull updates from repository"
        exit 1
    }

    print_success "Code updated successfully"
}

# Function to rebuild and restart bot
restart_bot() {
    print_status "Rebuilding and restarting bot..."

    # Stop current containers
    docker-compose -f docker-compose.prod.yml down

    # Rebuild images
    docker-compose -f docker-compose.prod.yml build

    # Start containers
    docker-compose -f docker-compose.prod.yml up -d

    # Wait for container to start
    sleep 5

    # Check if container is running
    if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
        print_success "Bot restarted successfully"
    else
        print_error "Failed to start bot after update"
        print_status "Check logs: docker-compose -f docker-compose.prod.yml logs"
        exit 1
    fi
}

# Function to verify bot health
verify_bot_health() {
    print_status "Verifying bot health..."

    # Wait a bit more for bot to fully initialize
    sleep 10

    # Check logs for any errors
    LOGS=$(docker-compose -f docker-compose.prod.yml logs --tail 20 2>&1)

    if echo "$LOGS" | grep -qi "error\|exception\|failed"; then
        print_warning "Potential issues detected in logs:"
        echo "$LOGS"
    else
        print_success "Bot appears to be running healthy"
    fi
}

# Main update function
main() {
    print_status "Starting bot update process..."
    echo "======================================"

    # Check prerequisites
    check_git_repo
    echo "--------------------"

    # Backup current state
    backup_current_state
    echo "--------------------"

    # Update code
    update_code
    echo "--------------------"

    # Restart bot
    restart_bot
    echo "--------------------"

    # Verify health
    verify_bot_health
    echo "======================================"

    print_success "Bot update completed successfully!"
    print_status "Monitor logs: docker-compose -f docker-compose.prod.yml logs -f"
}

# Check if running as root (not recommended)
if [ "$EUID" -eq 0 ]; then
    print_warning "Running as root is not recommended for security reasons"
fi

# Run update
main