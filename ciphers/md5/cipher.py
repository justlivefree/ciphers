import math

from ciphers.tools import left_rotation


class MD5:
    A: int = 0x67452301
    B: int = 0xefcdab89
    C: int = 0x98badcfe
    D: int = 0x10325476

    def F1(self, B, C, D):
        return (B & C) | (~B & D)

    def F2(self, B, C, D):
        return (B & D) | (~D & C)

    def F3(self, B, C, D):
        return B ^ C ^ D

    def F4(self, B, C, D):
        return C ^ (B | ~D)

    keys = (0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
            0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
            0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
            0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
            0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
            0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
            0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
            0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
            0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
            0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
            0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
            0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
            0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
            0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
            0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
            0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391)

    def __key_generate(self) -> None:
        keys = []
        for i in range(64):
            keys.append(int(abs(math.sin(i + 1)) * 2 ** 32))
        self.keys = tuple(keys)

    def __get_round_messages(self, message: bytes) -> tuple[int, ...]:
        chunks = []
        for i in range(0, 64, 4):
            chunks.append(message[i:i + 4])
        round_messages = []
        round_index_functions = (
            lambda val: val,
            lambda val: (5 * val + 1) % 16,
            lambda val: (3 * val + 5) % 16,
            lambda val: (7 * val) % 16
        )

        for func in round_index_functions:
            for i in range(16):
                round_messages.append(int.from_bytes(chunks[func(i)]))

        return tuple(round_messages)

    def __main_process(self, text: bytes) -> str:
        # padding
        bits_len = 8 * len(text) & 0xffffffffffffffff
        res = len(text) % 64
        padding_size = (55 - res) if res <= 55 else (119 - res)
        result = text + b'\x80' + b'\x00' * padding_size + bits_len.to_bytes(8)

        # initialize variables and functions
        a, b, c, d = (self.A, self.B, self.C, self.D)
        functions = (self.F1, self.F2, self.F3, self.F4)

        # process
        for i in range(0, len(result), 64):
            messages = self.__get_round_messages(result[i:i + 64])
            for rnd, func in enumerate(functions):
                for j in range(16):
                    index = j + (rnd - 1) * 16
                    save = b
                    b = a + func(b, c, d) + messages[index] + self.keys[index]
                    b = (left_rotation(b, [7, 12, 17, 22][index // 16]) + save) & 0xFFFFFFFF
                    a, d, c = d, c, save
            a = (self.A + a) & 0xffffffff
            b = (self.B + b) & 0xffffffff
            c = (self.C + c) & 0xffffffff
            d = (self.D + d) & 0xffffffff

        result = ''.join(f'{x:08x}' for x in (a, b, c, d))
        return result

    def encrypt(self, plaintext: str) -> str:
        text = plaintext.encode('utf-8')
        return self.__main_process(text)

    def compare(self, text: str, hash_value: str):
        return self.encrypt(text) == hash_value
