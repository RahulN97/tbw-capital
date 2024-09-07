#!/bin/bash

echo "Starting Trade Data Platform"

set -a
source .env
set +a

cd src && poetry run -vvv python app.py
