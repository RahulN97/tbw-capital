#!/bin/bash

TAG="runelite-parent-1.10.36.1"
REPO_URL="git@github.com:runelite/runelite.git"
TEMP_DIR="temp-runelite"

git clone --depth 1 --branch $TAG $REPO_URL $TEMP_DIR

rsync -av --exclude='.git' $TEMP_DIR/ .

rm -rf $TEMP_DIR

echo "Sync complete. Runelite version $TAG has been copied to current directory."
