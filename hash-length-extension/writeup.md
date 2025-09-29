# Writeup – Hash Length Extension Attack Challenge

This challenge involved exploiting a **fundamental cryptographic vulnerability** in custom MAC (Message Authentication Code) implementations using hash length extension attacks against SHA-256. The goal was to forge authenticated tokens without knowing the secret key by manipulating hash function internal states.

---

## 🔍 Challenge Overview

The challenge required understanding and exploiting the weakness in naive MAC construction using `SHA256(key || message)` instead of proper HMAC. This vulnerability allows attackers to extend authenticated messages and create valid authentication tokens for malicious payloads without access to the secret key.

### 🎯 Key Requirements:
- Understand vulnerable MAC construction patterns
- Exploit SHA-256 internal state mechanisms
- Implement hash length extension using custom tools
- Forge authentication tokens for extended messages
- Execute practical attacks against web applications
- Demonstrate real-world impact through grade manipulation

---

## 🛠️ My Implementation Approach

### 1. **Vulnerability Analysis**
The core vulnerability lies in the MAC construction used by Alice's token generation system:

```python
def createToken(key, message):
    return hashlib.sha256(key + message).hexdigest().encode() + message
```

**Critical Flaw**: This construction creates tokens using `SHA256(key || message)` where:
- The hash acts as authentication
- The original message is appended in plaintext
- Hash internal state can be extracted and manipulated

**Why This Is Vulnerable:**
- SHA-256 uses Merkle-Damgård construction with exposed internal state
- Given `H(key || message)`, attackers can compute `H(key || message || padding || extension)` 
- No knowledge of the secret key is required for hash extension

### 2. **Hash Length Extension Theory**
Understanding the cryptographic foundation was crucial:

```python
# SHA-256 processes data in blocks, maintaining internal state
# Original: SHA256(key + "get balance") = hash_value
# Extension: SHA256(key + "get balance" + padding + "after withdrawing 100")
#           = extended_hash_value (computable without knowing key)
```

**Key Insights:**
- Hash functions process input in fixed-size blocks (512 bits for SHA-256)
- Internal state after processing becomes the hash output
- This state can be used as starting point for processing additional data
- Proper padding calculation is essential for successful extension

### 3. **Attack Implementation in `mallory.py`**

#### **Step 1: Extract Original Data**
```python
def createForgery(hmac_data, additional_data, key_length):
    sha256_hasher = hlextend.new('sha256')
    
    # Extract components from legitimate token
    existing_hmac = hmac_data[:64].decode('ascii')  # First 64 chars = hex hash
    message_body = hmac_data[64:]  # Remaining bytes = original message
```

#### **Step 2: Initialize Hash State**
```python
# Set SHA-256 internal state to match extracted hash
sha256_hasher.set_state(existing_hmac)
```

**Critical Implementation Detail**: The `hlextend` library allows direct manipulation of SHA-256 internal registers, effectively "rewinding" the hash function to its state after processing the original `key + message`.

#### **Step 3: Compute Hash Extension**
```python
# Process original message and additional data
sha256_hasher.update(message_body)      # Original: "get balance"
sha256_hasher.update(additional_data)   # Extension: "after withdrawing 100"

forged_hmac = sha256_hasher.hexdigest() # New hash for extended message
```

#### **Step 4: Construct Forged Token** 
```python
# Calculate proper padding for block alignment
total_length = len(message_body) + key_length
padding_data = sha256_hasher.padding(total_length)

# Build complete forged token
forged_payload = (
    bytes.fromhex(forged_hmac) +  # New authentication hash
    message_body +               # Original authenticated message  
    padding_data +               # Required SHA-256 padding
    additional_data              # Malicious extension payload
)
```

### 4. **Web Application Exploitation**

#### **Grade Manipulation Attack in `attack.py`**
The practical demonstration involved exploiting a vulnerable grading system:

```python
def attack(url):
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    
    # Extract legitimate authentication components
    student_id = query_params['sid'][0]
    tag = query_params['tag'][0]

    # Load pre-computed forged HMAC 
    with open('fake-hmac.txt', 'rb') as f:
        fake_hmac = f.read()

    # Construct malicious request with forged authentication
    new_url = f"https://grades.seclab.space/?tag={tag}&sid={student_id}&mark=100"
```

**Attack Flow:**
1. **Intercept legitimate request** with valid authentication tag
2. **Extract authentication token** and student parameters  
3. **Apply hash length extension** to add `&mark=100` parameter
4. **Submit forged request** with extended authentication

---

## 🎯 Practical Attack Execution

### **Banking System Scenario**
Original authenticated message:
```
Token: 00d5951e148f0eae3807bf2129885f37f1b77812686ac5e22e4af52c3187c3fe + "get balance"
```

Extended malicious message:
```
Forged Token: [new_hash] + "get balance" + [padding] + "after withdrawing 100"
```

### **Grade System Exploitation**
1. **Legitimate Request**: `GET /grades?sid=[STUDENT_ID]&tag=[valid_hash]`
2. **Hash Extension**: Extend authentication to include grade modification
3. **Forged Request**: `GET /grades?sid=[STUDENT_ID]&tag=[forged_hash]&mark=100`
4. **Result**: Unauthorized grade change accepted by vulnerable server

---

## 🔧 Technical Challenges and Solutions

### **Challenge 1: Padding Calculation** 
**Issue**: SHA-256 requires specific padding for block alignment
**Solution**: Used `hlextend` library's padding function:
```python
padding_data = sha256_hasher.padding(total_length)
```

### **Challenge 2: Key Length Determination**
**Issue**: Attack requires knowing secret key length for proper padding
**Solution**: Implemented key length brute-force or analysis:
- Common key lengths: 8, 16, 32 bytes
- Try multiple lengths until valid token generated
- Server response patterns indicate successful authentication

### **Challenge 3: Hash State Management**
**Issue**: Precise internal state manipulation required
**Solution**: Leveraged `hlextend.py` custom library:
```python
sha256_hasher.set_state(existing_hmac)  # Direct state manipulation
```

### **Challenge 4: Message Format Consistency**
**Issue**: Extended messages must maintain expected format
**Solution**: Careful construction maintaining original message structure:
```python
# Preserve original message + padding + extension format
final_message = original + padding + extension
```

---

## 🛡️ Security Implications and Countermeasures

### **Critical Vulnerabilities Exposed:**

#### 1. **Naive MAC Construction**
- **Risk**: Using `SHA256(key || message)` instead of proper HMAC
- **Impact**: Complete authentication bypass without key compromise
- **Exploitation**: Hash length extension attacks

#### 2. **Cryptographic Implementation Errors** 
- **Risk**: Custom authentication mechanisms without cryptographic review
- **Impact**: Fundamental security failures in authentication systems
- **Scope**: Any application using vulnerable MAC patterns

### **Proper Mitigation Strategies:**

#### 1. **Use Standard HMAC Construction**
```python
# Vulnerable (DO NOT USE):
hash = SHA256(key + message)

# Secure (RECOMMENDED):
import hmac
secure_mac = hmac.new(key, message, hashlib.sha256).hexdigest()
```

#### 2. **Implement Key-Hashed Authentication**
```python
# HMAC uses nested hashing to prevent extension attacks:
# HMAC(K, m) = H((K ⊕ opad) || H((K ⊕ ipad) || m))
```

#### 3. **Cryptographic Library Usage**
- **Recommendation**: Use vetted libraries (OpenSSL, libsodium, etc.)
- **Principle**: Never implement custom cryptographic primitives
- **Validation**: Regular security audits of authentication mechanisms

---

## 📊 Attack Results and Effectiveness

### **Successful Exploitations:**
- ✅ **Authentication Bypass**: Forged valid tokens without key knowledge
- ✅ **Message Extension**: Successfully appended malicious payloads
- ✅ **Banking Simulation**: Demonstrated unauthorized transaction authorization  
- ✅ **Grade Manipulation**: Achieved unauthorized academic record modification
- ✅ **Hash State Control**: Precise manipulation of SHA-256 internal states

### **Technical Achievements:**
- ✅ **Cryptographic Understanding**: Deep analysis of hash function internals
- ✅ **Tool Development**: Effective use of custom hash extension libraries
- ✅ **Practical Impact**: Real-world attack demonstrations
- ✅ **Countermeasure Design**: Proper HMAC implementation alternatives

---

## 🎓 Key Learning Outcomes

### **Cryptographic Security Knowledge:**
- Understanding fundamental flaws in custom MAC implementations
- Hash function internal mechanics and Merkle-Damgård construction weaknesses
- Difference between naive concatenation and proper HMAC construction
- Practical cryptographic attack implementation and testing

### **Technical Skills Developed:**
- **Advanced Python Cryptography**: Hash function state manipulation and extension
- **Authentication System Analysis**: Identifying and exploiting MAC vulnerabilities
- **Custom Tool Usage**: Effective application of specialized cryptographic libraries
- **Web Application Security**: Authentication bypass techniques and exploitation

### **Security Architecture Understanding:**
- Critical importance of using standard cryptographic constructions
- Why HMAC exists and how it prevents length extension attacks
- Proper authentication token design and validation mechanisms
- Security implications of cryptographic implementation choices

---

## 🔄 Real-World Applications

This challenge provides essential knowledge for:

### **Security Assessment Roles:**
- **Penetration Testing**: Identifying authentication bypass vulnerabilities
- **Code Review**: Recognizing dangerous cryptographic patterns
- **Vulnerability Research**: Understanding hash-based attack vectors

### **Secure Development Practices:**
- **Authentication Design**: Implementing robust MAC systems
- **Cryptographic Integration**: Proper use of standard libraries
- **Security Architecture**: Understanding authentication system fundamentals

### **Incident Response and Forensics:**
- **Attack Recognition**: Identifying hash length extension exploit attempts
- **Impact Assessment**: Understanding authentication compromise scenarios
- **Mitigation Planning**: Implementing proper cryptographic countermeasures

The skills demonstrated here are directly applicable to cybersecurity positions involving authentication security, cryptographic implementation review, and security architecture design.