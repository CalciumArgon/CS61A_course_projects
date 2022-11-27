def falling(n, k):
    """Compute the falling factorial of n to depth k."""
    if k == 0:
        return 1
    if k == 1:
        return n
    return n * falling(n-1, k-1)


def sum_digits(y):
    """Sum all the digits of y."""
    if y // 10 == 0:
        return y
    return (y%10) + sum_digits(y//10)


def double_eights(n):
    """Return true if n has two eights in a row.
    >>> double_eights(2882)
    True
    >>> double_eights(880088)
    True
    >>> double_eights(80808080)
    False
    """
    flag = 0        # 要用来记录是否出现过88的判定
    while n // 10 != 0:
        if n % 10 == 8:
            flag = 1
            if (n//10) % 10 != 8:
                return False
            else:
                n //= 100
        else:
            n //= 10
    return True if flag == 1 else False     # flag=0说明从始至终未出现过88的判定, 即使未违反单8规则也是False
