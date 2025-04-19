# Caesar 26 – The Caesar Cipher

**Category:** Cryptography  
**Level:** Introductory  
**Tooling:** Python3, Command-line, Docker

Complete a Caesar cipher tool that encrypts and decrypts lowercase ASCII strings with a given right-shift key. The script supports both `--encrypt` and `--decrypt` modes, and accepts input from a file.

Flags are hidden in encrypted messages using this classical technique. Your job is to reverse the cipher and extract the flag using the correct key.

### Example Usage:

```bash
$ python3 caesar26.py --encrypt --key 4 plaintext.txt
$ python3 caesar26.py --decrypt --key 4 ciphertext.txt
```
