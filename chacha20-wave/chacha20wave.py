#!/usr/local/bin/python3

from Crypto.Cipher import ChaCha20
import wave

# =============================================
# ========= write your code below  ============
# =============================================
def read_key(keyFile):
    with open(keyFile, 'rb') as f:
        return f.read()


def encrypt(keyFile, inputFile, outputFile):
    ''' 
    Encrypts the wave inputFile with the keyFile using the ChaCha20 cipher (from PyCryptodome)
    and writes the wave outputFile
    The wave outputFile must be a playable wave file.
    (string, string, string) -> None
    '''
    key = read_key(keyFile)
    
    # Open the input wave file
    with wave.open(inputFile, 'rb') as wav_in:
        params = wav_in.getparams()  # Get WAV file parameters (header)
        frames = wav_in.readframes(wav_in.getnframes())  # Read the audio frames

    # Initialize ChaCha20 cipher
    cipher = ChaCha20.new(key=key)
    encrypted_frames = cipher.nonce + cipher.encrypt(frames)

    # Write to output wave file
    with wave.open(outputFile, 'wb') as wav_out:
        wav_out.setparams(params)  # Write the header
        wav_out.writeframes(encrypted_frames)  # Write the nonce + encrypted frames
    
def decrypt(keyFile, inputFile, outputFile):
    ''' 
    Decrypts the wave inputFile with the keyFile using the ChaCha20 cipher (from PyCryptodome)
    and writes the wave wave outputFile
    The wave output file must be a playable wave file. 
    (string, string, string) -> None
    '''
    key = read_key(keyFile)

    # Open the input encrypted wave file
    with wave.open(inputFile, 'rb') as wav_in:
        params = wav_in.getparams()  # Get WAV file parameters (header)
        frames = wav_in.readframes(wav_in.getnframes())  # Read the audio frames

    # Extract nonce and ciphertext
    nonce = frames[:8]  # First 8 bytes are the nonce
    ciphertext = frames[8:]  # The rest is the encrypted data

    # Initialize ChaCha20 cipher with the extracted nonce
    cipher = ChaCha20.new(key=key, nonce=nonce)
    decrypted_frames = cipher.decrypt(ciphertext)

    # Write to output wave file
    with wave.open(outputFile, 'wb') as wav_out:
        wav_out.setparams(params)  # Write the header
        wav_out.writeframes(decrypted_frames)  # Write the decrypted frames


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
      opts, args = getopt.getopt(sys.argv[1:],"hedk:o:",["help", "encrypt", "decrypt", "key=", "output="])
    except getopt.GetoptError as err:
      print(err)
      usage()
    # extract parameters
    mode = None
    keyFile = None
    outputFile = None
    inputFile = args[0] if len(args) > 0 else None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
           usage()
        elif opt in ("-e", "--encrypt"):
           mode = encrypt
        elif opt in ("-d", "--decrypt"):
           mode = decrypt
        elif opt in ("-k", "--key"):
           keyFile = arg
        elif opt in ("-o", "--output"):
           outputFile = arg
    # check arguments
    if (mode is None):
       print('encrypt/decrypt option is missing\n')
       usage()
    if (keyFile is None):
       print('key option is missing\n')
       usage()
    if (outputFile is None):
       print('output option is missing\n')
       usage()
    if (inputFile is None):
       print('input_file is missing\n')
       usage()
    # run the command
    mode(keyFile, inputFile, outputFile)
