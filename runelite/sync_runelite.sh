#!/bin/bash

TAG="runelite-parent-1.10.37"
REPO_URL="git@github.com:runelite/runelite.git"
TEMP_DIR="temp-runelite"

git -C . clean -ndx -e .idea
read -p "The above will be deleted and synced back from runelite's git repo. Proceed? (y/n)" confirm

if [ "$confirm" = "y" ]; then
    echo "Deleting files"
    git -C . clean -fdx -e .idea
else
    echo "Clean operation cancelled"
    exit 0
fi

mkdir -p $TEMP_DIR

git clone --depth 1 --branch $TAG $REPO_URL $TEMP_DIR

rsync -av --exclude='.git' $TEMP_DIR/ .

rm -rf $TEMP_DIR

echo "Sync complete. Runelite version $TAG has been copied to current directory."
