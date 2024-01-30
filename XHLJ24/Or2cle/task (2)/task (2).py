from Crypto.Util.number import *
from hashlib import *
import os
from Crypto.Cipher import AES
from Crypto.Util import Counter
from random import *
import socket
import threading
import base64

FLAG = b'fake_flag'

class Proof():
    def S(self,n):
        factors = set()
        while n % 2 == 0:
            factors.add(2)
            n //= 2
        for i in range(3, int(n**0.5) + 1, 2):
            while n % i == 0:
                factors.add(i)
                n //= i
        if n > 2:
            factors.add(n)
        
        return factors

    def Y(self,n):
        if n == 1:
            return 1

        result = n
        for p in self.S(n):
            result *= (1 - 1 / p)
        return int(result)


    def proof(self,n):
        res = 0
        for m in range(1, n+1):
            for l in range(1, m+1):
                for k in range(1, l+1):
                    for j in range(1, k+1):
                        for i in range(1, j+1):
                            for h in range(1, i+1):
                                for g in range(1, h+1):
                                    for f in range(1, g+1):
                                        for e in range(1, f+1):
                                            for d in range(1, e+1):
                                                for c in range(1, d+1):
                                                    for b in range(1, c+1):
                                                        for a in range(1, b+1):
                                                            res +=  b//a*(self.Y(a)) # Euler function 
        return res


class Harukii_Oracle:

    def __init__(self,key):
        self.k  = key

    def pad(self, plaintext):
        block_size = randint(1,len(plaintext)-1)
        if len(plaintext) <  block_size :
            return plaintext
        else:
            padding_length = len(plaintext) // 16
            padding_byets = bytes([padding_length])
            plaintext = plaintext.replace(padding_byets,b"\x00")
            p = plaintext[:16]
            for i in range(1 , padding_length+1):
                p += padding_byets + plaintext[16*i:16*(i+1)]
            return p

    def encrypt(self,plaintext):
        aes = AES.new(self.k,mode=AES.MODE_CTR,counter=Counter.new(128))
        chipertext = aes.encrypt(self.pad(plaintext))
        return chipertext
    
    def gift(self,ciphertext):
        aes = AES.new(self.k,mode=AES.MODE_CTR,counter=Counter.new(128))
        plaintext = aes.decrypt(ciphertext)
        padding_length = len(plaintext) // 16
        padding_bytes = bytes([padding_length])
        return plaintext.count(padding_bytes) == padding_length
        

Menu = """
1. get flag
2. gift
3. exit
"""

def task(client_socket):
    client_socket.settimeout(3600)
    s = str((getPrime(128)))
    client_socket.send(f"s : {s}\n".encode())
    client_socket.send("Give me a hash: ".encode())
    hash = client_socket.recv(1024)[:-1]
    hash = int(hash,16)
    '''if hash != int(sha256(str(Proof.proof(s)).encode()).hexdigest(),16):
        client_socket.send(": C".encode())
        exit(-1)'''
    key = randbytes(16)
    YSGS = Harukii_Oracle(key=key)
    while True:
        try:
            client_socket.send(Menu.encode())
            choice = client_socket.recv(1024).decode().strip()
            if choice == '1' :
                enc_flag = base64.b64encode(YSGS.encrypt(FLAG))
                client_socket.send(f"This is Your flag {enc_flag}".encode())
            elif choice == '2':
                c = client_socket.recv(1024)[:-1]
                if YSGS.gift(c):
                    client_socket.send("Dec successfully".encode())
                else:
                    client_socket.send("Dec faild".encode())

            else:
                exit(-1)
        except Exception as e:
            print(e)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(100)
    
    try:
        while True:
            client_sock, address = server.accept()
            
            print(f"Accepted connection from {address[0]}:{address[1]}")
            client_handler = threading.Thread(target=task, args=(client_sock,))
            client_handler.start()
    finally:
        server.close()

if __name__ == "__main__":
    main()
