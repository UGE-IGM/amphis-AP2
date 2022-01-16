from algos.tri import *
from random import randint
from upem.chrono import chrono_liste, graphique


def liste_triee(taille):
    return list(range(taille))


def liste_aleatoire(taille, seuil=None):
    if seuil is None:
        seuil = taille
    return ([randint(0, seuil) for _ in range(taille)],)


if __name__ == "__main__":
    functions = [
        sorted,
        bubble_sort,
        bubble_sort_plus,
        shaker_sort,
        shaker_sort_plus,
        selection_sort,
        insertion_sort,
        quick_sort,
        merge_sort
    ]

    nb_evaluations = 40
    pas = 20
    stats = chrono_liste(functions, liste_aleatoire,
                         nb_evaluations,
                         pas,
                         nb_repetitions=2,
                         nb_iterations=1)
    graphique(stats, nb_evaluations, pas)
