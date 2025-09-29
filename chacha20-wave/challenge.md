# ChaCha20 Wave File Encryption Challenge

## Challenge Description

This cybersecurity challenge focuses on **modern stream cipher implementation** using the ChaCha20 algorithm for encrypting WAV audio files. Participants must implement secure audio file encryption while preserving the playable format of encrypted files.

## Objective

Implement ChaCha20 encryption and decryption for WAV audio files with the following requirements:
1. **Encrypt WAV files** using ChaCha20 stream cipher
2. **Maintain playable format** - encrypted files must remain valid WAV files
3. **Implement secure nonce handling** for proper stream cipher operation
4. **Provide command-line interface** for encryption/decryption operations
5. **Ensure perfect audio recovery** during decryption process

## Files Provided

- `chacha20wave.py` - Implementation script with encryption/decryption functions
- `data/neil/` - Neil Armstrong audio samples and encryption keys
- `data/flag/` - Challenge flag audio files and keys
- `decrypted_flag.wav` - Example of successfully decrypted audio

## Skills Tested

- **Modern Cryptography**: Implementation of ChaCha20 stream cipher
- **File Format Handling**: Understanding and preserving WAV file structure
- **Nonce Management**: Proper handling of cryptographic nonces
- **Python Programming**: Using PyCryptodome library and wave module
- **CLI Development**: Building user-friendly command-line interfaces
- **Audio Processing**: Working with binary audio data

## Learning Outcomes

By completing this challenge, you will gain practical experience with:
- Contemporary stream cipher algorithms and their applications
- Multimedia file encryption while preserving format compatibility
- Cryptographic nonce generation and management best practices
- Python cryptographic library integration (PyCryptodome)
- WAV file structure and binary audio data manipulation
- Secure software design for cryptographic applications

## Technical Requirements

### Core Implementation
- Use **PyCryptodome's ChaCha20** cipher implementation
- Properly handle **WAV file headers** and audio frame data
- Implement **automatic nonce generation** during encryption
- Store and extract nonces for decryption operations
- Maintain **audio file playability** throughout encryption process

### Command-Line Interface
```bash
# Encryption
python3 chacha20wave.py -e -k keyfile.txt -o output.wav input.wav

# Decryption  
python3 chacha20wave.py -d -k keyfile.txt -o output.wav encrypted.wav
```

## Difficulty Level

**Intermediate** - Requires understanding of:
- Stream cipher cryptography principles
- Binary file format handling
- Python programming with crypto libraries
- Audio file structure basics
- Secure coding practices for cryptographic applications

## Educational Purpose

This challenge teaches both **offensive and defensive** security concepts:
- **Cryptographic implementation** for protecting multimedia content
- **Format preservation techniques** for maintaining file usability
- **Modern cipher applications** in real-world scenarios
- **Security best practices** for nonce handling and key management

Perfect for demonstrating practical cryptographic programming skills and understanding of contemporary security algorithms.