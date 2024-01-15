import concurrent.futures as cf
from abc import ABC, abstractmethod

from tools import bw_xor, bit_mode


class BaseFeistelNetwork(ABC):
    bit_text: str
    generated_keys: tuple | None
    rounds: int = 8
    block_size: int = 64
    chunk_size: int = 32
    key_size: int = 32
    raw_data = {}

    @abstractmethod
    def func(self, r_side, round_key):
        pass

    @abstractmethod
    def key_generation(self, _key: str | None):
        pass

    def block_encrypt(self, block: str, do_reverse=False):
        left, right = block[:self.chunk_size], block[self.chunk_size:]
        a, b = left, right
        if do_reverse:
            a, b = right, left
        for i in range(self.rounds):
            save = b
            b = bw_xor(a, self.func(b, self.generated_keys[i]))
            b = save
        result = a + b if do_reverse else b + a
        return result

    def check_key(self, _key: str):
        if len(_key) != self.key_size:
            raise ValueError(f'error: key is not {self.key_size} bit')

    def _main(self, text: str):
        l = len(text)
        with cf.ThreadPoolExecutor() as executor:
            blocks = (text[i:i + 8] if i + 8 < l else text[i:] for i in range(0, l, 8))
            bit_data = ''.join(executor.map(lambda val: self.block_encrypt(bit_mode(val)), blocks))
        result = ''.join(chr(int(bit_data[i:i + 8], 2)) for i in range(0, len(bit_data), 8))
        return result

    def encrypt(self, plaintext: str, set_key: str):
        self.generated_keys = self.key_generation(_key=set_key)
        return self._main(plaintext)

    def decrypt(self, text: str, set_key: str):
        self.generated_keys = self.key_generation(_key=set_key)[::-1]
        return self._main(text).strip('\x00')
