#!/bin/bash

NB=$1

####################################################
# helper functions
####################################################
usage()
{
    echo "Usage: $0 <path-to-jupyter-notebook>"
    echo "Note: The output file is written where the input notebook originates from."
    echo ""
}

if [ -z ${NB} ] ; then
    echo "Too few parameters."
    usage
    exit 1
fi

jupyter nbconvert --to python --template=nb2py.tpl ${NB}
