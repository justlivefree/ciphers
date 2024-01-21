from ciphers.feistel import BaseFeistelNetwork
from ciphers.tools import to_binary, left_shift, bw_xor, spilt_chunks
from .tables import PC1, PC2, SHIFT, IP, _IP, E, SBOX, P


class DES(BaseFeistelNetwork):
    rounds = 16
    key_size = 64  # actual key size is 56 bit

    @staticmethod
    def __pack(text, table):
        return ''.join(map(lambda val: text[val - 1], table))

    @staticmethod
    def __sboxs(get_bits: str):
        result = ''
        chunks = spilt_chunks(get_bits, 6)
        for i in range(len(chunks)):
            raw, col = map(lambda val: int(val, 2), (chunks[i][:2], chunks[i][2:]))
            result += to_binary(SBOX[i][raw][col])
        return result

    def key_generation(self, key):
        key, result = to_binary(key), []
        key56 = self.__pack(key, PC1)
        cn, dn = key56[:28], key56[28:]
        for r in range(self.rounds):
            cn, dn = left_shift(cn, SHIFT[r]), left_shift(dn, SHIFT[r])
            round_key = self.__pack(cn + dn, PC2)
            result.append(round_key)
        return result

    def func(self, r_side, round_key):
        e_table = self.__pack(r_side, E)
        tmp = self.__sboxs(bw_xor(e_table, round_key, 48))
        return self.__pack(tmp, P)

    def block_encrypt(self, block: str, **kwargs):
        block = self.__pack(block, IP)
        result = super().block_encrypt(block)
        return self.__pack(result, _IP)
