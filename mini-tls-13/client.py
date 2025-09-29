BUFFER_SIZE = 1048576  # the file size is limited to 1 mb
DH_G = 5               # co-prime
DH_KEY_SIZE = 256      # bytes
DH_NONCE_SIZE = 16     # bytes
AES_KEY_SIZE = 32      # bytes

import os, socket, json

from Crypto.Util import number
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import HKDF
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from OpenSSL import crypto

# =============================================
# ========= TLS 1.3 Implementation ============
# =============================================

def send_client_hello(sock, config):
    """Send TLS Client Hello with Diffie-Hellman parameters"""
    # Create Diffie-Hellman parameters
    p = number.getStrongPrime(2048)
    g = DH_G
    a = number.getRandomNBitInteger(2048)
    dhA = pow(g, a, p)
    
    # Generate a nonce for replay protection
    nonce = get_random_bytes(DH_NONCE_SIZE)
    
    # Send client hello: p, dhA, and nonce (n0)
    payload = p.to_bytes(256, 'big') + dhA.to_bytes(256, 'big') + nonce
    sock.sendall(payload)
    
    # Store values in config for later use
    config['p'] = p
    config['a'] = a
    config['nonce'] = nonce
    print('send client_hello: ' + str(len(payload)) + " bytes")

def receive_server_hello(sock, config):
    """Process TLS Server Hello and perform certificate validation"""
    # Receive the initial part of the payload that includes dhB and nonce_server
    payload = sock.recv(512)  # We expect 256 bytes for dhB + 16 bytes for nonce_server
    
    dhB = int.from_bytes(payload[:256], 'big')
    nonce_server = payload[256:256 + DH_NONCE_SIZE]
    
    # Now receive the remaining encrypted certificate and signature
    encrypted_payload = b''
    while True:
        part = sock.recv(BUFFER_SIZE)
        if not part:
            break
        encrypted_payload += part

    # Calculate the shared secret and session key using HKDF
    m = pow(dhB, config['a'], config['p'])
    k = HKDF(m.to_bytes(256, 'big'), AES_KEY_SIZE, config['nonce'] + nonce_server, SHA256)
    config['session_key'] = k
    
    # Decrypt the encrypted certificate and signature using AES-GCM
    cipher = AES.new(k, AES.MODE_GCM, nonce=nonce_server)
    cert_and_sig = cipher.decrypt_and_verify(encrypted_payload[:-16], encrypted_payload[-16:])
    
    # Extract certificate and signature
    cert_len = int.from_bytes(cert_and_sig[:4], 'big')
    cert = cert_and_sig[4:4 + cert_len]
    signature = cert_and_sig[4 + cert_len:]

    # Verify the certificate and signature
    server_cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
    org = server_cert.get_subject().O
    if org != config['to']:
        print("Invalid server organization")
        sys.exit(1)

    # Verify the signature using the public key from the certificate
    pub_key = server_cert.get_pubkey().to_cryptography_key()
    verifier = pkcs1_15.new(pub_key)
    verifier.verify(SHA256.new(config['nonce'] + nonce_server), signature)

    print('Received server_hello: ' + str(len(payload) + len(encrypted_payload)) + " bytes")

def send_request(sock, config):
    """Send encrypted request using AES-GCM"""
    # Use AES to encrypt the request
    payload = json.dumps({'request': config['request'], 'filename': config['filename'], 'from': config['from']}).encode('utf-8')
    
    cipher = AES.new(config['session_key'], AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(payload)
    
    sock.sendall(cipher.nonce + tag + ciphertext)
    print('send: ' + payload.decode('utf-8'))

def receive_ready(sock, config):
    """Receive server ready confirmation"""
    data = sock.recv(BUFFER_SIZE)
    cipher = AES.new(config['session_key'], AES.MODE_GCM, nonce=data[:DH_NONCE_SIZE])
    decrypted_data = cipher.decrypt(data[DH_NONCE_SIZE + 16:])
    
    metada = json.loads(decrypted_data.decode('utf-8'))
    print('recv: ' + decrypted_data.decode('utf-8'))
    
    if not metada['ready']:
        print('server ' + config['to'] + ' cannot upload file')
        sys.exit(1)

def send_upload(sock, config):
    """Send encrypted file upload"""
    if not os.path.exists(config['filepath']):
        print('file does not exists: ' + config['filepath'])
        sys.exit(1)

    # Encrypt the file content using AES
    file_content = open(config['filepath'], "rb").read()
    cipher = AES.new(config['session_key'], AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(file_content)
    
    sock.sendall(cipher.nonce + tag + ciphertext)
    print('send: upload ' + config['filepath'] + ' as ' + config['filename'])

def receive_download(sock, config):
    """Receive and decrypt downloaded file"""
    data = sock.recv(BUFFER_SIZE)
    
    # Decrypt the downloaded file using AES
    cipher = AES.new(config['session_key'], AES.MODE_GCM, nonce=data[:DH_NONCE_SIZE])
    file_content = cipher.decrypt(data[DH_NONCE_SIZE + 16:])
    
    if not os.path.exists(os.path.dirname(config['filepath'])):
        os.makedirs(os.path.dirname(config['filepath']))
    
    file_out = open(config['filepath'], "wb")
    file_out.write(file_content)
    file_out.close()
    print('recv: download ' + config['filename'] + ' into ' + config['filepath'])

# =============================================
# ===== TLS Client Main Protocol Handler =====
# =============================================

def client(config):
    """Main TLS client protocol handler"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # TLS handshake
        sock.connect((host, port))
        send_client_hello(sock, config)
        receive_server_hello(sock, config)
        # Encrypted data exchange
        send_request(sock, config)
        if config['request'] == 'upload':
            receive_ready(sock, config)
            send_upload(sock, config)
        elif config['request'] == 'download':
            receive_download(sock, config)
    
if __name__ == "__main__":
    import os, sys, getopt
    def usage():
        print ('Usage:    ' + os.path.basename(__file__) + ' options filepath ')
        print ('Options:')
        print ('\t -f from, --from=from')
        print ('\t -t to, --to=to')
        print ('\t -r roots, --roots=roots')
        print ('\t -u, --upload')
        print ('\t -d, --download')
        print ('\t -f filename, --filename=filename')
        sys.exit(2)
    try:
      opts, args = getopt.getopt(sys.argv[1:],"hudp:s:f:t:r:f:",["help", "upload", "download", "from=", "to=", "roots=", "filename="])
    except getopt.GetoptError as err:
      print(err)
      usage()
    # extract parameters
    request = None
    fr = None
    to = None
    roots = None
    filename = None
    filepath = args[0] if len(args) > 0 else None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
           usage()
        elif opt in ("-u", "--upload"):
           request = 'upload'
        elif opt in ("-d", "--download"):
           request = 'download'
        elif opt in ("-f", "--from"):
           fr = arg
        elif opt in ("-t", "--to"):
           to = arg
        elif opt in ("-r", "--roots"):
           roots = arg
        elif opt in ("-f", "--filename"):
           filename = arg
    # check arguments
    if (request is None):
       print('upload/download option is missing\n')
       usage()
    if (fr is None):
       print('from option is missing\n')
       usage()
    if (to is None):
       print('to option is missing\n')
       usage()
    if (roots is None):
       print('roots option is missing\n')
       usage()      
    if (filename is None):
       print('filename option is missing\n')
       usage()
    if (filepath is None):
       print('filepath is missing\n')
       usage()
    # create config
    config = {'request': request, 'from': fr, 'filename': filename, 'filepath': filepath}
    # extract server information
    config['to'] = to.split("@")[0]
    host = to.split("@")[1].split(":")[0]
    port = int(to.split(":")[1])
    # extract all root certificates
    if not os.path.exists(roots):
        print('root certificates path does not exists\n')
        usage()
    else:
        list_of_files = os.listdir(roots)
        config['roots']=[]
        for file in list_of_files:
            f = open(os.path.join(roots, file), "r")
            config['roots'].append(f.read())
            f.close()
    # run the TLS client
    client(config)