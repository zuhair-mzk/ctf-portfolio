# XOR-64 Challenge

This challenge demonstrates a simple XOR cipher combined with Base64 encoding.

The goal was to decrypt a secret message stored in `secret.txt`. We were told that the beginning of the message is known:

> "Once upon a time there was"

Using this, we performed a known-plaintext attack to recover the key used for encryption, and then used it to decrypt the full ciphertext.
