import random
import math
import timeit
import sys

# Schneier 1996, p. 224. (wikipedia)
def modpow(b, e, m):
    result = 1
    while (e > 0):
        if e & 1:
            result = (result * b) % m
        e = e >> 1
        b = (b * b) % m
    return result

def get_odd_rand(elower, eupper):
    x = random.randint(pow(2,elower), pow(2,eupper))
    if not (x & 1):
            x -= 1
    return x

def get_large_prime(elower, eupper):
    prime = get_odd_rand(elower, eupper)
    while(COMPOSITE == primality_test(prime, 100)):
        prime = get_odd_rand(elower, eupper)
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
        x = modpow(a, d, n)
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
# 
# Input: a, an integer that's larger that b
# Input: b, an integer smaller than a
# Output: The greatest Common divisor between a and b
def gcd(a, b):
    while (b != 0):
        t = b
        b = a % b
        a = t 
    return a

# Find the inverse of a mod n
# Input: a, an integer of which to find the inverse
# of modulo n.
# Input: n, the base 
def mod_inverse(a, n):
    i = n
    v = 0
    d = 1
    while a > 0:
        t = i / a
        x = a
        a = i % x
        i = x
        x = d
        d = v - t * x
        v = x
    return v % n
   
# Input elower and eupper are lower respective upper bit length of the primes
# Ouput ((e, n), (d, n)) where (e, n) is the public key and (d, n) the private
def generate_keys(elower, eupper):
    p = get_large_prime(elower, eupper)
    q = get_large_prime(elower, eupper)
    return generate_keys_with_primes(p, q)

def generate_keys_with_primes(p, q):
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Public key
    e = random.randint(math.ceil(math.log(n, 2)), phi_n)
    while (gcd(e, phi_n) != 1):
        e = random.randint(math.ceil(math.log(n, 2)), phi_n)

    # Private key
    d = mod_inverse(e, phi_n)

    #print "Public key: ", e
    #print "Private key: ", d
    
    return ((e, n), (d, n))

# string is the string to encrypt
# returns the integer representation of the cipher	
def encrypt(string, (e, n)): 
    return modpow(str_to_int(string), e, n)

# cipher as the integer
# returns the decrypted string
def decrypt(cipher, (d, n)):
    return int_to_str(modpow(cipher, d, n)) 

# encrypt with block length L
def encrypt_block(string, L, pub_key):
    ciphers = []
    i = 0
    while i < len(string):
        j = i + L
        ciphers.append(encrypt(string[i:j], pub_key))
        i = j
    return ciphers

# decrypt the list ciphers with priv_key
def decrypt_block(ciphers, priv_key):
    string = ""
    for i in ciphers:
        string += decrypt(i, priv_key)
    return string

def str_to_int(string):
    str_int = 0
    for i in range(len(string)):
        str_int = str_int << 8
        str_int += ord(string[i])
    return str_int

def int_to_str(int_str):
    string = ""
    while(int_str > 0):
        string = chr(int_str & 255) + string
        int_str = int_str >> 8
    return string

def count_bits(inten):
    c = 0
    while inten > 0:
        c += 1
        inten = inten >> 1
    return c

#################################################################
#### Here begins the statistical tests and program executions ###
#################################################################

stats = 0
debug = 0
if(stats):   
    pub_key, priv_key = generate_keys(32, 33)
    d, n = priv_key 
    e, n = pub_key
    
    # Length of L
    time = [] 
    length_of_l = [2,4,8,16,32,64,128]
    string = "x" * 200
    for i in length_of_l:
        cmd = "encrypt_block('%s',%d,(%d, %d))" % (string, i, e, n) 
        t = timeit.Timer(stmt=cmd,setup="from __main__ import encrypt_block")
        time.append((t.timeit(10) / 10)) # average 
    print "Length of L"
    print time
    print length_of_l
    
    # Length of input
    time = [] 
    bits = [2,4,8,16,32,64,128,256]
    for i in bits:
        string = "x" * i
        cmd = "encrypt_block('%s', 2, (%d, %d))" % (string, e, n) 
        t = timeit.Timer(stmt=cmd,setup="from __main__ import encrypt_block")
        time.append((t.timeit(10) / 10)) # average of 10
    print "Encryption with length of text with block size 2"
    print time
    print bits
    
    # Length of input
    time = [] 
    bits = [2,4,8,16,32,64,128,256]
    for i in bits:
        string = "x" * i
        ciphers = encrypt_block(string, 2, pub_key)
        cmd = "decrypt_block(%s,(%d, %d))" % (ciphers, d, n) 
        t = timeit.Timer(stmt=cmd,setup="from __main__ import decrypt_block")
        time.append((t.timeit(10) / 10)) # average of 10
    print "Length of text with of block size 2"
    print time
    print bits
    
    # generate_keys the size (in number of bits) of p and q.    
    time = [] 
    bits = [32,64,128,256,511]
    for i in bits:
        cmd = "generate_keys(%d, %d)" % (i, (i + 1)) 
        t = timeit.Timer(stmt=cmd,setup="from __main__ import generate_keys")
        time.append((t.timeit(10) / 10)) # average of 10
    print time
    print bits
    
    # Length of d and e
    time = [] 
    bits_real = []
    bits = [32,64,128,256,512]
    for i in bits:
        string = "xY" * 50
        pub_key, priv_key = generate_keys(i, 128)
        d, n = priv_key
        e, n = pub_key
        cmd = "encrypt_block('%s', 2, (%d, %d))" % (string, e, n) 
        t = timeit.Timer(stmt=cmd,setup="from __main__ import encrypt_block")
        time.append(t.timeit(1))
        #bits_real.append((count_bits(d),count_bits(e)))
        print bits_real
    print "Size of e"
    print time
    print bits
    print bits_real
       
if(debug):
    # Test Case
    assert modpow(2,1,2) == 0, "Not equal"
    assert modpow(4,13,497) == 445, "Not equal"
    assert modpow(2,21701,2) == 0, "Not equal"
    assert modpow(76,377,437) == pow(76,377,437), "Not equal"
    assert modpow(76,377,437) == 228, "Not equal"

    for i in range(1, 99999):
        x = random.randint(1,1000)
        y = random.randint(1,1000)
        z = random.randint(1,1000)
        assert modpow(x,y,z) == pow(x,y,z), "Not equal"
    
    # Generate keys 
    pub_key, priv_key = generate_keys(32, 512)
    print "Public key:", pub_key
    print "Private key:", priv_key
    assert "A" == decrypt(encrypt("A", pub_key), priv_key), "Broken encryption/decryption"

    msg = "abc ABC abc, encrypt and decrypt this as an integer?"
    assert msg == int_to_str(str_to_int(msg)), "Not equal"
    cipher = encrypt(msg, pub_key)
    print "Cipher is: '%d'" % cipher
    msg1 = decrypt(cipher, priv_key)
    print "Plain is: '%s'" % msg1 
    assert msg == msg1, "Broken"

    # Test case using block 
    L = 2
    assert msg == decrypt_block(encrypt_block(msg, L, pub_key), priv_key), "Broken block"

    
    
if(not stats):
    # Parse input and read plaintext
    L = int(sys.argv[1])
    plaintext = ""
    for i in range(2, len(sys.argv)):
        input = open(sys.argv[i])
        plaintext = "".join(input.readlines())
        input.close()
    
    print "Input plaintext: ", plaintext
    
    # Generate keys
    print "Generating keys"
    pub_key, priv_key = generate_keys(6, 256)
    print "Public key: ", pub_key
    print "Private key: ", priv_key
    
    # Save public key to file
    e, n = pub_key
    FILE = open("rsa_group4_%d.pub" % L, "w")
    FILE.write("%d\n%d" % (e, n))
    FILE.close()
    
    # Save private key to file
    d, n = priv_key
    FILE = open("rsa_group4_%d.key" % L, "w")
    FILE.write("%d\n%d" % (d, n))
    FILE.close()

    # Encrypt plaintext
    ciphertext = encrypt_block(plaintext, L, pub_key)
    print "Writing ciphertext file"
    FILE = open("rsa_group4_%d.crypto" % L,"w")
    for i in ciphertext:
        FILE.write("%d\n" % i)
    FILE.close()
    
    decrypted_text = decrypt_block(ciphertext, priv_key)
    
    # Write plain text
    FILE = open("rsa_group4_%s.plain" % L, "w")
    FILE.write(decrypted_text)  
    FILE.close()
