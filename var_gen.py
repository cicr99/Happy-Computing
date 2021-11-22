import math
import random as r
from typing import List
from utils import lower_bound

# method of inversion of the distribution function
def df_inversion(prob_list: List[float]):
    probs = sorted([(p, i + 1) for i, p in enumerate(prob_list)], reverse=True)
    acum = [p for (p, _) in probs]
    for i in range(1, len(acum)):
        acum[i] += acum[i - 1]
    
    u = r.random()
    pos = lower_bound(acum, u)
    return probs[pos][1]

# poisson distribution
def poisson(_lambda) -> int:
    u = r.random()
    n = 0

    val = math.exp(-_lambda)
    while u >= val:
        u *= r.random()
        n += 1

    return n

# exponential distribution
def exponential(_lambda) -> float:
    u = r.random()
    x = (-1 / _lambda) * math.log(u)
    return x

# normal distribution
def normal(mean, variance) -> float:
    y = exponential(1)
    u = r.random()
    sd = math.sqrt(variance)

    if u <= math.exp(-math.pow(y - 1, 2) / 2):
        return y * sd + mean

    return normal(mean, variance)
