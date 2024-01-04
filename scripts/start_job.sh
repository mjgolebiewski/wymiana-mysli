#!/bin/bash

# Check if script path is provided
if [ -z "$1" ]; then
    echo "Error: Please provide the script path as an argument."
    exit 1
fi

# Run bump-my-version to automatically increment the version
bump-my-version bump -v patch --allow-dirty

# Extract the current version from the configuration file and trim the quotes
CURRENT_VERSION=$(grep "current_version" pyproject.toml | sed -n 's/.*= *"\([^"]*\).*/\1/p')

# Set address of the Docker image
ADDRESS=ghcr.io/mjgolebiewski/wymiana-mysli/flink-wiosenna

# Build and push Docker image, passing script path as a build argument
docker build -t "$ADDRESS:$CURRENT_VERSION" --build-arg SCRIPT_PATH="$1" .
docker push "$ADDRESS:$CURRENT_VERSION"

# Uncomment the line in kustomization.yaml
sed -i 's/^#  - pyflink-job.yaml/  - pyflink-job.yaml/' flinkjobs/kustomization.yaml

# Commit and push changes to Git
git add .
git commit -m "Job started using version: $CURRENT_VERSION"
git push origin dev

echo "Job started using version: $CURRENT_VERSION."
echo "Flink UI available: https://flink.n4next.eu/"
