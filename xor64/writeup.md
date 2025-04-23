# XOR-64 Challenge Write-Up

## 🔐 Problem Summary

- Ciphertext: Base64-encoded XOR-encrypted text (`secret.txt`)
- Known plaintext: "Once upon a time there was"
- Task: Recover the key and decrypt the full message to find the flag.

## 🔧 Strategy

- Base64-decode the ciphertext to get raw XOR'd bytes
- Encode known plaintext to UTF-8 bytes
- XOR the two to recover the key (repeated pattern identified)
- Use the key to decrypt the full message

## 🧪 Flag

_The flag has been redacted for academic integrity._

## 🛠️ Tools

- Python 3
- PyCryptodome (`strxor`)
- Docker container (`thierrysans/pycryptodome`)

## 📂 Key Files

- `crack.py`: Recovers the key using known plaintext
- `xor64.py`: Performs encryption/decryption with Base64 wrapper
- `key.txt`: Contains the redacted key used for decryption
- `decrypted.txt`: not provided here
