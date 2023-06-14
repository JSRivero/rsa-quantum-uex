from math import gcd

def factorization(n):

    factors = []

    def get_factor(n):
        x_fixed = 2
        cycle_size = 2
        x = 2
        factor = 1

        while factor == 1:
            for count in range(cycle_size):
                if factor > 1: break
                x = (x * x + 1) % n
                factor = gcd(x - x_fixed, n)

            cycle_size *= 2
            x_fixed = x

        return factor

    while n > 1:
        next = get_factor(n)
        factors.append(next)
        n //= next

    return factors


def coprime(a, b):
    return gcd(a, b) == 1


def obtain_keys(p, q):

    n = p*q
    phin = (p-1)*(q-1)

    for x in range(2, phin):
        if coprime(x, phin):
            e = x
            break
    
    for x in range(2, phin):
        if x*e % phin == 1:
            d = x
            break
    
    return e, d, n

def get_public_key(p, q):
    public_key_e, _, public_key_n = obtain_keys(p, q)
    return public_key_e, public_key_n



def get_private_key(p, q):
    _, public_key_d, public_key_n = obtain_keys(p, q)
    return public_key_d, public_key_n