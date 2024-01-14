import random


def miller_rabin_test(num: int, k: int = 5) -> bool:
    # for optimizing
    if num <= 1:
        return False
    if num in (2, 3, 5, 7):
        return True
    if 0 in (num % 2, num % 3, num % 5, num % 7):
        return False

    r, d = 0, num - 1
    while ~d & 1:
        r += 1
        d >>= 1

    for _ in range(k):
        a = random.randint(2, num - 1)
        b = pow(a, d, num)
        if b in (1, num - 1):
            continue
        for _ in range(r):
            b = pow(b, 2, num)
            if b == num - 1:
                break
        else:
            return False
    return True
