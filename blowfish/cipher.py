from feistel import BaseFeistelNetwork
from tools import to_binary
from .tables import P, sboxs


class Blowfish(BaseFeistelNetwork):
    rounds = 16

    def key_generation(self, _key: str | None):
        _key = _key.encode()
        keys = [int.from_bytes(_key[i:i + 4]) for i in range(0, len(_key), 4)]
        result = []
        for i in range(self.rounds):
            result.append(P[i] ^ keys[i % len(keys)])
        return result

    def func(self, l_side, round_key):
        l_side = int(l_side, 2)
        tmp = (round_key ^ l_side).to_bytes(4)
        s = tuple(sboxs[i][tmp[i]] for i in range(4))
        result = ((s[0] & s[1]) ^ s[2]) & s[3]
        return to_binary(result)

    def block_encrypt(self, block: str, do_reverse=False):
        return super().block_encrypt(block, True)
