#!/usr/local/bin/python3
import base64
from Crypto.Util.strxor import strxor

# =============================================
# ========= write your code below  ============
# =============================================

def crack(plaintext, ciphertext, keyLength):
    # Convert plaintext to bytes
    # Base64-decode ciphertext to bytes
    # XOR corresponding bytes to recover key
    # Return the recovered key (UTF-8 string)
    ...

# =============================================
# ===== do not modify the code below ==========
# =============================================

if __name__ == "__main__":
    import os, sys, getopt
    def usage():
        print ('Usage:    ' + os.path.basename(__file__) + ' options key_file')
        print ('Options:')
        print ('\t -c ciphertext_file, --ciphertext=ciphertext_file')
        print ('\t -p plaintext_file, --plaintext=plaintext_file')
        print ('\t -k n, --key-length=n')
        sys.exit(2)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:p:k:", ["help", "ciphertext=", "plaintext=", "key-length="])
    except getopt.GetoptError as err:
        print(err)
        usage()

    # Parse arguments, open files, call crack(), write key
    ...
