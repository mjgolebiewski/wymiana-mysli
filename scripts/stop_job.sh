#!/bin/bash

# Extract the current version from the configuration file and trim the quotes
CURRENT_VERSION=$(grep "current_version" pyproject.toml | sed -n 's/.*= *"\([^"]*\).*/\1/p')

# Comment out the line in kustomization.yaml
sed -i 's/  - pyflink-job.yaml/#  - pyflink-job.yaml/' flinkjobs/kustomization.yaml

# Commit and push changes to Git
git add .
git commit -m "job stop"
git push wiosenna dev

echo "Job using version: $CURRENT_VERSION stopped."
