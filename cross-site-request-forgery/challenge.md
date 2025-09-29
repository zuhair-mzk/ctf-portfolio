# Cross-Site Request Forgery (CSRF) Challenge

## Challenge Description

This web application security challenge focuses on **Cross-Site Request Forgery (CSRF)** attacks against vulnerable web applications. Participants must exploit the lack of CSRF protection to perform unauthorized actions on behalf of authenticated users.

## Objective

Exploit CSRF vulnerabilities in a microblog application to:
1. **Understand CSRF attack mechanics** and browser behavior
2. **Craft malicious websites** that trigger cross-origin requests
3. **Bypass authentication** using victim's session cookies
4. **Execute unauthorized actions** on the victim's behalf
5. **Demonstrate the impact** of missing CSRF protections

## Files Provided

- `index.html` - Malicious website hosting the CSRF attack
- `exploit.js` - JavaScript payload for automatic form submission
- `docker-compose.yml` - Containerized environment for testing
- Target: Vulnerable microblog application

## Skills Tested

- **Web Application Security**: Understanding cross-site request vulnerabilities
- **JavaScript Development**: Client-side attack scripting and DOM manipulation
- **HTTP Protocol**: Cross-origin requests and cookie behavior
- **Social Engineering**: Combining technical attacks with user deception
- **Container Security**: Testing in isolated Docker environments
- **Web Development**: Understanding form submissions and authentication flows

## Learning Outcomes

By completing this challenge, you will gain practical experience with:
- CSRF attack vectors and exploitation techniques
- Browser same-origin policy and its limitations
- Cookie security attributes (SameSite, Secure, HttpOnly)
- Automated attack execution using JavaScript
- Web application authentication bypass methods
- Defense mechanisms against cross-site request forgery

## Technical Requirements

### Attack Components
- **Malicious Website**: Host attacker-controlled content
- **JavaScript Payload**: Automatically submit cross-origin forms
- **Social Engineering**: Trick victims into visiting malicious site
- **Target Application**: Vulnerable microblog without CSRF protection

### Environment Setup
```bash
# Launch containerized environment
docker-compose up

# Access vulnerable application
http://localhost:8080
```

### Attack Execution
1. **Victim Authentication**: Target user logs into vulnerable application
2. **Malicious Link Distribution**: Victim visits attacker's website
3. **Automatic Exploitation**: JavaScript executes CSRF attack
4. **Unauthorized Actions**: Requests processed using victim's session

## Difficulty Level

**Intermediate** - Requires understanding of:
- Web application security fundamentals
- JavaScript and DOM manipulation
- HTTP protocol and cookie mechanics
- Cross-origin request behavior
- Container-based testing environments

## Vulnerability Analysis

### Target Weaknesses
- **Missing CSRF tokens** in state-changing requests
- **No SameSite cookie protection** allowing cross-origin requests
- **Lack of origin validation** on server-side
- **Automatic form submission** possible via JavaScript

### Attack Surface
- POST endpoints accepting form data
- Authenticated session management
- Cross-origin request handling
- Client-side JavaScript execution

## Educational Purpose

This challenge teaches both **offensive and defensive** web security concepts:
- **Attack implementation** to understand real-world threats
- **Vulnerability identification** in web application design
- **Defense strategies** including CSRF tokens and SameSite cookies
- **Secure development practices** for preventing CSRF attacks

Essential for understanding modern web application security and the importance of implementing comprehensive CSRF protection mechanisms.