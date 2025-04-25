# 🔐 AES Playground – CTF Writeup

## 🧠 Challenge Goal

This challenge explores the strengths and weaknesses of various AES block cipher modes by encrypting `.ppm` image files. We experiment with:

- **Electronic Codebook (ECB)** – insecure due to identical block output
- **Cipher Block Chaining (CBC)** – adds randomized chaining with an IV
- **Counter (CTR)** – behaves like a stream cipher; secure if nonce is unique

We also exploit a serious vulnerability: **reusing the same key and nonce in CTR mode**.

---

## 🗂️ File Summary

| File          | Purpose                                                          |
| ------------- | ---------------------------------------------------------------- |
| `aes.py`      | Encrypts/decrypts images using AES-ECB, CBC, or CTR _(redacted)_ |
| `crack.py`    | Performs XOR-based attack on reused CTR ciphertexts _(redacted)_ |
| `key.txt`     | 128-bit AES key (starter file)                                   |
| `example.ppm` | Clean plaintext image used to show ECB leakage                   |
| `secret1.ppm` | AES-CTR encrypted image #1 (challenge input)                     |
| `secret2.ppm` | AES-CTR encrypted image #2 (same key+nonce)                      |
| `output.ppm`  | XOR result of secret1 and secret2 (reveals the flag)             |
| `enc-*.ppm`   | Encrypted output using various AES modes                         |
| `dec-*.ppm`   | Decrypted image files                                            |
| `run.sh`      | Helper script for Docker-based execution                         |

---

## 💥 The Vulnerability

CTR mode encrypts data by generating a pseudorandom keystream `K` and XORing it with the plaintext:

```
C = P ⊕ K
```

If the **same key and nonce** are reused, the same keystream `K` is used. So for two ciphertexts:

```
C1 = P1 ⊕ K
C2 = P2 ⊕ K
```

Then:

```
C1 ⊕ C2 = (P1 ⊕ K) ⊕ (P2 ⊕ K) = P1 ⊕ P2
```

This means we don’t need the key at all — we can recover the XOR of the original plaintexts!

---

## 🧨 Exploit Summary

We XOR `secret1.ppm` and `secret2.ppm` using `crack.py`, generating a new image `output.ppm` that visually reveals the flag "rijndael" due to differences between the original plaintexts.

This attack works **without knowing the key** or decrypting either image individually.

---

## 🔧 Terminal Commands Used

All commands are executed via Docker using the `thierrysans/pycryptodome` image:

### 🔍 Crack XOR of reused CTR ciphertexts:

```bash
docker run --rm -v "$(pwd)":/shared thierrysans/pycryptodome bash -c \
"python3 /shared/crack.py -o /shared/data/flag/output.ppm /shared/data/flag/secret1.ppm /shared/data/flag/secret2.ppm"
```

### 🔐 Encrypt an image with AES (e.g., ECB mode):

```bash
docker run --rm -v "$(pwd)":/shared thierrysans/pycryptodome bash -c \
"python3 /shared/aes.py --encrypt --mode ecb --key /shared/data/example/key.txt --output /shared/data/flag/enc-ecb.ppm /shared/data/example/example.ppm"
```

### 🔓 Decrypt it:

```bash
docker run --rm -v "$(pwd)":/shared thierrysans/pycryptodome bash -c \
"python3 /shared/aes.py --decrypt --mode ecb --key /shared/data/example/key.txt --output /shared/data/flag/dec-ecb.ppm /shared/data/flag/enc-ecb.ppm"
```

Swap `--mode` to `cbc` or `ctr` to try other modes.

---

## 🧪 Mode Comparisons

| Mode | Repeating Block Vulnerability | Needs Padding | Parallelizable | Notes                             |
| ---- | ----------------------------- | ------------- | -------------- | --------------------------------- |
| ECB  | ✅ Yes                        | ✅ Yes        | ✅ Yes         | Leaks structure                   |
| CBC  | ❌ No                         | ✅ Yes        | ❌ No          | Stronger chaining                 |
| CTR  | ❌ No                         | ❌ No         | ✅ Yes         | Secure **only** with unique nonce |

---

## 🖼️ Visual Outcome

- `output.ppm` reveals the hidden word: **"rijndael"** — the name of AES’s original cipher.
- `enc-ecb.ppm` of a clean image leaks structure (e.g., text outline) due to ECB’s deterministic nature.
- CBC and CTR encrypted versions look random and leak nothing — when used properly.

---

## 🎓 Key Lessons

- AES-ECB is never safe for structured data like images.
- AES-CTR is secure only if the **nonce is unique for each message**.
- XORing two reused CTR ciphertexts can leak sensitive plaintext data without needing the key.

---

## ✅ Final Result

The flag was recovered visually via XOR of two improperly encrypted CTR-mode images. This challenge demonstrates how a **minor misconfiguration (reused nonce)** can completely undermine a strong encryption algorithm like AES.
s
