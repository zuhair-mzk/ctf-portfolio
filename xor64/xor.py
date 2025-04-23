#!/usr/local/bin/python3
import base64
from Crypto.Util.strxor import strxor

# =============================================
# ========= write your code below  ============
# =============================================

def encrypt(key, plaintext):
    # Convert plaintext and key to bytes
    # Repeat key to match plaintext length
    # XOR bytes and return Base64-encoded result
    ...

def decrypt(key, ciphertext):
    # Base64-decode ciphertext
    # Repeat key to match decoded length
    # XOR and decode result to UTF-8
    ...

# =============================================
# ===== do not modify the code below ==========
# =============================================

if __name__ == "__main__":
    import os, sys, getopt
    def usage():
        print ('Usage:    ' + os.path.basename(__file__) + ' options input_file ')
        print ('Options:')
        print ('\t -e, --encrypt')
        print ('\t -d, --decrypt')
        print ('\t -k key_file, --key=key_file')
        print ('\t -o output_file, --output=output_file')
        sys.exit(2)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hedk:o:", ["help", "encrypt", "decrypt", "key=", "output="])
    except getopt.GetoptError as err:
        print(err)
        usage()

    # Parse arguments and run appropriate mode
    ...
