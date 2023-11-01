# Install docker on amazon linux 2

sudo yum update
sudo yum search docker
sudo yum install docker

sudo usermod -a -G docker ec2-user
id ec2-user
# Reload a Linux user's group assignments to docker w/o logout
newgrp docker

# Install docker compose
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-linux-x86_64 \
 -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose

# Enable docker service
sudo systemctl enable docker.service
sudo systemctl start docker.service

# Install git
sudo yum install git
docker-compose.staging.yml