#!/bin/sh

#
# Builds modern-deep-learning-docker Docker image
# Dockerfile taken from:
# https://github.com/waleedka/modern-deep-learning-docker
#
# Author: Christian Decker (cdeck3r)
#

docker build -t lostansible:latest . -f Dockerfile

#
# remove dangling images if build failed
#
docker rmi -f $(docker images --quiet --filter "dangling=true")
