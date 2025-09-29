# HTTP Packet Sniffer Challenge

## Challenge Description

This cybersecurity challenge focuses on **network packet analysis and HTTP traffic interception** using Python and Scapy. Participants must implement a sophisticated packet sniffer capable of capturing, filtering, and analyzing HTTP communications in a controlled network environment.

## Objective

Develop a comprehensive HTTP packet sniffer with the following requirements:
1. **Capture HTTP traffic** using Scapy packet manipulation library
2. **Filter HTTP requests and responses** from network traffic
3. **Extract meaningful data** including headers, query parameters, cookies, and body content
4. **Parse and structure data** into JSON format for analysis
5. **Handle both GET and POST requests** with proper parameter extraction
6. **Implement command-line interface** for flexible packet capture operations

## Files Provided

- `sniffer.py` - Main implementation script with packet filtering and processing functions
- `docker-compose.yml` - Docker environment setup with Alice (victim) and Mallory (attacker)
- `sample.json` - Example output format showing expected data structure
- `capture.json` - Sample captured traffic data
- `flag.txt` - Challenge flag to be discovered through packet analysis

## Skills Tested

- **Network Security**: Understanding HTTP protocol vulnerabilities and packet analysis
- **Python Programming**: Advanced use of Scapy library for packet manipulation
- **Traffic Analysis**: Extracting and parsing network communication data
- **JSON Processing**: Structuring captured data into analyzable formats
- **Docker Networking**: Working with containerized network environments
- **Man-in-the-Middle Concepts**: Understanding network interception techniques

## Learning Outcomes

By completing this challenge, you will gain practical experience with:
- Network packet capture and analysis using Scapy
- HTTP protocol internals and security implications
- Python-based network security tool development
- Docker container networking and traffic interception
- Data extraction and parsing from network communications
- Real-world network forensics and monitoring techniques

## Technical Requirements

### Core Implementation
- Use **Scapy library** for packet capture and manipulation
- Implement **packet filtering** to identify HTTP traffic specifically
- Extract **HTTP request details**: method, host, path, query parameters, cookies, body
- Extract **HTTP response details**: status codes, set-cookie headers, response body
- **Parse form data** and query strings from POST and GET requests
- Output results in **structured JSON format** for further analysis

### Network Environment
- **Alice container**: Simulates victim making HTTP requests
- **Mallory container**: Acts as network interceptor running the sniffer
- **Shared network**: Containers communicate over bridge network (10.0.0.0/28)
- **Traffic interception**: Mallory captures Alice's HTTP communications

### Command-Line Interface
```bash
python3 sniffer.py capture.json -c 50
```
- **count parameter**: Number of packets to capture
- **filepath parameter**: Output file for captured data
- **Help option**: Usage instructions and parameter descriptions

## Challenge Scenario

In this scenario, Alice is browsing an e-commerce website over HTTP (unencrypted). Mallory has positioned herself to intercept Alice's network traffic and wants to capture sensitive information including:
- Login credentials submitted via POST requests
- Session cookies and authentication tokens
- Personal information and browsing patterns
- Any other sensitive data transmitted over HTTP

Your task is to implement the packet sniffer that Mallory will use to successfully capture and analyze Alice's HTTP communications.

## Security Implications

This challenge demonstrates several critical cybersecurity concepts:
- **HTTP vulnerabilities**: Why HTTPS is essential for secure communications
- **Network monitoring**: How malicious actors can intercept unencrypted traffic
- **Data exposure**: The risk of transmitting sensitive information over HTTP
- **Defense strategies**: Understanding attack vectors to better implement protections

## Success Criteria

A successful implementation should:
1. Successfully capture HTTP packets from the network interface
2. Correctly filter HTTP requests and responses
3. Extract all relevant data fields accurately
4. Handle both GET requests with query parameters and POST requests with form data
5. Output well-structured JSON data matching the expected format
6. Operate reliably within the Docker container environment
7. Provide meaningful command-line interface for different capture scenarios