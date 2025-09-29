# Adjacent Memory Shellcode Challenge

## Challenge Description

This cybersecurity challenge focuses on **buffer overflow exploitation** in a vulnerable C program. Participants must identify and exploit memory safety vulnerabilities to execute shellcode and demonstrate complete control over program execution.

## Objective

Exploit the buffer overflow vulnerability in the provided C program to:
1. Gain control of program execution flow
2. Execute shellcode to read a target file from the system
3. Successfully demonstrate the exploitation technique

## Files Provided

- `vuln.c` - Vulnerable C program with buffer overflow
- `exploit.py` - Complete exploitation script
- `shellcode.py` - Shellcode generation utilities

## Skills Tested

- **Binary Exploitation**: Understanding stack-based buffer overflows
- **Memory Layout**: Stack frame analysis and address calculation  
- **Shellcode Development**: Crafting and deploying execution payloads
- **Dynamic Analysis**: Using crash dumps for exploitation
- **Python Scripting**: Automating exploitation with pwntools

## Learning Outcomes

By completing this challenge, you will gain practical experience with:
- Classical buffer overflow exploitation techniques
- Memory safety vulnerabilities in C programs
- Stack layout manipulation and return address overwriting
- Shellcode injection and execution
- Using debugging tools for vulnerability analysis

## Difficulty Level

**Intermediate** - Requires understanding of:
- C programming and memory management
- Assembly language basics
- Stack-based exploitation techniques
- Python and pwntools framework

## Educational Purpose

This challenge is designed to teach defensive programming by demonstrating the consequences of memory safety vulnerabilities. Always practice ethical hacking and use these skills responsibly for defensive security purposes.