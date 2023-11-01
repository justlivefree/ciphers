from tools import bw_xor, bit_mode
from random import randint


class FeistelCipher64bit:
    bit_text: str = None
    generated_keys: tuple = None
    rounds: int = 8
    block_size: int = 64
    chunk_size: int = 32

    def function(self, r_side, round_key):
        return bw_xor(r_side, round_key)

    def key_generation(self):
        generated_keys = []
        for i in range(self.rounds):
            round_key = ''.join(str(randint(0, 1)) for _ in range(self.chunk_size))
            generated_keys.append(round_key)
        return tuple(generated_keys)

    def set_keygen(self, set_keys: tuple = None):
        if set_keys:
            for key in set_keys:
                if len(key) < self.chunk_size:
                    raise ValueError(f'error: expect {self.chunk_size} bit key but got {key}')
            return set_keys
        return self.key_generation()

    def block_encrypt(self, block: str):
        left, right = block[:self.chunk_size], block[self.chunk_size:]
        for i in range(self.rounds):
            save = right
            right = bw_xor(left, self.function(right, self.generated_keys[i]))
            left = save
        return right + left

    @property
    def _main(self):
        data = ''
        for i in range(0, len(self.bit_text), self.block_size):
            data += self.block_encrypt(self.bit_text[i:i + self.block_size])
        data = ''.join(chr(int(data[i:i + 8], 2)) for i in range(0, len(data), 8))
        return data

    def encrypt(self, plaintext: str, set_key: tuple = None, rounds: int = None):
        if rounds:
            self.rounds = rounds
        self.generated_keys = self.set_keygen(set_key)
        self.bit_text = bit_mode(plaintext)
        return self._main

    def decrypt(self, plaintext: str, set_key=None, rounds: int = None):
        reverse_key = tuple(reversed(set_key))
        plaintext = self.encrypt(plaintext, reverse_key, rounds).strip('\x00')
        return plaintext
