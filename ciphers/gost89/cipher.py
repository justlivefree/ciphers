from ciphers.feistel import BaseFeistelNetwork
from ciphers.tools import to_binary, bw_xor, left_shift
from .tables import SBOX


class GOST89(BaseFeistelNetwork):
    rounds = 32
    key_size = 256

    def key_generation(self, key):
        key = to_binary(key)
        keys = [key[i:i + 32] for i in range(0, 256, 32)]
        keys += keys * 2 + keys[::-1]
        return keys

    def func(self, right, round_key):
        tmp = bw_xor(right, round_key)
        result = ''
        for i in range(8):
            idx = int(tmp[i * 4:(i + 1) * 4], 2)
            result += to_binary(SBOX[i][idx], 4)
        result = left_shift(result, 11)
        return result
