def rech_exh_iter(lst, x):
    for elem in lst:
        if elem == x:
            return True
    return False


def rech_exh_rec(lst, x, d=0):
    if d >= len(lst):
        return False
    if lst[d] == x:
        return True
    return rech_exh_rec(lst, x, d+1)


def rech_in(lst, x):
    return x in lst


def rech_dicho_iter(lst, x):
    (g, d) = (0, len(lst) - 1)
    while g <= d:
        m = (g + d) // 2
        if lst[m] == x:
            return True
        elif lst[m] < x:
            g = m + 1
        else:
            d = m - 1
    return False


def rech_dicho_rec(lst, x, d=0, f=None):
    if f is None:
        f = len(lst)-1
    if d > f:
        return False
    m = (d + f) // 2
    if lst[m] == x:
        return True
    elif lst[m] < x:
        return rech_dicho_rec(lst, x, m+1, f)
    else:
        return rech_dicho_rec(lst, x, d, m-1)


def rech_dicho_prem(lst, e):

    def recherche(d, f):
        if d > f:
            return -1
        if d == f:
            if lst[d] == e:
                return d
            else:
                return -1
        m = (d + f) // 2

        if lst[m] >= e:
            return recherche(d, m)
        else:
            return recherche(m+1, f)

    return recherche(0, len(lst)-1)
