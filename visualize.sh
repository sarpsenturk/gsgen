#!/bin/bash

set -e

CKPT="$1"

if [ -z "$CKPT" ]; then
  echo "Usage: ./visualize.sh \"<checkpoint>\""
  exit 1
fi

echo "Starting visualization for $CKPT on port 8000..."

python vis.py $CKPT --port 8000

