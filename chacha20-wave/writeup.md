# Writeup – ChaCha20 Wave File Encryption

This challenge involved implementing **ChaCha20 stream cipher encryption and decryption** for WAV audio files. The goal was to develop secure audio file encryption while maintaining the playable format of the encrypted output.

---

## 🔍 Challenge Overview

The challenge required implementing the ChaCha20 cipher to encrypt and decrypt WAV audio files using the **PyCryptodome** library. The key requirement was that encrypted WAV files must remain **playable** while containing encrypted audio data.

### 🎯 Key Requirements:
- Implement ChaCha20 encryption/decryption for WAV files
- Preserve WAV file structure and headers
- Ensure encrypted files remain playable audio files
- Handle nonce generation and storage properly
- Support command-line interface for encryption/decryption operations

---

## 🛠️ My Implementation Approach

### 1. **WAV File Structure Analysis**
Understanding the WAV file format was crucial:
```python
with wave.open(inputFile, 'rb') as wav_in:
    params = wav_in.getparams()    # WAV header parameters
    frames = wav_in.readframes(wav_in.getnframes())  # Audio data frames
```

### 2. **ChaCha20 Cipher Integration**
Used PyCryptodome's ChaCha20 implementation:
```python
from Crypto.Cipher import ChaCha20

# Encryption
cipher = ChaCha20.new(key=key)
encrypted_frames = cipher.nonce + cipher.encrypt(frames)

# Decryption  
nonce = frames[:8]  # Extract nonce from encrypted data
ciphertext = frames[8:]  # Remaining encrypted audio
cipher = ChaCha20.new(key=key, nonce=nonce)
decrypted_frames = cipher.decrypt(ciphertext)
```

### 3. **Nonce Handling Strategy**
Critical design decision for nonce management:
- **Encryption**: Generate random nonce, prepend to encrypted data
- **Decryption**: Extract nonce from first 8 bytes of encrypted frames
- **Storage**: Embed nonce directly in the WAV file's frame data

### 4. **WAV File Preservation**
Maintained playable WAV format:
```python
# Preserve original WAV parameters
with wave.open(outputFile, 'wb') as wav_out:
    wav_out.setparams(params)      # Keep original header
    wav_out.writeframes(encrypted_frames)  # Write encrypted content
```

### 5. **Command-Line Interface**
Implemented robust CLI with proper error handling:
- `-e/--encrypt` and `-d/--decrypt` mode selection
- `-k/--key` for key file specification  
- `-o/--output` for output file naming
- Input validation and usage instructions

---

## 🔬 Technical Implementation Details

### Encryption Process
```python
def encrypt(keyFile, inputFile, outputFile):
    key = read_key(keyFile)
    
    # Read original WAV file
    with wave.open(inputFile, 'rb') as wav_in:
        params = wav_in.getparams()
        frames = wav_in.readframes(wav_in.getnframes())
    
    # ChaCha20 encryption
    cipher = ChaCha20.new(key=key)
    encrypted_frames = cipher.nonce + cipher.encrypt(frames)
    
    # Write encrypted WAV
    with wave.open(outputFile, 'wb') as wav_out:
        wav_out.setparams(params)
        wav_out.writeframes(encrypted_frames)
```

### Decryption Process
```python
def decrypt(keyFile, inputFile, outputFile):
    key = read_key(keyFile)
    
    # Read encrypted WAV file
    with wave.open(inputFile, 'rb') as wav_in:
        params = wav_in.getparams()
        frames = wav_in.readframes(wav_in.getnframes())
    
    # Extract nonce and decrypt
    nonce = frames[:8]
    ciphertext = frames[8:]
    cipher = ChaCha20.new(key=key, nonce=nonce)
    decrypted_frames = cipher.decrypt(ciphertext)
    
    # Write decrypted WAV
    with wave.open(outputFile, 'wb') as wav_out:
        wav_out.setparams(params)
        wav_out.writeframes(decrypted_frames)
```

---

## 🧪 Testing and Validation

### Test Data Structure
The challenge included comprehensive test data:
- **Neil Armstrong samples**: `neil.wav` → `neilc.wav` (encrypted)
- **Flag audio**: `flagc.wav` (encrypted flag audio)
- **Multiple keys**: Different encryption keys for various samples
- **Decryption verification**: Successfully recovered original audio

### Key Management
```
data/neil/key.txt: "1SmallStep4Man1GiantLeap4Mankind"
data/flag/key.txt: "Bowman: OpenThePodBayDoors, HAL."
```

### Validation Process
1. ✅ **Encryption**: Original WAV → Encrypted playable WAV
2. ✅ **Decryption**: Encrypted WAV → Recovered original audio
3. ✅ **Format Integrity**: All output files remain valid WAV format
4. ✅ **Audio Quality**: Perfect audio recovery with correct keys

---

## 🏆 Solution Results

The implementation successfully:
- ✅ **Encrypts WAV files** while maintaining playable format
- ✅ **Decrypts audio** with perfect fidelity recovery
- ✅ **Handles nonce management** securely and efficiently  
- ✅ **Preserves WAV structure** in all operations
- ✅ **Provides robust CLI** with comprehensive error handling

### 🎵 Audio Encryption Demo
```bash
# Encrypt audio file
python3 chacha20wave.py -e -k data/neil/key.txt -o encrypted_output.wav neil_input.wav

# Decrypt audio file  
python3 chacha20wave.py -d -k data/neil/key.txt -o decrypted_output.wav encrypted_input.wav
```

---

## 🛡️ Security Considerations

### ChaCha20 Advantages
- **Stream cipher**: Efficient for audio data encryption
- **Strong security**: Cryptographically secure against known attacks
- **Performance**: Fast encryption/decryption suitable for media files
- **Nonce-based**: Each encryption uses unique nonce for security

### Implementation Security
- **Proper nonce handling**: Automatic generation and storage
- **Key management**: Secure key reading from external files
- **Format preservation**: No information leakage through format changes
- **Error handling**: Prevents information disclosure through error messages

---

## 📚 Key Learnings

1. **Stream cipher applications**: ChaCha20 usage for media file encryption
2. **File format preservation**: Maintaining structure while encrypting content
3. **Nonce management**: Critical importance of unique nonces in stream ciphers
4. **Audio processing**: Working with WAV file structure and headers
5. **CLI development**: Building user-friendly command-line interfaces
6. **Cryptographic integration**: Properly using established crypto libraries

---

## 🎯 Educational Value

This challenge demonstrated:
- **Modern cryptography**: Implementation of contemporary cipher algorithms
- **Media security**: Protecting multimedia content while preserving usability
- **Software engineering**: Building robust, user-friendly crypto tools
- **Format handling**: Understanding and preserving binary file formats
- **Security best practices**: Proper nonce handling and key management

---

## 📁 Files Overview

- [`chacha20wave.py`](./chacha20wave.py) - Complete ChaCha20 implementation
- [`data/`](./data/) - Test audio files and encryption keys
  - [`neil/`](./data/neil/) - Neil Armstrong audio samples and keys
  - [`flag/`](./data/flag/) - Challenge flag audio and keys
- [`decrypted_flag.wav`](./decrypted_flag.wav) - Successfully decrypted flag audio
- [`challenge.md`](./challenge.md) - Challenge description and objectives
- [`writeup.md`](./writeup.md) - This technical analysis

This challenge showcased practical cryptographic implementation skills and demonstrated the application of modern ciphers to multimedia security challenges.