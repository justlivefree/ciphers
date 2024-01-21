import base64
import concurrent.futures as cf
from abc import ABC, abstractmethod

from ciphers.tools import bw_xor, bit_mode, to_binary


class BaseFeistelNetwork(ABC):
    rounds: int = 8
    block_size: int = 64
    key_size: int = 32
    generated_keys: tuple | None

    @abstractmethod
    def key_generation(self, key):
        pass

    @abstractmethod
    def func(self, r_side, round_key):
        pass

    def block_encrypt(self, block: str, **kwargs):
        chunk_size = self.block_size // 2
        left, right = block[:chunk_size], block[chunk_size:]
        for i in range(self.rounds):
            save = right
            right = bw_xor(left, self.func(right, self.generated_keys[i]))
            left = save
        return right + left

    def check_key(self, set_key: str):
        if len(set_key) != self.key_size:
            raise Exception(f'error: must be {self.key_size} bit')

    def _main(self, text: str, **kwargs):
        def block_func(val):
            block_data = self.block_encrypt(bit_mode(to_binary(val), self.block_size), **kwargs)
            return int(block_data, 2).to_bytes(8).strip(b'\x00')

        l = len(text)
        with cf.ThreadPoolExecutor() as executor:
            blocks = (text[i:i + 8] if i + 8 < l else text[i:] for i in range(0, l, 8))
            result = b''.join(executor.map(block_func, blocks))
        return result

    def encrypt(self, plaintext: str, set_key: str):
        self.check_key(to_binary(set_key))
        self.generated_keys = self.key_generation(set_key)
        return base64.b64encode(self._main(plaintext)).decode()

    def decrypt(self, text: str, set_key: str):
        text = base64.b64decode(text.encode()).decode('latin-1')
        self.generated_keys = self.key_generation(key=set_key)[::-1]
        return self._main(text, dc_mode=True).decode()
