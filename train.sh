#!/bin/bash

set -e

PROMPT="$1"

if [ -z "$PROMPT" ]; then
  echo "Usage: ./train.sh \"Your text prompt here\""
  exit 1
fi

echo "Training model for prompt: $PROMPT"

python main.py --config-name=base prompt.prompt="$PROMPT"
