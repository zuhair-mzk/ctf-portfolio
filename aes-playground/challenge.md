# AES Playground CTF Challenge

In this challenge, we explore the behavior of AES encryption in different modes of operation by encrypting and decrypting `.ppm` image files.

We examine:

- AES-ECB: reveals patterns in plaintext
- AES-CBC: more secure, randomizes blocks with IV
- AES-CTR: acts like a stream cipher, but vulnerable if nonce/key is reused

We are provided:

- A plaintext image `example.ppm`
- Key file `key.txt`
- Pre-encrypted example images in each mode
- Two encrypted files: `secret1.ppm`, `secret2.ppm` (CTR mode, same key+nonce)
