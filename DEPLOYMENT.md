# Deployment Guide

This document describes how to set up and use the automated deployment system for the RSS CAP Alert System.

## Overview

The project uses GitHub Actions for continuous deployment. When code is pushed to the `main` branch:

1. Docker images are built and pushed to GitHub Container Registry (GHCR)
2. The deployment workflow SSHs into your production VM
3. The latest code and images are pulled
4. Containers are updated with zero downtime
5. Health checks verify the deployment

## Initial Setup

### 1. Enable GitHub Container Registry

GHCR is automatically available for your GitHub repository. Images will be stored at:
- `ghcr.io/YOUR_USERNAME/rss-api-prod:latest`
- `ghcr.io/YOUR_USERNAME/rss-db:latest`
- `ghcr.io/YOUR_USERNAME/rss-client-prod:latest`
- `ghcr.io/YOUR_USERNAME/cap-gen-prod:latest`

### 2. Configure GitHub Secrets

Navigate to your repository: **Settings → Secrets and variables → Actions → New repository secret**

Add the following secrets:

#### SSH Access Secrets
- `SSH_HOST`: Your VM's IP address or hostname (e.g., `192.168.1.100` or `server.example.com`)
- `SSH_USER`: Username for SSH access (e.g., `deploy` or your username)
- `SSH_PRIVATE_KEY`: Your SSH private key (see instructions below)
- `SSH_PORT`: (Optional) SSH port, defaults to 22

#### CAP API Environment Variables
- `DB_HOST`: Database hostname (usually `postgres`)
- `DB_USER`: PostgreSQL username (e.g., `rss`)
- `DB_PASSWORD`: PostgreSQL password
- `DB_NAME`: Database name (e.g., `rss`)
- `API_HOST`: API hostname for internal communication
- `API_USER`: API authentication username
- `API_PASSWORD`: API authentication password
- `CONFIG`: Configuration environment (e.g., `prod`)

#### CAP Generator Environment Variables
- `CAP_GEN_API_URL`: URL to the RSS API (e.g., `http://rss-api:5000`)
- `CAP_GEN_API_USER`: Username for API authentication
- `CAP_GEN_API_PASSWORD`: Password for API authentication
- `CAP_GEN_CLIENT_IP`: Client IP for seismic event listening
- `CAP_GEN_CLIENT_PORT`: Client port for seismic event listening

### 3. Generate SSH Key for Deployment

On your **local machine or CI/CD environment**:

```bash
# Generate a new SSH key pair (use a strong passphrase or leave empty for CI/CD)
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_deploy

# Copy the PUBLIC key to your VM
ssh-copy-id -i ~/.ssh/github_deploy.pub YOUR_USERNAME@YOUR_VM_IP

# Copy the PRIVATE key content for GitHub Secrets
cat ~/.ssh/github_deploy
```

Copy the entire output (including `-----BEGIN OPENSSH PRIVATE KEY-----` and `-----END OPENSSH PRIVATE KEY-----`) and paste it into the `SSH_PRIVATE_KEY` secret in GitHub.

### 4. Prepare Your Production VM

On your **production VM**:

```bash
# Clone the repository (if not already done)
cd ~
git clone https://github.com/YOUR_USERNAME/RSS.git
cd RSS

# Make the deployment script executable
chmod +x deploy.sh

# Set the GITHUB_REPO_OWNER environment variable
# Add this to your ~/.bashrc or ~/.zshrc
export GITHUB_REPO_OWNER="YOUR_GITHUB_USERNAME"

# Authenticate with GitHub Container Registry
echo "YOUR_GITHUB_PAT" | docker login ghcr.io -u YOUR_USERNAME --password-stdin
```

**Note:** You'll need a GitHub Personal Access Token (PAT) with `read:packages` permission. Create one at: **GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)**

### 5. Security Hardening (Recommended)

#### Create a Dedicated Deployment User

On your **production VM**:

```bash
# Create deployment user
sudo useradd -m -s /bin/bash deploy

# Add to docker group
sudo usermod -aG docker deploy

# Setup SSH directory
sudo mkdir -p /home/deploy/.ssh
sudo cp ~/.ssh/authorized_keys /home/deploy/.ssh/
sudo chown -R deploy:deploy /home/deploy/.ssh
sudo chmod 700 /home/deploy/.ssh
sudo chmod 600 /home/deploy/.ssh/authorized_keys

# Clone repository for deploy user
sudo su - deploy
cd ~
git clone https://github.com/YOUR_USERNAME/RSS.git
```

#### Configure SSH Security

Edit `/etc/ssh/sshd_config`:

```
# Disable password authentication
PasswordAuthentication no

# Only allow key-based authentication
PubkeyAuthentication yes

# Disable root login
PermitRootLogin no

# Allow specific user (optional)
AllowUsers deploy
```

Restart SSH:
```bash
sudo systemctl restart sshd
```

## Usage

### Automatic Deployment

Simply push to the `main` branch:

```bash
git push origin main
```

GitHub Actions will automatically:
1. Run tests (via existing build-and-test workflow)
2. Build Docker images
3. Deploy to production
4. Verify health checks

Monitor the deployment at: **GitHub → Actions tab**

### Manual Deployment

Trigger deployment manually:

1. Go to **GitHub → Actions → Deploy to Production**
2. Click **Run workflow**
3. Select the `main` branch
4. Click **Run workflow**

### Manual Deployment on VM

SSH into your VM and run:

```bash
cd ~/RSS
export GITHUB_REPO_OWNER="YOUR_GITHUB_USERNAME"
./deploy.sh
```

## Rollback Procedure

If a deployment fails, you can rollback to a previous version:

```bash
# On your VM
cd ~/RSS

# View available image tags
docker images | grep rss

# Update docker-compose.prod.yml to use specific SHA tag
# Example: ghcr.io/YOUR_USERNAME/rss-api-prod:abc123def

# Pull and deploy specific version
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d --no-build

# Or rollback git and rebuild
git checkout PREVIOUS_COMMIT_SHA
./deploy.sh
```

## Building Images Locally

To build images locally instead of using GHCR:

1. On your VM, edit `docker-compose.prod.yml`
2. Uncomment the `build` sections
3. Comment out the `image` lines with ghcr.io
4. Run:
   ```bash
   docker compose -f docker-compose.prod.yml build
   docker compose -f docker-compose.prod.yml up -d
   ```

## Troubleshooting

### Deployment Fails at SSH Step

- Verify `SSH_HOST`, `SSH_USER`, and `SSH_PRIVATE_KEY` secrets are correct
- Check SSH key has proper permissions on VM: `~/.ssh/authorized_keys` should be 600
- Test SSH manually: `ssh -i ~/.ssh/github_deploy USER@HOST`

### Images Not Pulling

- Verify GitHub Container Registry authentication on VM
- Check if images were built and pushed: **GitHub → Packages**
- Make sure `GITHUB_REPO_OWNER` environment variable is set correctly

### Health Check Fails

- Check API logs: `docker compose -f docker-compose.prod.yml logs rss-api`
- Verify database is running: `docker compose -f docker-compose.prod.yml ps postgres`
- Check `.env` files have correct credentials

### Database Connection Issues

- Ensure `DB_HOST` secret is set to `postgres` (the service name in docker-compose)
- Verify PostgreSQL container is healthy
- Check database credentials in secrets match `.env` file

### SSL Certificate Issues

- SSL certificates must be obtained separately using certbot
- Follow the existing process: `make ssl-certificate` and `make nginx-https`
- Certificates are persisted in `./certbot/conf/` volume

## Monitoring

### View Logs

```bash
# All services
docker compose -f docker-compose.prod.yml logs -f

# Specific service
docker compose -f docker-compose.prod.yml logs -f rss-api
docker compose -f docker-compose.prod.yml logs -f rss-client
docker compose -f docker-compose.prod.yml logs -f cap-generator
```

### Check Service Status

```bash
docker compose -f docker-compose.prod.yml ps
```

### Check Resource Usage

```bash
docker stats
```

## Additional Notes

- Database data persists in `./postgres-data` volume
- Database backups are stored in `./pg_backup` volume
- SSL certificates are stored in `./certbot/conf` volume
- The deployment uses a zero-downtime strategy: old containers are stopped only after new ones are started
- Images are tagged with both `latest` and the commit SHA for version tracking
