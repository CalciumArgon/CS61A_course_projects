HW_SOURCE_FILE = __file__


def num_eights(x):
    """Returns the number of times 8 appears as a digit of x.

    >>> num_eights(3)
    0
    >>> num_eights(8)
    1
    >>> num_eights(88888888)
    8
    >>> num_eights(2638)
    1
    >>> num_eights(86380)
    2
    >>> num_eights(12345)
    0
    >>> from construct_check import check
    >>> # ban all assignment statements
    >>> check(HW_SOURCE_FILE, 'num_eights',
    ...       ['Assign', 'AugAssign'])
    True
    """
    if x <= 10:
        return 0 if x != 8 else 1
    return num_eights(x // 10) + num_eights(x % 10)


# from functools import lru_cache
# @lru_cache(maxsize=1000000000)
def pingpong(n):
    """Return the nth element of the ping-pong sequence.

    >>> pingpong(8)
    8
    >>> pingpong(10)
    6
    >>> pingpong(15)
    1
    >>> pingpong(21)
    -1
    >>> pingpong(22)
    -2
    >>> pingpong(30)
    -2
    >>> pingpong(68)
    0
    >>> pingpong(69)
    -1
    >>> pingpong(80)
    0
    >>> pingpong(81)
    1
    >>> pingpong(82)
    0
    >>> pingpong(100)
    -6
    >>> from construct_check import check
    >>> # ban assignment statements
    >>> check(HW_SOURCE_FILE, 'pingpong', ['Assign', 'AugAssign'])
    True
    """
    def evaluate(i, acc, p):
        while i < n:
            if (i+1) % 8 == 0 or num_eights(i+1):
                return evaluate(i + 1, acc + p, -p)
            else:
                return evaluate(i + 1, acc + p, p)
        return acc
    return evaluate(1, 1, 1)

    # # 不用 functools.lru.cache() 就会超时
    # if n <= 8: 
    #     return n
    # if (n-1) % 8 == 0 or num_eights(n-1):
    #     return pingpong(n-2)
    # else:
    #     return pingpong(n-1) * 2 - pingpong(n-2)


def missing_digits(n):
    """Given a number a that is in sorted, increasing order,
    return the number of missing digits in n. A missing digit is
    a number between the first and last digit of a that is not in n.
    >>> missing_digits(1248) # 3, 5, 6, 7
    4
    >>> missing_digits(19) # 2, 3, 4, 5, 6, 7, 8
    7
    >>> missing_digits(1122) # No missing numbers
    0
    >>> missing_digits(123456) # No missing numbers
    0
    >>> missing_digits(3558) # 4, 6, 7
    3
    >>> missing_digits(35578) # 4, 6
    2
    >>> missing_digits(12456) # 3
    1
    >>> missing_digits(16789) # 2, 3, 4, 5
    4
    
    >>> missing_digits(4) # No missing numbers between 4 and 4
    0
    >>> from construct_check import check
    >>> # ban while or for loops
    >>> check(HW_SOURCE_FILE, 'missing_digits', ['While', 'For'])
    True
    """
    if n < 10 :
        return 0

    if n%10 in ((n//10)%10, (n//10)%10 - 1):
        return missing_digits(n // 10)
    else:
        return missing_digits(n // 10) + (n%10 - (n//10)%10 - 1)


# ===== Solve deviding number problem first ===== #
def count_by_m(num, m):
    """
    Count num by a start with m
    """
    if m == 1:
        return 1
    if m == num:
        return 1 + count_by_m(num, m - 1)
    if m > num:
        return 0 + count_by_m(num, m - 1)
    return count_by_m(num - m, m) + count_by_m(num, m - 1)
# print(count_by_m(4, 2))
# print(count_by_m(4, 4))
# =============================================== #

def get_next_coin(coin):
    """Return the next coin. 
    >>> get_next_coin(1)
    5
    >>> get_next_coin(5)
    10
    >>> get_next_coin(10)
    25
    >>> get_next_coin(2) # Other values return None
    """
    if coin == 25:
        return 10
    elif coin == 10:
        return 5
    elif coin == 5:
        return 1


def count_coins(change):
    """Return the number of ways to make change using coins of value of 1, 5, 10, 25.
    >>> count_coins(15)
    6
    >>> count_coins(10)
    4
    >>> count_coins(20)
    9
    >>> count_coins(100) # How many ways to make change for a dollar?
    242
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(HW_SOURCE_FILE, 'count_coins', ['While', 'For'])                                          
    True
    """
    def devide(part, largest):
        if largest == 1:
            return 1
        elif largest > part:
            return devide(part, get_next_coin(largest)) + 0
        if largest == part:
            return devide(part, get_next_coin(largest)) + 1
        return devide(part, get_next_coin(largest)) + devide(part-largest, largest)
    return devide(change, 25)



from operator import sub, mul

def make_anonymous_factorial():
    """Return the value of an expression that computes factorial.

    >>> make_anonymous_factorial()(5)
    120
    >>> from construct_check import check
    >>> # ban any assignments or recursion
    >>> check(HW_SOURCE_FILE, 'make_anonymous_factorial', ['Assign', 'AugAssign', 'FunctionDef', 'Recursion'])
    True
    """
    # The following expressions need '=' assignment, and still rely on the name 'factorial'
    # factorial = lambda x: 1 if x == 1 else x * factorial(x - 1)
    # factorial = lambda x: 1 if x == 1 else mul(x, factorial(sub(x, 1)))
    
    # 需要递归时, 就再调用一次make_anonymous_factorial()重新生成递归函数
    # But the following expressions need 'recursion' which is banned
    # return lambda n: reduce(lambda x, y: x * y, range(1, n+1), 1)

    # 正确的做法: Y-combinator 使 lambda 函数也可以调用
    return lambda n: (lambda f: f(f, n))(lambda g, x: 1 if x == 0 else x * g(g, x-1))


def print_move(origin, destination):
    """Print instructions to move a disk."""
    print("Move the top disk from rod", origin, "to rod", destination)


def move_stack(n, start, end):
    """Print the moves required to move n disks on the start pole to the end
    pole without violating the rules of Towers of Hanoi.

    n -- number of disks
    start -- a pole position, either 1, 2, or 3
    end -- a pole position, either 1, 2, or 3

    There are exactly three poles, and start and end must be different. Assume
    that the start pole has at least n disks of increasing size, and the end
    pole is either empty or has a top disk larger than the top n start disks.

    >>> move_stack(1, 1, 3)
    Move the top disk from rod 1 to rod 3
    >>> move_stack(2, 1, 3)
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 3
    >>> move_stack(3, 1, 3)
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 3 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 1
    Move the top disk from rod 2 to rod 3
    Move the top disk from rod 1 to rod 3
    """
    assert 1 <= start <= 3 and 1 <= end <= 3 and start != end, "Bad start/end"
    if n == 1:
        print_move(start, end)
        return
    move_stack(n-1, start, 6-(start+end))
    print_move(start, end)
    move_stack(n-1, 6-(start+end), end)
    return
