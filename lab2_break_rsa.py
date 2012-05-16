import random
import math
import timeit
import sys
import bisect

# Schneier 1996, p. 224. (wikipedia)
def modpow(b, e, m):
    result = 1
    while (e > 0):
        if e & 1:
            result = (result * b) % m
        e = e >> 1
        b = (b * b) % m
    return result

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
   
# string is the string to encrypt
# returns the integer representation of the cipher	
def encrypt(string, (e, n)): 
    return modpow(str_to_int(string), e, n)

# cipher as the integer
# returns the decrypted string
def decrypt(cipher, (d, n)):
    return int_to_str(modpow(cipher, d, n)) 

# encrypt with block length L
def encrypt_block(string, L, priv_key):
    ciphers = []
    i = 0
    while i < len(string):
        j = i + L
        ciphers.append(encrypt(string[i:j], priv_key))
        i = j
    return ciphers

# decrypt the list ciphers with pub_key
def decrypt_block(ciphers, pub_key):
    string = ""
    for i in ciphers:
        string += decrypt(i, pub_key)
    return string

def str_to_int(string):
    str_int = 0
    for i in range(len(string)):
        str_int = str_int << 8
        str_int += ord(string[i])
    return str_int

# Converts an integer to the string representation
# based on ascii-values.

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

#Find the index of x in a if it exists,
# else returns -1
def index(a, x):
    i = bisect.bisect_left(a, (x, -1))
    if i != len(a) and a[i][0] == x:
        return i
    return -1

def create_table_and_inv(table, inv, e, n, start, end):
    for i in range(start, end+1):
        if i % 10000 == 0:
            print i
        v = modpow(i, e, n)
        table.append((v, i))
        inv.append(mod_inverse(v, n))
    table.sort()
        
def match(ciphertexts_int, table, inv, n, r):
    plain = ""
    L = -1
    done = True
    for c in ciphertexts_int:
        i = 1
        while i <= pow(2,r):
            foundindex = index(table, c*inv[i-1] % n)
            if foundindex > -1:
                break
            i += 1
        if foundindex > -1:
            (oldv, j) = table[foundindex]
            m = int_to_str(i*j % n)
            plain += m
            L = len(m)
            # print "m = '%s', i = %d, j = %d" % (int_to_str(m), i, j)
        else:
            # print "m = ?, i = %d" % i
            done = False
            plain += "[?]"
    if L != -1:
        plain = plain.replace("[?]", L * "*")        
    return (done, plain)
    

#################################################################
#### Here begins the statistical tests and program executions ###
#################################################################

debug = 0
       
if(debug):
    # Test Case
    assert modpow(2,1,2) == 0, "Not equal"
    assert modpow(4,13,497) == 445, "Not equal"
    assert modpow(2,21701,2) == 0, "Not equal"
    assert modpow(76,377,437) == pow(76,377,437), "Not equal"
    assert modpow(76,377,437) == 228, "Not equal"

        
if(not debug):
    # Parse input and read ciphertexts
    #r = int(sys.argv[1])
    ciphertexts = []
    input = open(sys.argv[1])
    ciphertexts = input.readlines()
    input.close()
    ciphertexts_int = []
    for i in ciphertexts:
        ciphertexts_int.append(int(i))
        
    input = open(sys.argv[2])
    e = int(input.readline())
    n = int(input.readline())
    input.close()
    r = int(sys.argv[3])  
    
    table = []
    inv = []
    r_old = 0
    cont = "y"
    done = False
    while not done:
        if r_old == 0:
            print "Creating table [1, 2^%d]..." % r
            create_table_and_inv(table, inv, e, n, 1, pow(2,r))
        else:
            print "Creating table [2^%d+1, 2^%d]..." % (r_old, r)
            create_table_and_inv(table, inv, e, n, pow(2,r_old)+1, pow(2,r))
        (done, plain) = match(ciphertexts_int, table, inv, n, r)
        print "Plaintext: '%s'" % plain
        r_old = r
        r += 1
