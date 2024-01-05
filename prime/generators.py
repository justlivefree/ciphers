import random
from prime.tests import miller_rabin_test


def sieve_of_erts(n: int) -> tuple[int, ...]:
    """
    TODO: optimize
    """
    n += 1
    try:
        from numpy import int8, ones
        nums = ones(shape=n, dtype=int8)
    except ImportError:
        nums = [1] * n

    i = 2
    while i * i <= n:
        if nums[i]:
            for j in range(i * i, n, i):
                nums[j] = 0
        i += 1
    nums[0], nums[1] = 0, 0
    result = tuple(num for num, is_prime in enumerate(nums) if is_prime)
    return result


def sieve_of_atkin(n: int) -> tuple[int, ...]:
    """
    TODO: optimize
    """
    if n <= 1:
        return ()

    try:
        from numpy import int8, zeros
        nums = zeros(shape=(n + 1), dtype=int8)
    except ImportError:
        nums = [0] * (n + 1)

    s1 = (1, 13, 17, 29, 37, 41, 49, 53)
    s2 = (7, 19, 31, 43)
    s3 = (11, 23, 47, 59)

    def check(val, limit, sn):
        return val <= limit and (val % 60 in sn or val == 5)

    x = 1
    while x * x <= n:
        y = 1
        while y * y <= n:
            z = 4 * x * x + y * y
            if check(z, n, s1) and z & 1:
                nums[z] ^= 1

            z = 3 * x * x + y * y
            if check(z, n, s2):
                nums[z] ^= 1

            z = 3 * x * x - y * y
            if check(z, n, s3) and x > y:
                nums[z] ^= 1
            y += 1
        x += 1

    for i in range(5, int(n ** 0.5) + 1):
        if nums[i]:
            for k in range(i ** 2, n + 1, i ** 2):
                nums[k] = 0

    nums[0], nums[1] = 0, 0
    result = tuple(num for num, is_prime in enumerate(nums) if is_prime)

    return 2, 3, *result


def miller_rabin_generator(n: int) -> int:
    """
    Generator based on Miller-Rabin test
    :param n: number of digits
    :return: prime number
    """
    start = 10 ** (n - 1)
    stop = 10 ** n

    while True:
        random_number = random.randint(start, stop)
        if miller_rabin_test(random_number):
            return random_number
