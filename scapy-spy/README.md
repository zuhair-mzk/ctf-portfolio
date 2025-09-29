# Scapy Network Monitoring Project

## Project Description

This cybersecurity project demonstrates advanced network packet analysis and monitoring using Scapy, Python's premier network manipulation library. The challenge involves implementing a sophisticated network surveillance system capable of monitoring DNS queries, HTTP requests, and HTTPS connections in a controlled Docker environment.

## Educational Value

### Core Learning Objectives
- **Network Protocol Analysis**: Hands-on experience with DNS, HTTP, and TLS/HTTPS protocols
- **Packet Capture & Filtering**: Implementation of efficient network traffic filtering systems
- **Container Security**: Docker-based network security simulation and monitoring
- **Python Network Programming**: Advanced use of Scapy library for security applications
- **Traffic Analysis**: Extracting security-relevant information from network communications

### Skills Demonstrated
- Network protocol understanding (OSI layers, TCP/IP stack)
- Python advanced programming and library usage
- Container orchestration with Docker Compose
- Security monitoring and incident response techniques
- Data analysis and pattern recognition in network traffic

## Technical Implementation

### Architecture Overview
The project uses a multi-container Docker environment:
- **Alice Container**: Simulates user web browsing behavior
- **Mallory Container**: Implements network monitoring and packet analysis
- **Custom Network**: Isolated bridge network for controlled traffic analysis

### Key Features
- **Multi-Protocol Monitoring**: DNS (port 53), HTTP (port 80), HTTPS (port 443)
- **Real-time Analysis**: Live packet capture and processing
- **Metadata Extraction**: Server names, IP addresses, and protocol information
- **Structured Data Output**: JSON format for further analysis and reporting

### Security Insights
This project highlights important cybersecurity concepts:
- Network traffic surveillance capabilities and limitations
- Metadata leakage in encrypted communications (SNI in HTTPS)
- Privacy implications of network monitoring
- Enterprise security monitoring applications

## Files Structure

- `spy.py` - Main packet analysis implementation using Scapy
- `docker-compose.yml` - Container orchestration configuration
- `script.py` - Traffic analysis and pattern recognition script  
- `test.json` - Sample captured network traffic data
- `challenge.md` - Detailed challenge requirements and learning objectives
- `writeup.md` - Comprehensive technical analysis and implementation details

## Running the Project

1. **Setup Environment**:
   ```bash
   docker-compose up -d
   ```

2. **Execute Monitoring**:
   ```bash
   docker exec -it mallory python3 /shared/spy.py -c 50 /shared/output.json
   ```

3. **Analyze Results**:
   ```bash
   python3 script.py
   ```

## Academic Context

This project is designed for educational cybersecurity training and demonstrates:
- Practical network security monitoring techniques
- Real-world application of Python security libraries
- Container-based security research methodologies
- Ethical considerations in network surveillance

**Note**: This implementation is intended for educational purposes in controlled environments. All monitoring activities should comply with applicable laws and ethical guidelines.

## Future Enhancements

Potential extensions for advanced learning:
- Integration with threat intelligence feeds
- Machine learning-based anomaly detection
- Advanced protocol analysis (SMTP, FTP, SSH)
- Real-time alerting and notification systems
- Integration with SIEM platforms

This project provides a comprehensive foundation for understanding network security monitoring while maintaining strong educational value and practical applicability to real-world cybersecurity scenarios.