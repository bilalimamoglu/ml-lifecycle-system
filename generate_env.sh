#!/bin/bash

# Detect Operating System
OS="$(uname)"
if [ "$OS" == "Linux" ]; then
    # Check if docker group exists
    if getent group docker > /dev/null 2>&1; then
        DOCKER_GID=$(getent group docker | cut -d: -f3)
    else
        echo "Docker group not found on the host. Please ensure Docker is installed and the 'docker' group exists."
        exit 1
    fi
elif [ "$OS" == "Darwin" ]; then
    # On macOS, Docker runs inside a VM, so set DOCKER_GID to 0 (root)
    DOCKER_GID=0
else
    echo "Unsupported OS: $OS"
    exit 1
fi

# Check if .env file exists
if [ -f .env ]; then
    # If .env exists, update the DOCKER_GID line or add it if not present
    if grep -q "^DOCKER_GID=" .env; then
        sed -i.bak "s/^DOCKER_GID=.*/DOCKER_GID=${DOCKER_GID}/" .env
        echo "Updated DOCKER_GID in existing .env file."
    else
        echo "DOCKER_GID=${DOCKER_GID}" >> .env
        echo "Added DOCKER_GID to existing .env file."
    fi
else
    # If .env doesn't exist, create it
    echo "DOCKER_GID=${DOCKER_GID}" > .env
    echo ".env file created with DOCKER_GID=${DOCKER_GID}"
fi
