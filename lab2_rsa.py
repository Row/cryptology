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

# Constants
COMPOSITE = 0
PROBLABLY_PRIME = 1

# Miller–Rabin primality test
# Input: n > 3, an odd integer to be tested for primality;
# Input: k, a parameter that determines the accuracy of the test
# Output: composite if n is composite, otherwise probably prime
def primality_test(n, k):
    for i in range(k):
        

write n − 1 as 2s·d with d odd by factoring powers of 2 from n − 1

LOOP: repeat k times:
   pick a random integer a in the range [2, n − 2]
   x ← ad mod n
   if x = 1 or x = n − 1 then do next LOOP
   for r = 1 .. s − 1
      x ← x2 mod n
      if x = 1 then return composite
      if x = n − 1 then do next LOOP
   return composite
return probably prime
