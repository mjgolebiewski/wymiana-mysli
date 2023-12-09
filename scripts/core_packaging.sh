#!/bin/bash

# Get the directory of the core_packaging.sh script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define paths
CORE_DIR="$SCRIPT_DIR/../core"
OUTPUT_FILE="$SCRIPT_DIR/../core.zip"

# Change to the parent directory of the core directory
cd "$SCRIPT_DIR/.." || exit 1

# Package the core code and dependencies into a ZIP file, preserving the directory structure
zip -r "$OUTPUT_FILE" "core"

# Change back to the original directory
cd "$SCRIPT_DIR/.." || exit 1
