def to_binary(data: int | str):
    result = ''
    if isinstance(data, int):
        save = bin(data)[2:]
        result += '0' * (8 - len(save)) + save
    elif isinstance(data, str):
        for i in data:
            save = bin(ord(i))[2:]
            result += '0' * (8 - len(save)) + save
    return result


def bw_xor(a: str, b: str):
    x, y = sorted((a, b), key=lambda val: len(val))
    result = ''
    for i in range(1, len(x) + 1):
        result += str(int(x[-i] != y[-i]))
    return y[:len(y) - len(x)] + result[::-1]


def bit_mode(plaintext: str, mode: int = 64):
    b_text = to_binary(plaintext)
    chunk = 0
    if (len_btext := len(b_text)) <= mode:
        chunk = mode - len_btext
    elif len_btext % 64:
        chunk = mode - len_btext % 64
    b_text += '0' * chunk
    return b_text
