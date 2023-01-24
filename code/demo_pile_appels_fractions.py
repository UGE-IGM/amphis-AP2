def pgcd(a, b):
    while b:
        a, b = b, a % b
    return a

def simplifier(fraction):
    d = pgcd(fraction[0], fraction[1])
    res = (fraction[0] // d, fraction[1] // d)
    return res

def ajouter(frac1, frac2):
    denom = frac1[1] * frac2[1]
    num = (frac1[0] * frac2[1]
           + frac2[0] * frac1[1])
    res = simplifier((num, denom))
    return res

frac = ajouter((1, 3), (1, 6))
print(frac)