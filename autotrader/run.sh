echo "Running locally. Sourcing env vars"
set -a
source .env
set +a

cd src && poetry run -vvv python main.py
