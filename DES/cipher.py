from typing import Optional

from table import *

text = 'ABCDEFGH'
key = 'ABCDEFGH'

text = ''.join(map(lambda val: '0' + bin(ord(val))[2:], text))
key = ''.join(map(lambda val: '0' + bin(ord(val))[2:], key))

new_key56 = ''.join(key[i - 1] for i in PC1)

c = new_key56[:28]
d = new_key56[28:]
round_keys = []
for i in SHIFT:
    c = c[i:] + c[:i]
    d = d[i:] + d[:i]
    round_keys.append(''.join((c + d)[j - 1] for j in PC2))

R = text[32:]
L = text[:32]

new_r = ''.join(R[i - 1] for i in E)
print(len(new_r))


def to_binary(data: int | str):
    result = '0'
    if isinstance(data, int):
        result += bin(data)[2:]
    elif isinstance(data, str):
        result += '0'.join(bin(ord(i))[2:] for i in data)
    return result


class FeistelCipher:
    rounds = None
    keys = None
    plaintext = None

    def __init__(self, text: str, key: str):
        chunk = len(to_binary(text)) % 64
        
    def function(self, r_side, round_key):
        pass

    def key_generate(self):
        pass

    def encrypt(self):
        self.keys = self.key_generate()
        for k in range(self.rounds):
            self.function()


def feistel(R, L, func):
    pass
