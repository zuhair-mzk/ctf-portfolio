# Scapy Spy Network Monitoring Challenge

## Challenge Overview

This network analysis challenge focuses on implementing packet filtering and analysis using Scapy, a powerful Python library for network packet manipulation. The challenge involves monitoring network traffic in a containerized environment to capture and analyze DNS, HTTP, and HTTPS communications.

## Learning Objectives

- **Network Protocol Analysis**: Understanding DNS queries, HTTP requests, and HTTPS/TLS handshakes
- **Packet Filtering**: Implementing efficient filters to capture specific network protocols
- **Scapy Framework**: Mastering Python's premier network manipulation library
- **Container Security**: Working with Docker networking and security capabilities
- **Traffic Analysis**: Extracting meaningful information from network communications

## Technical Environment

### Docker Architecture
The challenge uses a multi-container Docker setup:

- **Alice Container**: Simulates a user browsing the web and making network requests
- **Mallory Container**: Acts as the monitoring station with network analysis capabilities
- **Shared Network**: Custom bridge network (10.0.0.0/28) allowing packet interception

### Container Capabilities
Both containers require elevated privileges:
- `NET_ADMIN`: Network administration (packet capture)
- `SYS_ADMIN`: System administration (advanced networking)

## Challenge Requirements

### Protocol Monitoring
Implement packet filters and processors for:

1. **DNS Queries** (Port 53/UDP)
   - Capture A record queries (qtype=1)
   - Extract queried domain names
   - Record source/destination addresses

2. **HTTP Traffic** (Port 80/TCP)
   - Monitor HTTP requests
   - Extract Host header information
   - Track unencrypted web communications

3. **HTTPS Traffic** (Port 443/TCP)
   - Analyze TLS Client Hello messages
   - Extract Server Name Indication (SNI)
   - Monitor encrypted connection initiation

### Data Structure
Each captured network event should be recorded with:
```json
{
    "src": "source_ip_address",
    "dst": "destination_ip_address", 
    "protocol": "DNS|HTTP|HTTPS",
    "servername": "extracted_server_name"
}
```

## Expected Skills Demonstrated

- **Network Programming**: Understanding of OSI layers and protocol structures
- **Packet Analysis**: Ability to dissect and interpret network protocols
- **Python Development**: Advanced use of Scapy library for network operations
- **Security Monitoring**: Implementing network surveillance capabilities
- **Container Networking**: Working with Docker network interfaces and packet capture

## Challenge Difficulty: Intermediate

This challenge requires solid understanding of:
- Network protocols (TCP/IP, DNS, HTTP, TLS)
- Python programming and library usage
- Container technologies and networking
- Security monitoring concepts
- Packet capture and analysis techniques

The implementation must efficiently filter network traffic and extract meaningful security-relevant information from various protocols, demonstrating practical network security monitoring skills.