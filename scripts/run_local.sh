#!/bin/bash

# Check if the script path is provided
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <path_to_pyflink_script>"
  exit 1
fi

# Set the path to your PyFlink script
PYFLINK_SCRIPT="$1"

# Set the Flink home directory
FLINK_HOME=/home/mjg/flink_infra/flink-1.18.0

# Set the Flink home directory
APP_CORE=/home/mjg/dev/pyflink-playground/core.zip

# Submit the PyFlink job to the local cluster
$FLINK_HOME/bin/flink run --python $PYFLINK_SCRIPT --pyFiles $APP_CORE
