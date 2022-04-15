import math

# 0.8 <= alpha <= 0.9
def exponentialCooling(t0, alpha, k):
    return t0 * (alpha ** k)

# alpha > 1
def logarithmicalCooling(t0, alpha, k):
    return t0 / (1 + alpha * math.log(1 + k))

# alpha > 0
def linearCooling(t0, alpha, k):
    return t0 / (1 + alpha * k)

# alpha > 0
def quadraticCooling(t0, alpha, k):
    return t0 / (1 + alpha * (k ** 2))
