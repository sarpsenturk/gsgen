#!/bin/bash

set -e

CKPT="$1"

if [ -z "$CKPT" ]; then
  echo "Usage: ./export.sh \"<checkpoint>\""
  exit 1
fi

echo "Export checkpoint $CKPT as .ply file"

python -m utils.export $CKPT --type ply
