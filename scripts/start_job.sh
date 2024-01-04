#!/bin/bash

# Extract the current version from the configuration file
CURRENT_VERSION=$(grep "current_version" pyproject.toml | sed -E 's/.*=//')

# Run bump-my-version to automatically increment the version
bump-my-version bump --current-version "$CURRENT_VERSION"

# Get the latest version from the pyproject.toml file
CONTAINER_VERSION=$(grep "version" pyproject.toml | sed -E 's/.*=//')

# # Build and push Docker image
# docker build . -t ghcr.io/mjgolebiewski/wymiana-mysli/flink-wiosenna:$CONTAINER_VERSION
# docker push ghcr.io/mjgolebiewski/wymiana-mysli/flink-wiosenna:$CONTAINER_VERSION

# # Commit and push changes to Git
# git add .
# git commit -m "job start on version: $CONTAINER_VERSION"
# git push wiosenna dev

echo Container version: $CONTAINER_VERSION
