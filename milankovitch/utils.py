import math


def next_power_of_2(x):
    """Compute the smallest power of 2 greater than or equal to x."""
    return 1 if x == 0 else math.ceil(math.log2(x))
