#!/bin/bash

VERSION=$(<"scripts/version")
TAG="runelite-parent-$VERSION"
REPO_URL="git@github.com:runelite/runelite.git"

git -C . clean -ndx -e .idea
read -p "The above will be deleted and synced back from runelite's git repo. Proceed? (y/n)" confirm

if [ "$confirm" = "y" ]; then
    echo "Deleting files"
    git -C . clean -fdx -e .idea
else
    echo "Clean operation cancelled"
    exit 0
fi

TEMP_DIR=$(mktemp -d)
git clone --depth 1 --branch $TAG $REPO_URL $TEMP_DIR

/usr/bin/python3 -m scripts.add_core_dependency \
  --version $VERSION \
  --parent $TEMP_DIR/pom.xml \
  --client $TEMP_DIR/runelite-client/pom.xml

rsync -av --exclude='.git' $TEMP_DIR/ .
rm -rf $TEMP_DIR

echo "Sync complete. Runelite version $TAG has been copied to current directory."
