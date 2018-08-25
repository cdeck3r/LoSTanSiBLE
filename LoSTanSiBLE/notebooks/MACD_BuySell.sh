#!/bin/bash

#
# Runs a Jupyter notebook using parameters
#
# Author: Christian Decker (cdeck3r)
#

SCRIPT_DIR=$(dirname $(readlink -f $0))

####################################################
# Important parameters to be set
####################################################

# we need the notebook to run as first parameter
INPUT_IPYNB="${SCRIPT_DIR}/MACD_BuySell.ipynb"
# we need the base name of the output notebook
OUTPUT_IPYNB="MACD_BuySell"

P1="${SCRIPT_DIR}/../data/external/data.csv"
P2="${SCRIPT_DIR}/../data/interim"
# parameters for MACD
P3=30
P4=26
P5=9
# other params
P6=

# the input notebook file must exist
if [ ! -e "${INPUT_IPYNB}" ]
  then
    echo "Notebook does not exists."
    exit 1
fi

####################################################
# install papermill
####################################################
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# We run the notebook install_papermill.ipynb
# it will install papermill into the system
jupyter nbconvert --to notebook --execute "${SCRIPT_DIR}/install_papermill.ipynb"

####################################################
# Run notebook using papermill
####################################################

for fast in {1..5}
do
    for slow in {1..5}
    do
        for signal in {1..5}
        do
            echo fast_window: $fast, slow_window: $slow, signal_window: $signal
            papermill ${INPUT_IPYNB} \
                $P2/${OUTPUT_IPYNB}_${fast}_${slow}_${signal}.ipynb \
                -p nb_file $INPUT_IPYNB \
                -p input_data_file $P1 \
                -p output_data_path $P2 \
                -p fast_window $fast \
                -p slow_window $slow \
                -p signal_window $signal
        done
    done
done
