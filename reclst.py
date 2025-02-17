from random import randrange


def liste_vide():
    """
    Renvoie une liste récursive vide.
    """
    return None


def est_vide(r_liste):
    """
    Renvoie True si r_liste est vide, False sinon.

    >>> est_vide(liste_vide())
    True
    >>> est_vide(('a', ('b', ('c', None))))
    False
    """
    return r_liste == None


def ajout_debut(v, r_liste):
    """
    Crée une liste récursive contenant v suivi des éléments de r_liste.

    >>> ajout_debut('a', liste_vide())
    ('a', None)
    >>> ajout_debut('a', ajout_debut('b', liste_vide()))
    ('a', ('b', None))
    """
    return (v, r_liste)
ajout_debut('a', 
    ajout_debut('b', 
        ajout_debut('c', 
            liste_vide())))
def tete(r_liste):
    """
    Renvoie l'élément de tête de r_liste.

    ATTENTION : plante si r_liste est vide !

    >>> tete(('a', ('b', None)))
    'a'

    >>> tete(None)
    Traceback (most recent call last):
    ...
    TypeError: 'NoneType' object is not subscriptable
    """
    return r_liste[0]


def suite(r_liste):
    """
    Renvoie r_liste privée de son élément de tête.

    ATTENTION : plante si r_liste est vide !

    >>> suite(('a', ('b', None)))
    ('b', None)

    >>> suite(None)
    Traceback (most recent call last):
    ...
    TypeError: 'NoneType' object is not subscriptable
    """
    return r_liste[1]


def liste_aleatoire(longueur, min=0, max=None):
    if max is None:
        max = longueur
    if longueur == 0:
        return liste_vide()
    else:
        tmp = liste_aleatoire(longueur-1, min, max)
        return ajout_debut(randrange(min, max), tmp)
    