#!/bin/bash

# Discord Bot Backup Script
# Creates backups of exported files and logs

set -e

# Configuration
BACKUP_DIR="backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="discord_bot_backup_${TIMESTAMP}"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[BACKUP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Create backup directory
mkdir -p "${BACKUP_DIR}"

print_status "Starting backup process..."

# Create backup archive
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"

print_status "Creating backup archive: ${BACKUP_PATH}"

# Create tar archive with exported files, logs, and config
tar -czf "${BACKUP_PATH}" \
    --exclude="backups" \
    --exclude=".git" \
    --exclude="__pycache__" \
    --exclude="*.pyc" \
    exports/ \
    logs/ \
    .env 2>/dev/null || true

print_success "Backup created: ${BACKUP_PATH}"

# Get backup size
BACKUP_SIZE=$(du -h "${BACKUP_PATH}" | cut -f1)
print_status "Backup size: ${BACKUP_SIZE}"

# Cleanup old backups (keep last 7)
print_status "Cleaning up old backups (keeping last 7)..."
cd "${BACKUP_DIR}"
ls -t discord_bot_backup_*.tar.gz 2>/dev/null | tail -n +8 | xargs rm -f

print_success "Backup process completed!"
print_status "Backup location: $(pwd)/${BACKUP_NAME}.tar.gz"