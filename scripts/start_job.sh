#!/bin/bash

# Run bump-my-version to automatically increment the version
bump-my-version bump -v patch

# Extract the current version from the configuration file
CURRENT_VERSION=$(grep "current_version" pyproject.toml | sed -E 's/.*=//')

# Set address of the Docker image
ADDRESS=ghcr.io/mjgolebiewski/wymiana-mysli/flink-wiosenna

# Build and push Docker image
docker build . -t $ADDRESS:$CURRENT_VERSION
docker push $ADDRESS:$CURRENT_VERSION

# Uncomment the line in kustomization.yaml
sed -i 's/^#  - pyflink-job.yaml/  - pyflink-job.yaml/' flinkjobs/kustomization.yaml

# Commit and push changes to Git
git add .
git commit -m "job started using version: $CURRENT_VERSION"
git push wiosenna dev

echo "Job started using version: $CURRENT_VERSION."
