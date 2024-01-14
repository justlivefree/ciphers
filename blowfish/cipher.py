from feistel import BaseFeistelNetwork
from tables import P, sboxs
from tools import to_binary, bw_xor


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

    def block_encrypt(self, block: str):
        left, right = block[:self.chunk_size], block[self.chunk_size:]
        for i in range(self.rounds):
            save = left
            left = bw_xor(right, self.func(left, self.generated_keys[i]))
            right = save
        return right + left
