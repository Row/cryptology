import random
import math
# Schneier 1996, p. 224. (wikipedia)
def modpow(b, e, m):
    result = 1
    while (e > 0):
        if e & 1:
            result = (result * b) % m
        e = e >> 1
        b = (b * b) % m
    return result

assert modpow(2,1,2) == 0, "Not equal"
assert modpow(4,13,497) == 445, "Not equal"
assert modpow(2,21701,2) == 0, "Not equal"

def get_odd_rand():
    x = random.randint(pow(2,32), pow(2,512))
    if not (x & 1):
            x -= 1
    return x

def get_large_prime():
    prime = get_odd_rand()
    while(COMPOSITE == primality_test(prime, 100)):
        prime = get_odd_rand()

    return prime
# Constants
COMPOSITE = 0
PROBABLY_PRIME = 1
    
# Miller Rabin primality test (wikipedia)
# Input: n > 3, an odd integer to be tested for primality;
# Input: k, a parameter that determines the accuracy of the test
# Output: composite if n is composite, otherwise probably prime
def primality_test(n, k):
    s = 0
    d = n - 1
    while(d & 1):
        d = d >> 1
        s += 1
    for i in range(k):
        a = random.randint(2, n - 2)
        x = modpow(a,d,n)
        bo = 0
        if (x != 1 and x != n - 1):
            for r in range(1, s):
                x = modpow(x, 2, n)
                if x == 1:
                    return COMPOSITE
                bo = x == n - 1 
                if bo:
                    break
            if bo:
                continue
            return COMPOSITE
    return PROBABLY_PRIME

assert primality_test(pow(2,512) - 1, 20) == COMPOSITE

# (wikipedia)
def gcd(a, b):
    while (b != 0):
        t = b
        b = a % b
        a = t 
    return a

def extended_gcd(a, b):
    x = 0
    y = 1
    lastx = 1
    lasty = 0
    while (b != 0):
        q = a / b
        t = b
        b = a % b
        a = t
        
        t = lastx - q * x
        lastx = x
        x = t
        
        t = lasty - q * y
        lasty = y
        y = t        
    return lasty

def mod_inverse(a, n):
    i = n
    v = 0
    d = 1
    while a > 0:
        t = i/a
        x = a
        a = i % x
        i = x
        x = d
        d = v - t*x
        v = x
    return v % n
   

def generate_keys():
    p = get_large_prime()
    q = get_large_prime()

    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Public key
    e = random.randint(math.ceil(math.log(n, 2)), phi_n)
    while(gcd(e, phi_n) != 1):
        e = random.randint(math.ceil(math.log(n, 2)), phi_n)

    # Private key
    #d = extended_gcd(phi_n, e)
    d = mod_inverse(e, phi_n)

    #print "Public key: ", e
    #print "Private key: ", d
    
    return ((e, n), (d, n))

# c = pow(m, e) mod n	
def encrypt(msg, (e, n)):
    return modpow(msg, e, n)

# m = pow(c, d) mod n
def decrypt(cipher, (d, n)):
    return modpow(cipher, d, n)

pub_key, priv_key = generate_keys()
print "Public key:", pub_key
print "Private key:", priv_key
assert 67 == decrypt(encrypt(67, priv_key), pub_key), "Broken encryption/decryption"
