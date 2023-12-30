from feistel import CoreFeistelNetwork
from tables import PC1, PC2, SHIFT, IP, _IP, E, SBOX, P
from tools import to_binary, left_shift, bw_xor, spilt_chunks


class DESCipher(CoreFeistelNetwork):
    rounds = 16

    def s_boxs(self, get_bits: str):
        result = ''
        _chunks = spilt_chunks(get_bits, 6)
        for i in range(len(_chunks)):
            raw, col = map(lambda val: int(val, 2), (_chunks[i][:2], _chunks[i][2:]))
            result += to_binary(SBOX[i][raw][col])
        return result

    def function(self, r_side, round_key):
        e_table = ''.join(map(lambda val: r_side[val - 1], E))
        to_sbox = bw_xor(e_table, round_key)
        save = self.s_boxs(to_sbox)
        per = ''.join(map(lambda val: save[val - 1], P))
        return per

    def key_generation(self, _key: str, do_reverse: bool = False):
        bit_key = to_binary(_key)
        result = []
        key56 = ''.join(map(lambda val: bit_key[val - 1], PC1))
        cn, dn = key56[:28], key56[28:]
        for r in range(self.rounds):
            cn, dn = left_shift(cn, SHIFT[r]), left_shift(dn, SHIFT[r])
            save = cn + dn
            round_key = ''.join(map(lambda val: save[val - 1], PC2))
            result.append(round_key)
        if do_reverse:
            return tuple(result[::-1])
        return tuple(result)

    def block_encrypt(self, block: str):
        ip = ''.join(map(lambda val: block[val - 1], IP))
        result = super().block_encrypt(ip)
        inverse_ip = ''.join(map(lambda val: result[val - 1], _IP))
        return inverse_ip
