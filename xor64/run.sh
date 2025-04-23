#!/bin/bash
docker run --rm -v "$(pwd)":/shared thierrysans/pycryptodome \
bash -c "python3 /shared/xor64.py --decrypt --key /shared/key.txt --output /shared/decrypted.txt /shared/secret.txt"

---

# README.md

# XOR Cipher - Base64 Challenge

A CTF challenge involving a repeating-key XOR cipher and Base64 encoding.

## 🔓 Objective
- Reverse a Base64-encoded XOR ciphertext using known plaintext
- Recover the repeating key and decrypt the full message

## 🔧 Tools Used
- Python 3 + PyCryptodome (`strxor`)
- Docker container (`thierrysans/pycryptodome`)

## 📁 Key Components
- `xor64.py`: Script for encryption and decryption
- `crack.py`: Script to recover the key
- `key.txt`: (Key redacted for integrity)
- `decrypted.txt`: (Flag redacted)
- `run.sh`: Docker-based runner for clean execution
- `writeup.md`: Full technical walkthrough (flag omitted)
