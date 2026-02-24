#!/bin/bash
#
# Deployment script for RSS CAP Alert System
# This script is executed on the production VM by GitHub Actions
#
# Usage: ./deploy.sh
#

set -e  # Exit on error
set -u  # Exit on undefined variable

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running in correct directory
if [ ! -f "docker-compose.prod.yml" ]; then
    log_error "docker-compose.prod.yml not found. Are you in the correct directory?"
    exit 1
fi

log_info "Starting deployment process..."

# Export GITHUB_REPO_OWNER for docker-compose
export GITHUB_REPO_OWNER=${GITHUB_REPO_OWNER:-local}
log_info "Using GITHUB_REPO_OWNER: $GITHUB_REPO_OWNER"

# Pull latest code
log_info "Pulling latest code from git..."
git fetch origin
git checkout main
git pull origin main

# Pull latest Docker images
log_info "Pulling latest Docker images..."
docker compose -f docker-compose.prod.yml pull || {
    log_error "Failed to pull Docker images"
    exit 1
}

# Stop existing containers gracefully
log_info "Stopping existing containers..."
docker compose -f docker-compose.prod.yml stop || log_warn "No containers to stop"

# Start new containers
log_info "Starting updated containers..."
docker compose -f docker-compose.prod.yml up -d rss-api rss-client postgres cap-generator --remove-orphans

# Wait for services to be ready
log_info "Waiting for services to start (10 seconds)..."
sleep 10

# Check container status
log_info "Checking container status..."
docker compose -f docker-compose.prod.yml ps

# Health check for API
log_info "Performing health check on API..."
MAX_RETRIES=5
RETRY_COUNT=0
API_HEALTHY=false

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -f http://localhost:5000/ > /dev/null 2>&1; then
        API_HEALTHY=true
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    log_warn "API health check failed, retry $RETRY_COUNT/$MAX_RETRIES..."
    sleep 5
done

if [ "$API_HEALTHY" = true ]; then
    log_info "API health check passed!"
else
    log_error "API health check failed after $MAX_RETRIES attempts"
    log_error "Deployment may have failed. Check logs with: docker compose -f docker-compose.prod.yml logs"
    exit 1
fi

# Cleanup old images
log_info "Cleaning up old Docker images..."
docker image prune -f

log_info "Deployment completed successfully!"
log_info "You can view logs with: docker compose -f docker-compose.prod.yml logs -f"
