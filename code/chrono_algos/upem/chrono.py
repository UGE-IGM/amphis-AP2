#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['chronometre', 'chrono_liste', 'graphique']

from timeit import repeat as _repeat
from sys import setrecursionlimit as _setrecursionlimit
from matplotlib import pyplot as _plt
from numpy import arange as _arange


def chrono_liste(fun_list, generateur, nb_evaluations, pas=1,
                 nb_repetitions=1, nb_iterations=1, nb_recursions=None):
    """ Chronomètre une liste de fonctions 'fun_list' 'nb_evaluations'
        fois avec des paramètres générés par 'generateur'

    :param fun_list: liste des fonctions à chronométrer
    :param generateur: la fonction générant les valeurs à fournir aux
                       fonctions à chronométrer
    :param nb_evaluations: nombre d'évaluations
    :param pas: pas d'incrémentation ou de décrémentation
    :param nb_repetitions: nombre de répétitions pour chaque fonction
    :param nb_iterations: nombre d'appels pour chaque répétition
    :param nb_recursions: profondeur de récursion maximale
    :return: une liste de couples  (fonction, résultats) où 'résultats'
             est une liste de triplets (i, resultat, temps)
    """
    res = []
    for fun in fun_list:
        stats = chronometre(fun, generateur, nb_evaluations,
                            pas, nb_repetitions, nb_iterations, nb_recursions)
        res.append((fun.__name__, stats))
    return res


def chronometre(fonction, generateur, nb_evaluations, pas=1,
                nb_repetitions=1, nb_iterations=1, nb_recursions=None):
    """ Chronomètre la fonction 'fonction' 'nb_nb_evaluations' fois
        avec des paramètres générés par 'generateur'

    :param fonction: la fonction à chronométrer
    :param generateur: la fonction générant les valeurs à fournir à la
                       fonction à chronométrer
    :param nb_evaluations: nombre d'évaluations
    :param pas: pas d'incrémentation ou de décrémentation
    :param nb_repetitions: nombre de répétitions pour chaque fonction
    :param nb_iterations: nombre d'appels pour chaque répétition
    :param nb_recursions: profondeur de récursion maximale
    :return: une liste de triplets (i, resultat, temps)
    """
    if nb_recursions is not None:
        _setrecursionlimit(nb_recursions)
    resultats = []
    fun = lambda: fonction(*generateur(i))

    print('{}:'.format(fun.__name__), end='')
    for i in range(0, nb_evaluations*pas, pas):
        resultats.append((i, fun(),
                          min(_repeat(fun,
                                      number=nb_iterations,
                                      repeat=nb_repetitions))))
        progress = 100*(i+pas)/(pas*nb_evaluations)
        print('\r{}: {:.0f}%'.format(fonction.__name__, progress), end='')
    print()
    return resultats


def graphique(chrono, nb_evaluations, pas=1):
    """ Affiche les courbes de temps d'une ou de plusieurs
        fonctions ('chrono').

    :param chrono: liste de triplets (i, res, temps)
                   ou liste de couples  (fonction, résultats)
                   fourni par la fonction 'chronometre' ou 'chrono_liste'
    :param nb_evaluations: nombre d'évaluations
    :param pas: pas d'incrémentation ou de décrémentation
    :return: None
    """
    x = _arange(0, nb_evaluations*pas, pas)
    if isinstance(chrono, list):
        for fonction, resultats in chrono:
            resultats = list(map(lambda r: r[2], resultats))
            _plt.plot(x, resultats, label=fonction)
    else:
        resultats = list(map(lambda r: r[2], chrono[1]))
        _plt.plot(x, resultats, label=chrono[0])
    _plt.legend(loc='upper left')
    _plt.show()
