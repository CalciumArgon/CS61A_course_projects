import math as m
def is_prime(x):
    mid = m.floor(m.sqrt(x)) + 1
    for i in range(2, mid):
        if x % i == 0:
            return False
    return True
# print(is_prime(2017)) # True
def prime(n):
    ans = list(range(n+1))
    for factor in ans[2:]:
        if factor != -1:
            for j in range(2*factor, n+1, factor):
                ans[j] = -1
    ans = [num for num in ans
                    if num != -1][2:]
    return ans
# print(prime(2021)[305]) # 2017

'''--------------------------------------------------------------------------'''

def twenty_twenty_one():
    """Come up with the most creative expression that evaluates to 2021,
    using only numbers and the +, *, and - operators.

    >>> twenty_twenty_one()
    2021
    """
    return prime(2021)[305] + 4

print(twenty_twenty_one())

'''--------------------------------------------------------------------------'''
