#!/bin/bash

# Usage: bash run.sh encrypt 4 plaintext.txt
#        bash run.sh decrypt 4 ciphertext.txt

MODE=$1
KEY=$2
FILE=$3

if [ -z "$MODE" ] || [ -z "$KEY" ] || [ -z "$FILE" ]; then
  echo "Usage: bash run.sh [encrypt|decrypt] [key] [input_file]"
  exit 1
fi

docker run --rm -v "$(pwd)":/shared python:3 bash -c "python3 /shared/caesar26.py --$MODE --key $KEY /shared/$FILE"
