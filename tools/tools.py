def to_binary(data: int | str):
    result = ''
    if isinstance(data, int):
        result = bin(data)
        result = result[result.index('b') + 1:]
        # result += '0' * (8 - len(save)) + save
    elif isinstance(data, str):
        for i in data:
            save = bin(ord(i))[2:]
            result += '0' * (8 - len(save)) + save
    return result


def bw_xor(a: str | int, b: str | int):
    a = to_binary(a) if isinstance(a, int) else a
    b = to_binary(b) if isinstance(b, int) else b
    x, y = sorted((a, b), key=lambda val: len(val))
    result = ''
    for i in range(1, len(x) + 1):
        result += str(int(x[-i] != y[-i]))
    s = y[:len(y) - len(x)] + result[::-1]
    # if s[0] == 'b':
    #     print(a, b)
    #     print(len(s[1:]))
    #     return s[1:]
    return s


def bit_mode(plaintext: str | int, mode: int = 64):
    b_text = to_binary(plaintext)
    chunk = 0
    if (len_btext := len(b_text)) <= mode:
        chunk = mode - len_btext
    elif len_btext % mode:
        chunk = mode - len_btext % mode
    b_text += '0' * chunk
    return b_text


def left_shift(text: str, shift: int) -> str:
    for _ in range(shift):
        text = text[-1] + text[:-1]
    if text[1] == 'b':
        print('left shift')
        print(text)
    return text


def left_rotation(num, shift):
    return (num << shift & 0xffffffff) | num >> (32 - shift)


def spilt_chunks(text: str, size: int):
    _len = len(text)
    result = [text[i:i + size] if i + size < _len else text[i:] for i in range(0, _len, size)]
    return result
