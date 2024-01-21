import base64

from ciphers.prime.generators import miller_rabin_generator
from .tools import mod_inverse


class RSA:

    def __init__(self, p: int = None, q: int = None, e: int = None, number_of_digits=20):
        if p is None:
            p = miller_rabin_generator(number_of_digits)
        if q is None:
            q = miller_rabin_generator(number_of_digits)
        ttn = (p - 1) * (q - 1)
        if e is None:
            e = ttn - 1
        self.n = p * q
        self.e = e
        self.d = mod_inverse(e, ttn)

    def encrypt(self, plaintext: str):
        def enc(val: int):
            val = pow(val, self.e, self.n)
            return hex(val)[2:].encode()

        arr = map(ord, plaintext)
        result = b':'.join(map(enc, arr))
        return base64.b64encode(result)

    def decrypt(self, text: bytes):
        def dec(val: bytes):
            val = int(val.decode(), 16)
            return chr(pow(val, self.d, self.n))

        text = base64.b64decode(text)
        result = ''.join(map(dec, text.split(b':')))
        return result
