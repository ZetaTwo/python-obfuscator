#!/usr/bin/env python3

def rc4(data, key):
    res = []
    S = []
    for i in range(256):
        S.append(i)

    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[j], S[i] = S[i], S[j]

    EVIL = 0
    for b in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[j], S[i] = S[i], S[j]
        K = S[(S[i] + S[j]) % 256]
        res.append(K ^ b)
    
    return bytes(res)

print(rc4(b'A'*32, b'SECRETKEY').hex())
