#!/bin/bash

echo "Starting AutoTrader"

set -a
source .env
set +a

cd src && poetry run -vvv python main.py
