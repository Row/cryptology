import random
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

def get_rand():
    return random.randint(pow(2,32), pow(2,512))


# Constants
COMPOSITE = 0
PROBABLY_PRIME = 1
    
# Miller Rabin primality test
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

print primality_test(7, 2) == PROBABLY_PRIME
print primality_test(12, 2) == COMPOSITE
print primality_test(pow(2,512) - 1, 2) == COMPOSITE

prime = 4
while(COMPOSITE != primality_test(prime, 10)):
    print prime
    prime = get_rand()

print prime

