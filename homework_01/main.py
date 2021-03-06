"""
Домашнее задание №1
Функции и структуры данных
"""
from time import monotonic
from functools import cache, wraps


def power_numbers(*args) -> list[int]:
    """
    функция, которая принимает N целых чисел,
    и возвращает список квадратов этих чисел
    >>> power_numbers(1, 2, 5, 7)
    <<< [1, 4, 25, 49]
    """
    return [arg ** 2 for arg in args]


def time_it(some_func):
    @wraps(some_func)
    def wrapper(*args, **kwargs):
        start = monotonic()
        res = some_func(*args, **kwargs)
        print(f'Выполнено за {monotonic() - start} секунд')
        return res
    return wrapper


# filter types
ODD = "odd"
EVEN = "even"
PRIME = "prime"


def is_prime2(number: int) -> bool:
    # 0 and 1 is not a prime number
    if number < 2:
        return False
    return True if number < 4 else bool(number % 2) and all(
        (number % i for i in range(3, int(number ** (1 / 2)) + 1, 2)))


# -func = {'... - можно объявить до функции, чтобы не создавать каждый раз заново
# - `not bool(x % 2)` это всё равно что `not x % 2`, но быстрее. в данной ситуации и для odd тоже можно
# без приведения типа, так как в булевом контексте можно не приводить лишний раз тип, оно произойдёт автоматически
# - ключи ('odd', и тд) нужно использовать в виде констант, которые объявлены выше
func = {ODD: lambda x: x % 2,
        EVEN: lambda x: not x % 2,
        PRIME: lambda x: is_prime(x)}


# в 3.9 уже можно вместо ` -> List[int]:` писать ` -> list[int]:` (то есть использовать встроенный list для аннотации, а не импортировать)
def filter_numbers(numbers, filter_name) -> list[int]:
    """
    Функция, которая на вход принимает список из целых чисел,
    и возвращает только чётные/нечётные/простые числа
    (выбор производится передачей дополнительного аргумента)

    >>> filter_numbers([1, 2, 3], ODD)
    <<< [1, 3]
    >>> filter_numbers([2, 3, 4, 5], EVEN)
    <<< [2, 4]
    """
    return list(filter(func[filter_name],numbers))


# is_multiple_3_v2 is better than is_multiple_3_v1
def is_multiple_3_v1(n: int) -> bool:
    return sum(int(digit) for digit in str(n)) % 3 == 0


# is_multiple_2_v2 is better than is_multiple_2_v1
def is_multiple_2_v1(n: int) -> bool:
    return int(str(n)[-1]) % 2 == 0


def is_multiple_3_v2(n: int) -> bool:
    return n % 3 == 0


def is_multiple_2_v2(n: int) -> bool:
    return n % 2 == 0


def is_prime(number: int) -> bool:
    # 0 and 1 is not a prime number
    if number < 2:
        return False
    # 2 and 3 is prime numbers
    if number < 4:
        return True
    if number % 2 == 0 or number % 3 == 0:
        return False
    # 5 + 6k check it
    # 5 + 1 + 6k not a prime /2
    # 5 + 2 + 6k check it
    # 5 + 3 + 6k not a prime /2
    # 5 + 4 + 6k not a prime /3
    # 5 + 5 + 6k not a prime /2
    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6
    return True


# is_prime is better then is_prime1. Why?
@cache
def is_prime1(number: int) -> bool:
    # 0 and 1 is not a prime number
    if number < 2:
        return False
    # 2 and 3 is prime numbers
    if number < 4:
        return True
    if number % 2 == 0 or number % 3 == 0:
        return False
    # 5 + 6k check it
    # 5 + 1 + 6k not a prime /2
    # 5 + 2 + 6k check it
    # 5 + 3 + 6k not a prime /2
    # 5 + 4 + 6k not a prime /3
    # 5 + 5 + 6k not a prime /2
    i = 5
    # now start bruteforce
    # check only prime numbers as divisor
    while i * i <= number:
        if is_prime1(i) and number % i == 0:
            return False
        if is_prime1(i + 2) and number % (i + 2) == 0:
            return False
        i += 6
    return True
