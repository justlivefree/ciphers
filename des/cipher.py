from feistel import FeistelCipher64bit
from tools import to_binary, bit_mode


class DESCipher64bit(FeistelCipher64bit):
    main_key: str = None

    def function(self, r_side, round_key):
        pass

    def des_key_check(self, _key: str):
        return

    def key_generation(self, _key: str = None):
        return ()

    def set_keygen(self, set_keys: tuple = None):
        return set_keys

    def encrypt(self, plaintext: str, set_key: str = None, rounds=None):
        if val := to_binary(set_key) != 64:
            raise ValueError(f'error: key must be 64 bit. but got {val}')
        self.rounds = 16
        self.generated_keys = self.key_generation(set_key)
        self.bit_text = bit_mode(plaintext)
        return self._main
