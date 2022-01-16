from random import randint, shuffle


def aleatoire(nb_elems):
    return [randint(1, nb_elems+1) for _ in range(nb_elems)]


def permutation(nb_elem):
    res = list(range(1, nb_elem+1))
    shuffle(res)
    return res


def croissante(nb_elems):
    return list(range(1, nb_elems+1))


def decroissante(nb_elems):
    return list(range(nb_elems, 0, -1))


def repetitions(nb_elems):
    return [randint(1, 10) for _ in range(nb_elems)]