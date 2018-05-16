#!/bin/bash

if [ $# != 6 ]; then
    echo Usage: "$0 install_dir gurobi_file_location gurobi_license_key boxer_username boxer_password boxer_models"
    exit 1
fi

install_dir=$1
gurobi_file=$2
gurobi_license_key=$3
boxer_username=$4
boxer_password=$5
boxer_models=$6

# Create install_dir if it doesn't exist
mkdir -p $install_dir

if [ ! -d "$install_dir" ]; then
    exit 1
fi

export ADP_HOME=$install_dir

source ./setenv-linux64.sh

# Install gurobi
./install-gurobi-linux.sh $gurobi_file $gurobi_license_key

# Install henry
./install-henry.sh

# Install boxer
./install-boxer-linux.sh $boxer_username $boxer_password $boxer_models
