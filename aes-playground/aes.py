#!/usr/local/bin/python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util import Counter
from PIL import Image

# =============================================
# ======= do not change these values ==========
# =============================================

CBC_IV = b'bUQVch74NmLyWACd'
CTR_NONCE = b'PzphkGKm'

# =============================================
# ========= write your code below  ============
# =============================================      

def read_key(keyFile):
    # Function to read the encryption key from a file
    pass

def encrypt(mode, keyFile, inputFile, outputFile):
    # Function to encrypt an image file using the specified mode
    pass

def decrypt(mode, keyFile, inputFile, outputFile):
    # Function to decrypt an image file using the specified mode
    pass

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
        print ('\t -m ecb, --mode=ecb')
        print ('\t -m cbc, --mode=cbc')
        print ('\t -m ctr, --mode=ctr')
        print ('\t -k key_file, --key=key_file')
        print ('\t -o output_file, --output=output_file')
        sys.exit(2)
    try:
      opts, args = getopt.getopt(sys.argv[1:],"hedm:k:o:",["help", "encrypt", "decrypt", "mode=", "key=", "output="])
    except getopt.GetoptError as err:
      print(err)
      usage()
    # extract parameters
    op = None
    mode = None
    keyFile = None
    outputFile = None
    inputFile = args[0] if len(args) > 0 else None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
           usage()
        elif opt in ("-e", "--encrypt"):
           op = encrypt
        elif opt in ("-d", "--decrypt"):
           op = decrypt
        elif opt in ("-m", "--mode"):
           mode = arg
        elif opt in ("-k", "--key"):
           keyFile = arg
        elif opt in ("-n", "--nonce"):
           nonceFile = arg
        elif opt in ("-o", "--output"):
           outputFile = arg
    # check arguments
    if (op is None):
       print('encrypt/decrypt option is missing\n')
       usage()
    if (mode is None):
       print('mode of operation option is missing\n')
       usage()
    if mode not in ["ecb", "cbc", "ctr"]:
        print('mode of operation should be either ecb, cbc or ctr\n')
        usage()
    if (keyFile is None):
       print('key option is missing \n')
       usage()
    if (outputFile is None):
       print('output option is missing\n')
       usage()
    if (inputFile is None):
       print('input_file is missing\n')
       usage()
    # run the command
    op(mode, keyFile, inputFile, outputFile)
