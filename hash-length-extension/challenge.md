# Hash Length Extension Attack Challenge

## Challenge Description

This cybersecurity challenge focuses on **hash length extension attacks** against vulnerable authentication systems using SHA-256 hashing. Participants must exploit a fundamental weakness in custom MAC (Message Authentication Code) implementations to forge authenticated messages and manipulate application behavior.

## Objective

Implement a sophisticated hash length extension attack with the following requirements:
1. **Understand vulnerable MAC construction** using `SHA256(key || message)` pattern
2. **Exploit hash function internals** to extend authenticated messages without knowing the secret key
3. **Implement hash state manipulation** using custom hash extension tools
4. **Forge authenticated tokens** for unauthorized operations
5. **Demonstrate practical impact** in realistic web application scenarios
6. **Execute remote attacks** against grade manipulation systems

## Files Provided

- `alice.py` - Token generation system creating vulnerable HMACs using `SHA256(key + message)`
- `bob.py` - Token verification system validating HMAC authenticity
- `mallory.py` - Attack implementation framework for hash length extension
- `attack.py` - Web application exploitation script for grade manipulation
- `hlextend.py` - Hash extension library for SHA-256 state manipulation
- `generate_tag.py` - Utility for creating legitimate authentication tags
- `message.txt` - Original authenticated message (`"get balance"`)
- `ext.txt` - Extension payload for attack (`"after withdrawing 100"`)
- `key.txt` - Secret key used in MAC generation (for testing purposes)
- `hmac.txt` - Legitimate HMAC token for original message
- `fake-hmac.txt` - Forged HMAC demonstrating successful attack

## Skills Tested

- **Cryptographic Vulnerabilities**: Understanding hash function internal states and vulnerabilities
- **Hash Length Extension**: Exploiting Merkle-Damgård construction weaknesses
- **Authentication Bypass**: Forging valid authentication tokens without secret keys
- **Python Cryptography**: Advanced manipulation of hash function internals
- **Web Application Security**: Exploiting authentication flaws in real applications
- **Attack Implementation**: Building practical exploits for cryptographic vulnerabilities

## Learning Outcomes

By completing this challenge, you will gain practical experience with:
- Hash function internal mechanics and state manipulation
- Critical flaws in custom MAC implementations
- Length extension attacks against SHA-256 and similar algorithms
- Proper vs. improper authentication token construction (HMAC vs. naive concatenation)
- Real-world impact of cryptographic implementation errors
- Web application authentication bypass techniques

## Technical Requirements

### Core Implementation
- **Hash State Manipulation**: Use `hlextend.py` library to manipulate SHA-256 internal states
- **Message Extension**: Append additional data to authenticated messages
- **Token Forgery**: Create valid authentication tokens for extended messages
- **Remote Exploitation**: Execute attacks against web applications using forged tokens

### Vulnerability Analysis
The vulnerable MAC construction follows this pattern:
```python
def createToken(key, message):
    return hashlib.sha256(key + message).hexdigest().encode() + message
```

**Critical Flaw**: Using `SHA256(key || message)` instead of proper HMAC construction allows:
- Hash state extraction from existing valid tokens
- Message extension without key knowledge  
- Authentication bypass through cryptographic manipulation

### Attack Methodology
1. **Token Analysis**: Extract hash value and original message from legitimate token
2. **State Initialization**: Set SHA-256 internal state to match extracted hash
3. **Message Extension**: Append malicious payload to original authenticated message
4. **Hash Computation**: Calculate new hash for extended message using manipulated state
5. **Token Forgery**: Construct forged token with new hash and extended message

## Challenge Scenarios

### **Scenario 1: Banking System Exploitation**
- **Original Message**: `"get balance"`
- **Extension**: `"after withdrawing 100"`
- **Goal**: Forge authentication token that appears to authorize money withdrawal
- **Impact**: Demonstrate how authentication bypass leads to financial fraud

### **Scenario 2: Grade Manipulation System**
- **Target**: Web application at `grades.seclab.space`
- **Method**: Extend legitimate authentication tokens to include grade modification parameters
- **Payload**: Add `&mark=100` to authenticated requests
- **Result**: Unauthorized grade changes through token forgery

## Security Implications

This challenge demonstrates several critical cybersecurity concepts:

### **Cryptographic Implementation Errors**
- **Vulnerability**: Naive MAC construction using simple concatenation
- **Weakness**: Hash function internal state exposure through output
- **Exploitation**: Length extension attacks against Merkle-Damgård constructions

### **Authentication System Flaws**
- **Risk**: Complete authentication bypass without key compromise
- **Impact**: Unauthorized operations with valid-appearing tokens
- **Scope**: Any system using vulnerable MAC construction patterns

### **Proper Mitigation Strategies**
- **HMAC Implementation**: Use proper HMAC construction with nested hashing
- **Key-Hashed Authentication**: Implement `HMAC(key, message)` instead of `SHA256(key || message)`
- **Cryptographic Libraries**: Leverage vetted authentication libraries rather than custom implementations

## Success Criteria

A successful implementation should:
1. Successfully extract hash state from legitimate authentication tokens
2. Manipulate SHA-256 internal state using hash extension techniques
3. Forge valid authentication tokens for extended messages
4. Demonstrate authentication bypass in realistic application scenarios
5. Execute remote attacks against web-based grade manipulation systems
6. Understand and explain the fundamental cryptographic vulnerability
7. Propose and implement proper authentication mechanisms as countermeasures

## Tools and Libraries

- **hlextend.py**: Custom SHA-256 hash extension library
- **Python hashlib**: Standard library for hash computation and verification
- **HTTP client libraries**: For remote web application exploitation
- **Command-line interfaces**: All tools support flexible parameter configurations

## Real-World Relevance

Hash length extension attacks represent a class of vulnerabilities found in:
- Legacy web applications with custom authentication systems
- API authentication mechanisms using naive MAC constructions  
- Financial systems with improper cryptographic implementations
- Any system concatenating secrets with user data for authentication

Understanding these attacks is crucial for:
- **Security Assessment**: Identifying cryptographic implementation flaws
- **Secure Development**: Implementing proper authentication mechanisms
- **Incident Response**: Recognizing and mitigating authentication bypass attacks
- **Cryptographic Design**: Understanding why standard constructions (like HMAC) exist