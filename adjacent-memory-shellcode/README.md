# Adjacent Memory Shellcode Challenge

**Challenge Type:** Binary Exploitation | **Difficulty:** Intermediate | **Status:** ✅ SOLVED

## Overview

This challenge demonstrates classical **buffer overflow exploitation** techniques against a vulnerable C program. The goal is to exploit memory safety vulnerabilities to execute shellcode and gain control of program execution flow.

## Challenge Structure

This folder contains all the necessary files for the Adjacent Memory Shellcode challenge:

- **`vuln.c`** - Vulnerable C program with buffer overflow
- **`exploit.py`** - Working exploitation script 
- **`shellcode.py`** - Shellcode generation utilities
- **`challenge.md`** - Challenge description and objectives
- **`writeup.md`** - Technical analysis and solution methodology

## Technical Skills Demonstrated

- **Memory Layout Analysis**: Understanding stack frames and buffer placement
- **Dynamic Exploitation**: Using crash analysis for address calculation
- **Shellcode Injection**: Crafting and deploying executable payloads  
- **Binary Exploitation**: Classic return address overwriting techniques
- **Python Automation**: Using pwntools for exploitation scripting

## Key Learning Outcomes

This challenge provides hands-on experience with:

1. **Vulnerability Research**: Identifying buffer overflow conditions in C code
2. **Exploit Development**: Building reliable exploitation payloads  
3. **Memory Management**: Understanding the criticality of bounds checking
4. **Security Tools**: Leveraging debugging and analysis frameworks
5. **Payload Engineering**: Constructing shellcode with NOP sleds for reliability

## Challenge Objective

Successfully exploit the buffer overflow vulnerability to:
1. Gain control of program execution flow
2. Execute shellcode to read a target file
3. Demonstrate complete understanding of the exploitation process

---

*This challenge is part of my cybersecurity portfolio demonstrating practical binary exploitation skills and secure coding awareness.*