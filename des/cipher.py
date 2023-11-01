from feistel import FeistelCipher64bit
from tools import to_binary, bit_mode, left_shift, bw_xor, spilt_chunks
from table import PC1, PC2, SHIFT, IP, _IP, E, SBOX, P


class DESCipher64bit(FeistelCipher64bit):
    main_key: str = None

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

    def key_generation(self, _reverse: bool = False):
        result = []
        key56 = ''.join(map(lambda val: self.main_key[val - 1], PC1))
        cn, dn = key56[:28], key56[28:]
        for r in range(self.rounds):
            cn, dn = left_shift(cn, SHIFT[r]), left_shift(dn, SHIFT[r])
            save = cn + dn
            round_key = ''.join(map(lambda val: save[val - 1], PC2))
            result.append(round_key)
        if _reverse:
            return tuple(reversed(result))
        return tuple(result)

    def block_encrypt(self, block: str):
        ip = ''.join(map(lambda val: block[val - 1], IP))
        result = super().block_encrypt(ip)
        inverse_ip = ''.join(map(lambda val: result[val - 1], _IP))
        return inverse_ip

    def encrypt(self, **kwargs):
        plaintext, set_key = kwargs['plaintext'], kwargs['set_key']
        if len(_key_bit := to_binary(set_key)) == 64:
            self.rounds = 16
            self.main_key = _key_bit
            self.generated_keys = self.key_generation(_reverse=kwargs.get('decrypt', False))
            self.bit_text = bit_mode(plaintext)
            return self._main
        raise ValueError(f'error: key must be 64 bit. but got {len(to_binary(set_key))}')

    def decrypt(self, **kwargs):
        kwargs['decrypt'] = True
        return self.encrypt(**kwargs).rstrip('\x00')
