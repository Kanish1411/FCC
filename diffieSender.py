import sympy
import math

def find_order(a, n):
    if (a == 1) & (n == 1):
        return 1
    if math.gcd(a, n) != 1:
        print ("a and n should be relative prime!")
        return -1
    for i in range(1, n):
        if pow(a, i) % n == 1:
            return i
    return -1
def euler_totient(n):
    result = n
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            while n % i == 0:
                n //= i
            result -= result // i
    if n > 1:
        result -= result // n
    return result


def find_primitive_root(n):
    if n == 1:
        return [0]
    phi = euler_totient(n)
    for i in range (n-1, 0,-1):
        if math.gcd(i, n) == 1:
            order = find_order(i, n)
            if order == phi:
                return i
    return None
def base():
    p=sympy.randprime(100,1000)
    print(p)
    g=find_primitive_root(p)
    print(g)
    return (g,p)

def mod(g,n,p):
    return (g**n)%p


