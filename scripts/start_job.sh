#!/bin/bash

# Extract the current version from the configuration file and trim the quotes
CURRENT_VERSION=$(grep "current_version" pyproject.toml | sed -n 's/.*= *"\([^"]*\).*/\1/p')

# Commit and push changes to Git
git add .
git commit -m "Job started using version: $CURRENT_VERSION"
git push wiosenna dev

echo "Job started using version: $CURRENT_VERSION"
echo "Current Job on Flink UI available at: https://flink.n4next.eu/#/job/running"
