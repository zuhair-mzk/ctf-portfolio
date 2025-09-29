import hlextend


# =============================================
# ========= write your code below  ============
# =============================================

def createForgery(hmac_data, additional_data, key_length):
    sha256_hasher = hlextend.new('sha256')

    # Step 1: Retrieve the existing HMAC and the original message
    existing_hmac = hmac_data[:64].decode('ascii')  # HMAC extracted as a hexadecimal string
    message_body = hmac_data[64:]  # Original message in bytes

    print(f"Existing HMAC: {existing_hmac}")
    print(f"Original message: {message_body.decode('ascii')}")

    # Convert the additional data to bytes if it's in string format
    if isinstance(additional_data, str):
        additional_data = additional_data.encode()

    try:
        # Step 2: Initialize the SHA256 state with the existing HMAC
        sha256_hasher.set_state(existing_hmac)

        # Step 3: Update the hash with the original message and the additional data
        sha256_hasher.update(message_body)  # Incorporate the original message
        sha256_hasher.update(additional_data)  # Incorporate the additional data

        forged_hmac = sha256_hasher.hexdigest()  # Obtain the new HMAC as a hexadecimal string

    except Exception as error:
        print(f"Error during HMAC extension: {error}")
        return None

    # Step 4: Determine the total length for padding
    total_length = len(message_body) + key_length
    padding_data = sha256_hasher.padding(total_length)  # Compute the required padding

    # Step 5: Construct the final forgery payload
    forged_payload = (
        bytes.fromhex(forged_hmac) +  # Convert the forged HMAC from hex to bytes
        message_body +  # Original message remains in bytes
        padding_data +  # Padding is in bytes
        additional_data  # Additional data is in bytes
    )

    return forged_payload





# =============================================
# ===== do not modify the code below ==========
# =============================================
    
if __name__ == "__main__":
   import os, sys, getopt
   def usage():
        print ('Usage:    ' + os.path.basename(__file__) + ' options input_file ')
        print ('Options:')
        print ('\t -x extension_file, --extension=extension_file')
        print ('\t -o output_file, --output=output_file')
        print ('\t -k n, --key-length=n')
        sys.exit(2)
   try:
      opts, args = getopt.getopt(sys.argv[1:],"hx:o:k:",["help", "extension=", "output=", "key-length="])
   except getopt.GetoptError as err:
      print(err)
      usage()
   # extract parameters
   extensionFile = None
   outputFile = None
   keyLength = None
   inputFile = args[0] if len(args) > 0 else None
   for opt, arg in opts:
        if opt in ("-h", "--help"):
           usage()
        elif opt in ("-x", "--extension"):
           extensionFile = arg
        elif opt in ("-o", "--output"):
           outputFile = arg
        elif opt in ("-k", "--key-length"):
           keyLength = int(arg)
   # check arguments
   if (extensionFile is None):
       print('extension option is missing\n')
       usage()
   if (outputFile is None):
       print('output option is missing\n')
       usage()
   if (inputFile is None):
       print('input_file is missing\n')
       usage()
  # run the command
   with open(extensionFile, "rb") as extensionStream:
        extension = extensionStream.read()
        with open(inputFile, "rb") as inputStream:
            data = inputStream.read()
            output = forgeIllegalPayload(data, extension, keyLength)
            with open(outputFile, "wb") as outputStream:
                outputStream.write(output)