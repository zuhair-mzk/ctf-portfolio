---

### ✅ `writeup.md`

```markdown
# Writeup – Caesar 26

This challenge involved implementing the Caesar cipher, a basic shift cipher where each letter in the plaintext is shifted a fixed number of positions in the alphabet.

---

## 🔍 My Approach

1. **Parsing CLI arguments** using `argparse` to handle mode (`--encrypt` / `--decrypt`) and key (`--key n`).
2. **Reading input files** into memory and validating that content contained only lowercase a–z.
3. **Performing the shift** using ASCII math:
   - For encryption: `chr(((ord(c) - ord('a') + key) % 26) + ord('a'))`
   - For decryption: same but subtract the key
4. **Writing output** to `stdout`, with all debug messages redirected to `stderr`.

---

## 🧪 Sample Test

### Input (`plaintext.txt`)
