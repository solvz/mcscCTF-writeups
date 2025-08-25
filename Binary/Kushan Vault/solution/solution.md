# Kushan Vault - Writeup

## Challenge Overview

**Category:** Binary Exploitation  
**Flag:** `mcsc{k4n1shk4_th3_gr34t_kush4n_3mp3r0r_50|375|CE}`

This challenge presents a classic stack-based buffer overflow vulnerability in a C program themed around the ancient Kushan Empire. The goal is to bypass authentication and access the treasury vault.

**Note:** The binary in the challenge directory contains the local version of the binary given to the participants, and the binary in the solutions directory contain the hosted version which contains the flag

## Vulnerability Analysis

### The Bug

This program contains **a critical vulnerabilities**:

1. **Buffer Overflow**: The `fgets()` call reads up to 128 bytes into a 64-byte buffer

This can be seen when opening the binary in a reversing tool like ghidra.

### Memory Layout Analysis

In the `vulnerable_function()`, the local variables are allocated on the stack:

- `buffer[64]` - 64 bytes for input
- `comparison[32]` - 32 bytes for comparison (uninitialized)

```
High Address
+----------------+
|  comparison[32]| <- This needs to contain "KANISHKA"
+----------------+
|   buffer[64]   | <- We overflow from here
+----------------+
Low Address
```

`comparison` is located **after** `buffer` on the stack, so we can overflow `buffer` to write into `comparison`.

## Solution Approach

### Step 1: Calculate Offset

To overwrite the `comparison` array, we need to:
1. Fill the entire `buffer[64]` with padding
2. Write "KANISHKA" into the `comparison` array

### Step 2: Craft Payload

```python
payload = b"A" * 64 + b"KANISHKA"
```

This payload:
- Fills `buffer[64]` with 64 'A' characters
- Overwrites `comparison[32]` with "KANISHKA"

## Complete Solution Script

The complete solution is in (`soln.py`).