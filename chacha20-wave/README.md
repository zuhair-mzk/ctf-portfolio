# ChaCha20 Wave File Encryption Challenge

**Challenge Type:** Cryptographic Implementation | **Difficulty:** Intermediate | **Status:** ✅ SOLVED

## Overview

This challenge demonstrates **modern stream cipher implementation** using the ChaCha20 algorithm for encrypting WAV audio files. The goal was to develop secure audio file encryption while maintaining the playable format of encrypted files - a unique intersection of cryptography and multimedia processing.

## Challenge Structure

This folder contains all the necessary files for the ChaCha20 Wave encryption challenge:

- **`chacha20wave.py`** - Complete ChaCha20 implementation for WAV files
- **`data/`** - Test audio files and encryption keys
  - **`neil/`** - Neil Armstrong audio samples with encryption keys
  - **`flag/`** - Challenge audio files and corresponding keys
- **`decrypted_flag.wav`** - Successfully decrypted flag audio
- **`challenge.md`** - Challenge description and technical requirements
- **`writeup.md`** - Comprehensive technical analysis and methodology

## Technical Skills Demonstrated

- **Modern Cryptography**: ChaCha20 stream cipher implementation
- **File Format Preservation**: Maintaining WAV structure during encryption
- **Nonce Management**: Secure handling of cryptographic nonces
- **Python Development**: Advanced use of PyCryptodome and wave libraries
- **CLI Design**: User-friendly command-line interface development
- **Audio Processing**: Binary audio data manipulation and format handling

## Key Learning Outcomes

This challenge provided hands-on experience with:

1. **Contemporary Cryptography**: Implementation of state-of-the-art stream ciphers
2. **Multimedia Security**: Protecting audio content while preserving usability
3. **Format Engineering**: Understanding and maintaining binary file structures
4. **Secure Programming**: Cryptographic best practices and proper nonce handling
5. **Library Integration**: Professional use of established cryptographic libraries
6. **User Interface Design**: Building robust command-line tools

## Implementation Highlights

### Encryption Process
- **Stream cipher application** to WAV audio frame data
- **Nonce generation** and embedding for security
- **Format preservation** to maintain playable audio files
- **Header protection** while encrypting content

### Decryption Process  
- **Nonce extraction** from encrypted audio frames
- **Perfect audio recovery** with correct decryption keys
- **Format integrity** maintained throughout the process
- **Error handling** for robust operation

## Educational Value

This challenge showcases:
- **Real-world cryptographic applications** beyond theoretical concepts
- **Intersection of security and multimedia** technologies
- **Modern cipher implementation** using professional libraries
- **Secure software development** practices and methodologies

## Challenge Completion

Successfully implemented a complete ChaCha20 encryption/decryption system for WAV files that:
- ✅ **Encrypts audio files** while maintaining playable format
- ✅ **Provides perfect decryption** with proper key management
- ✅ **Handles nonces securely** with automatic generation/extraction  
- ✅ **Offers professional CLI** with comprehensive functionality
- ✅ **Preserves audio quality** throughout the encryption lifecycle

---

*This challenge demonstrates practical cryptographic implementation skills and showcases the application of modern security algorithms to multimedia protection scenarios.*