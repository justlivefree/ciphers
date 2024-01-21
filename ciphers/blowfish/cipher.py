from ciphers.feistel import BaseFeistelNetwork
from ciphers.tools import bw_xor, to_binary
from .tables import P, sboxs


class Blowfish(BaseFeistelNetwork):
    rounds = 16

    def key_generation(self, key):
        key, result = key.encode(), []
        keys = [int.from_bytes(key[i:i + 4]) for i in range(0, len(key), 4)]
        for i in range(self.rounds):
            result.append(P[i] ^ keys[i % len(keys)])
        return result

    def func(self, l_side, round_key):
        l_side = int(l_side, 2)
        tmp = (round_key ^ l_side).to_bytes(40)
        s = tuple(sboxs[i][tmp[i]] for i in range(4))
        result = ((s[0] & s[1]) ^ s[2]) & s[3]
        return to_binary(result)

    def check_key(self, set_key: str):
        if not (32 <= len(set_key) <= 448):
            raise Exception(f'error: key bit length out of range')

    def block_encrypt(self, block: str, **kwargs):
        left, right, p_array = block[:32], block[32:], P[:16]
        p17, p18 = map(to_binary, P[16:18])
        if kwargs.get('dc_mode'):
            p_array = p_array[::-1]
        for i in range(self.rounds):
            right = bw_xor(right, self.func(left, self.generated_keys[i]))
            left = bw_xor(left, to_binary(p_array[i]))
        return bw_xor(left, p18) + bw_xor(right, p17)
