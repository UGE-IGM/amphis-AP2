#! /usr/bin/env python3
#from timing import time_functions

from upem.chrono import chrono_liste, graphique
from algos.recherche import *
from sys import setrecursionlimit


def zeroes_and_a_one(taille):
    return [0] * (taille-1) + [1], 1


if __name__ == '__main__':
    taille = 2000
    setrecursionlimit(taille + 10)
    functions = [
        rech_exh_iter,
        rech_exh_rec,
        rech_in,
        rech_dicho_iter,
        rech_dicho_rec
    ]

    nb_evaluations = 100
    pas = taille // nb_evaluations
    stats = chrono_liste(functions, zeroes_and_a_one,
                         nb_evaluations,
                         pas,
                         nb_repetitions=10,
                         nb_iterations=10)
    graphique(stats, nb_evaluations, pas)
