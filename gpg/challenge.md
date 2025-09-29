# GPG Cryptography and Digital Signatures Challenge

## Challenge Description

This cybersecurity challenge focuses on **GNU Privacy Guard (GPG) cryptography operations**, including public key cryptography, digital signatures, message encryption, and cryptographic verification. Participants must demonstrate mastery of GPG key management, message authentication, and secure communication protocols used in real-world cryptographic systems.

## Objective

Master comprehensive GPG cryptography operations with the following requirements:
1. **Public Key Management**: Import, export, and manage GPG public and private key pairs
2. **Digital Signature Verification**: Verify authenticity and integrity of signed messages
3. **Message Encryption**: Encrypt sensitive data using public key cryptography
4. **Decryption Operations**: Decrypt encrypted messages using corresponding private keys
5. **Combined Operations**: Handle messages that are both encrypted AND digitally signed
6. **Key Trust Validation**: Understand and work with GPG trust models and key validation
7. **Cryptographic Analysis**: Extract and verify cryptographic flags from multiple sources

## Files Provided

### **Core GPG Files**
- `key.asc` - Student's GPG public key for encryption and signature verification
- `key2.asc` - Secondary public key for additional cryptographic operations  
- `instructorkey.asc` - Instructor's public key for message verification and encryption
- `private-key.asc` - Private key component for decryption operations
- `zuhair.khan` - Key identifier file for key management operations

### **Message Files**
- `signed.txt` - Plaintext message demonstrating digital signature concepts
- `signed.txt.asc` - Detached signature file for signature verification
- `signed.asc` - Cleartext signed message with embedded signature
- `encryptedAndSigned.txt` - Plaintext version of encrypted+signed message
- `encryptedAndSigned.asc` - Message that is both encrypted AND digitally signed

### **Challenge Flags**
- `flag.txt` - Primary challenge flag requiring GPG operations to access
- `flags/0.txt` through `flags/9.txt` - Multiple signed flag files requiring verification

## Skills Tested

- **Public Key Cryptography**: Understanding RSA/DSA key generation and management
- **Digital Signatures**: Creating and verifying cryptographic message signatures  
- **Message Encryption**: Symmetric and asymmetric encryption using GPG
- **Key Trust Models**: GPG web of trust concepts and key validation
- **Cryptographic Verification**: Ensuring message authenticity and integrity
- **Command-Line Cryptography**: Proficiency with GPG command-line operations
- **Security Best Practices**: Proper key handling and cryptographic workflows

## Learning Outcomes

By completing this challenge, you will gain practical experience with:
- GPG key generation, import/export, and lifecycle management
- Digital signature creation and verification processes
- Public key encryption and private key decryption workflows
- Combined encryption+signing operations for maximum security
- Real-world cryptographic communication protocols
- Command-line cryptography tools and best practices
- Understanding of PKI (Public Key Infrastructure) concepts

## Technical Requirements

### **GPG Operations Mastery**
```bash
# Key Management
gpg --import key.asc
gpg --import instructorkey.asc
gpg --list-keys
gpg --list-secret-keys

# Signature Verification
gpg --verify signed.asc
gpg --verify signed.txt.asc signed.txt

# Message Decryption
gpg --decrypt encryptedAndSigned.asc

# Combined Operations
gpg --decrypt-and-verify encryptedAndSigned.asc
```

### **Challenge Tasks**
1. **Key Import**: Successfully import all provided public keys into GPG keyring
2. **Signature Verification**: Verify authenticity of all signed messages and flag files
3. **Message Decryption**: Decrypt encrypted messages to reveal hidden content
4. **Flag Collection**: Extract cryptographic flags from various signed and encrypted sources
5. **Trust Management**: Properly handle key trust levels and signature validation

## Challenge Scenarios

### **Scenario 1: Message Authentication**
- **Goal**: Verify that signed messages actually came from claimed senders
- **Process**: Use GPG signature verification to confirm message authenticity
- **Skills**: Digital signature validation, key fingerprint verification

### **Scenario 2: Confidential Communication**  
- **Goal**: Decrypt encrypted messages using appropriate private keys
- **Process**: Use GPG decryption to reveal confidential message content
- **Skills**: Public key decryption, private key management

### **Scenario 3: Maximum Security Communication**
- **Goal**: Handle messages with both encryption AND digital signatures
- **Process**: Decrypt content while simultaneously verifying sender authenticity  
- **Skills**: Combined cryptographic operations, dual verification

### **Scenario 4: Flag Hunting**
- **Goal**: Extract multiple cryptographic flags from various signed sources
- **Process**: Systematically verify and extract flags from numbered flag files
- **Skills**: Batch cryptographic operations, systematic verification

## Security Implications

This challenge demonstrates critical cybersecurity concepts:

### **Authentication vs. Confidentiality**
- **Digital Signatures**: Provide authentication and non-repudiation
- **Encryption**: Provides confidentiality and privacy protection
- **Combined Use**: Achieves both goals simultaneously for maximum security

### **Key Management Security**
- **Public Key Distribution**: Secure methods for sharing public keys
- **Private Key Protection**: Critical importance of private key security
- **Key Trust Models**: Understanding web of trust vs. certificate authority models

### **Real-World Applications**
- **Secure Email**: PGP/GPG email encryption and signing
- **Software Distribution**: Package signing for software integrity
- **Document Authentication**: Legal and business document verification
- **Whistleblower Communication**: Secure, anonymous communication channels

## GPG Command Reference

### **Essential Commands**
```bash
# Key Operations
gpg --gen-key                    # Generate new key pair
gpg --import keyfile.asc         # Import public key
gpg --export -a "Name"           # Export public key
gpg --list-keys                  # List all public keys
gpg --fingerprint               # Show key fingerprints

# Signing Operations  
gpg --sign message.txt           # Create signed message
gpg --clearsign message.txt      # Create cleartext signature
gpg --detach-sign message.txt    # Create detached signature
gpg --verify signed.asc          # Verify signature

# Encryption Operations
gpg --encrypt -r "recipient" file.txt     # Encrypt for recipient
gpg --decrypt encrypted.asc               # Decrypt message
gpg --encrypt --sign -r "recipient" file  # Encrypt and sign
```

## Success Criteria

A successful implementation should:
1. Successfully import all provided GPG public keys
2. Verify signatures on all signed messages and flag files
3. Decrypt all encrypted content using appropriate keys
4. Extract all cryptographic flags from various sources
5. Demonstrate understanding of GPG trust models and key validation
6. Handle both simple and complex cryptographic operations (encryption+signing)
7. Explain the security implications of different cryptographic operations
8. Show proficiency with GPG command-line interface and workflows

## Real-World Relevance

GPG skills are essential for:
- **Cybersecurity Professionals**: Implementing secure communication systems
- **Software Developers**: Signing code and verifying software integrity  
- **System Administrators**: Managing secure server communications
- **Privacy Advocates**: Protecting confidential communications
- **Digital Forensics**: Verifying digital evidence authenticity
- **Compliance Officers**: Meeting regulatory requirements for data protection

Understanding GPG provides foundation knowledge for modern cryptographic systems, secure communication protocols, and privacy-preserving technologies used throughout the cybersecurity industry.