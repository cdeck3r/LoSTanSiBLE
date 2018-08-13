#!/bin/sh

#
# runs the LoSTanSible Docker image
#
# Author: Christian Decker (cdeck3r)
#

#
# Note that under Windows not every directory can be used as shared folder.
# The host directory specified in `-v <host dir>:<container dir>`
# must be a subdir of `C:\Users\<username>\`.
#

HOST_DIR=$(pwd -P)/LoSTanSible

#################################################
# Do not edit below
#################################################

# takes the first command line argument
RUNMODE=$1

# need to check for invalid params
PARAMFAIL=1

#
# Help text, usage
#
usage ()
{
  echo "Usage : $0 [bash|jupyter]"
  exit
}

if [ -z $RUNMODE ]
then
    echo "Too few arguments."
    usage
    exit 1
fi

# jupyter
if [ "$RUNMODE" = "jupyter" ]
then
docker run -it --rm \
    -p 8888:8888 -p 6006:6006 \
    -v $HOST_DIR:/host \
    lostansible:latest \
    jupyter notebook --allow-root /host
PARAMFAIL=0
fi

if [ "$RUNMODE" = "bash" ]
then
docker run -it --rm \
    -p 8888:8888 -p 6006:6006 \
    -v $HOST_DIR:/host \
    lostansible:latest
PARAMFAIL=0
fi

if [ $PARAMFAIL -ne 0 ]
then
    echo "No valid arguments."
    usage
    exit 1
fi
