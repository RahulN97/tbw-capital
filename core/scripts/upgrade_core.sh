#!/bin/bash

INITIAL_DIR=$PWD
PARENT_DIR=$(basename "$PWD")
if [ "$PARENT_DIR" != "core" ]; then
    echo "Must run the upgrade from within core/, but outside scripts/"
    exit 0
fi

echo "Building core"
poetry install

echo "Installing core into Trade Data Platform"
cd ../tdp && poetry remove core
poetry add ../core

echo "Installing core into Autotrader"
cd ../autotrader && poetry remove core
poetry add ../core

cd $INITIAL_DIR
