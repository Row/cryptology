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

# Find the inverse of a mod n ( http://snippets.dzone.com/posts/show/4256 )
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
   
# Converts an integer to the string representation
# based on ascii-values.
def int_to_str(int_str):
    string = ""
    while(int_str > 0):
        string = chr(int_str & 255) + string
        int_str = int_str >> 8
    return string

#Find the index of x in a if it exists,
# else returns -1
def index(a, x):
    i = bisect.bisect_left(a, (x, -1))
    if i != len(a) and a[i][0] == x:
        return i
    return -1

# Appends the numbers from start to end to table and inv, using key (e, n) 
def create_table_and_inv(table, inv, e, n, start, end):
    for i in range(start, end+1):
        v = modpow(i, e, n)
        table.append((v, i))
        inv.append(mod_inverse(v, n))
    table.sort()

# Tries to match the ciphers in ciphertexts_int with the table and the list
# inv, with key size n, 2^r times
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
        else:
            done = False
            plain += "[?]"
    if L != -1:
        plain = plain.replace("[?]", L * "*")        
    return (done, plain)

# ciphertexts_int is a list of block ciphers to break, public key (e, n) and 
# initial table size r
# Side-effects prints the progress and finally the result 
def break_rsa(ciphertexts_int, e, n, r):
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
#################################################################
#### Here begins the statistical tests and program executions ###
#################################################################

# Main        
# Parse input and read ciphertexts
if len(sys.argv) < 4:
    print "Usage:"
    print "python lab2_break_rsa.py cipher.crypt key.pub r"
    print "integer r specifies the first range of the table ([1, 2, ..., 2^r])"
    sys.exit()
    
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

# Stats
if(1):
    # blabv    
    average_of = 1
    cmd = "break_rsa(%s, %d, %d, %d)" % (ciphertexts_int, e, n, r)
    t = timeit.Timer(stmt=cmd,setup="from __main__ import break_rsa")
    time = (t.timeit(average_of) / average_of)
    print "Runtime: %fs" % time
else:
    break_rsa(ciphertexts_int, e, n, r)    
