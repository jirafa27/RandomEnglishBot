import string
from random import random


def generate_random_string(l: int) -> str:
    """
    Возвращает случайную строку длиной l,
    состоящую из букв (a-z, A-Z) и цифр.
    """
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choices(alphabet, k=l))
