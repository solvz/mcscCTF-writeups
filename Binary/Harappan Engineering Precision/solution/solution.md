# Harappan Engineering Precision - Binary Exploitation Writeup

## Challenge Overview

**Category:** Binary Exploitation  
**Flag:** `mcsc{har4pp4n_w3iGh|s_|fl4g_f0|unD}`

This challenge presents a classic Return-to-Function (ret2func) buffer overflow vulnerability with an information leak. The goal is to exploit a buffer overflow to redirect execution to a function that prints the flag, using a leaked address to bypass ASLR (Address Space Layout Randomization).

## Vulnerability Analysis

### The Vulnerabilities

This program contains two key elements that make exploitation possible:

1. **Information Leak**: The `leak_measurement()` function prints the address of `weight_standard()`
2. **Buffer Overflow**: The `gets()` function in `decode_script()` has no bounds checking

### Memory Layout Understanding

```
Memory Layout (with PIE):
+-----------------+
| harappan_vault  | <- Our target function (randomized base)
+-----------------+
|      ...        |
+-----------------+
| weight_standard | <- Leaked address (randomized base)
+-----------------+
```

Even with PIE enabled, the relative offset between functions remains constant within the same binary. This is why the information leak is crucial - it allows us to calculate the target function's address despite ASLR.

## Solution Approach

### Step 1: Check Binary Security & Find Vulnerabilities

```bash
checksec --file=./precision_measurements
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY
Partial RELRO   No canary found   NX enabled    PIE enabled     No RPATH   No RUNPATH   52 Symbols        No
```

**Key Security Features:**
- **PIE Enabled**: The binary uses Position Independent Executable, meaning base addresses are randomized
- **NX Enabled**: Stack is non-executable (prevents shellcode execution)
- **No Stack Canary**: No stack protection against buffer overflows
- **Partial RELRO**: Some relocation protections, but GOT is still writable

The binary has PIE enabled but no stack canary, making buffer overflow exploitation possible but requiring an information leak to bypass ASLR.

### Step 2: Calculate Function Offset

Use GDB or static analysis to find the relative positions of functions:

```bash
gdb ./precision_measurements
(gdb) info functions
(gdb) print harappan_vault
(gdb) print weight_standard
```

From analysis, the offset between `weight_standard` and `harappan_vault` is 234 bytes:

```python
offset = 234
vault_addr = leaked_addr - offset
```

This means `harappan_vault` is located 234 bytes before `weight_standard` in memory.

### Step 3: Calculate Buffer Overflow Offset

The buffer overflow occurs in the `decode_script()` function:
- `measurement_buffer[64]` is a 64-byte buffer
- We need to overflow this buffer to overwrite the return address
- Through testing/analysis, the return address is overwritten after 72 bytes

#### Stack Frame Analysis

Understanding the stack layout in `decode_script()`:

```
High Address
+----------------+
| Return Address | <- Overwrite this with harappan_vault address
+----------------+
| Saved RBP      | <- 8 bytes
+----------------+
| buffer[64]     | <- 64 bytes of buffer
+----------------+
Low Address
```

Total offset to return address: 64 + 8 = 72 bytes

### Step 4: Craft the Exploit

```python
payload = b'A' * 72 + p64(vault_addr)
```

This payload:
- Fills the 64-byte buffer plus 8 bytes of saved frame pointer
- Overwrites the return address with the address of `harappan_vault()`

## Complete Solution Script

The complete solution is in (`soln.py`).