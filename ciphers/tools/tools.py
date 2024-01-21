import math


def to_binary(data: int | str, mode=8):
    result = ''
    if isinstance(data, int):
        result = bit_mode(bin(data)[2:], mode)
    elif isinstance(data, str):
        for i in data:
            result += bit_mode(bin(ord(i))[2:], mode)
    return result


def bw_xor(a: str | int, b: str | int, mode: int = 32):
    if isinstance(a, str):
        a = int(a, 2)
    if isinstance(b, str):
        b = int(b, 2)
    return bit_mode(bin(a ^ b)[2:], mode)


def bit_mode(text: str, mode: int = 64):
    chunk = 0
    if (len_btext := len(text)) <= mode:
        chunk = mode - len_btext
    elif len_btext % mode:
        chunk = mode - len_btext % mode
    text = '0' * chunk + text
    return text


def left_shift(bin_num: str, shift: int) -> str:
    if shift < 0:
        raise Exception('Shift must be positive')
    return bin_num[-shift:] + bin_num[:-shift]


def left_rotation(num, shift):
    return (num << shift & 0xffffffff) | num >> (32 - shift)


def spilt_chunks(text: str, size: int):
    _len = len(text)
    result = [text[i:i + size] if i + size < _len else text[i:] for i in range(0, _len, size)]
    return result


def euler_phi(n: int):
    result = map(lambda val: math.gcd(val, n) == 1, range(1, n))
    return sum(result)


def euclid_gcd(a: int, b: int):
    if a < b:
        a, b = b, a
    while a % b:
        a, b = b, a % b
    return b


def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = extended_gcd(b, a % b)
        return d, y, x - (a // b) * y


def mod_inverse(a, m):
    d, x, y = extended_gcd(a, m)
    if d != 1:
        raise ValueError("Inverse does not exist")
    else:
        return x % m
