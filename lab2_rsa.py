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
