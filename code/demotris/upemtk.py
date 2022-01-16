#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Fichier upemtk.py
# Bibliothèque graphique simplifiée utilisant le module tkinter
# Dérivé de iutk.py, IUT de Champs-sur-Marne, 2013-2014

from tkinter import *
from tkinter import font
import subprocess
import sys
# from tkinter import _tkinter
# from time import *
# import os

__all__ = ['ignore_exception', 'auto_update', 'cree_fenetre', 'ferme_fenetre',
           'mise_a_jour', 'ligne', 'fleche', 'rectangle', 'cercle', 'point', 'marque',
           'image', 'texte', 'longueur_texte', 'hauteur_texte', 'efface_tout',
           'efface', 'efface_marque', 'attente_clic', 'attente_touche',
           'attente_clic_ou_touche', 'clic', 'capture_ecran', 'donne_evenement',
           'type_evenement', 'clic_x', 'clic_y', 'touche',
           'TypeEvenementNonValide', 'FenetreNonCree', 'FenetreDejaCree']


class CustomCanvas:
    """
    Classe qui encapsule tous les objets tkinter nécessaires à la création
    d'un canevas.
    """

    def __init__(self, width, height):
        # width and height of the canvas
        self.width = width
        self.height = height

        # root Tk object
        self.root = Tk()

        # canvas attached to the root object
        self.canvas = Canvas(self.root, width=width,
                             height=height, highlightthickness=0)

        # binding of the different events
        self.root.protocol("WM_DELETE_WINDOW", self.event_quit)
        self.canvas.bind("<Button-1>", self.event_handler_button1)
        right_button = "<Button-3>"  # d'après la doc le bouton droit le 3
        if sys.platform.startswith("darwin"):  # sous mac c'est le bouton 2
            right_button = "<Button-2>"
        self.canvas.bind(right_button, self.event_handler_button2)
        self.canvas.bind_all("<Key>", self.event_handler_key)
        self.canvas.pack()

        # eventQueue stores the list of events received
        self.eventQueue = []

        # font for the texte functions
        self.set_font("Purisa", 24)

        # marque
        self.tailleMarque = 5

        # update
        self.root.update()

    def set_font(self, _font, size):
        self.tkfont = font.Font(self.canvas, font=(_font, size))
        self.tkfont.height = self.tkfont.metrics("linespace")

    def update(self):
        # sleep(_tkinter.getbusywaitinterval() / 1000)
        self.root.update()

    def event_handler_key(self, event):
        self.eventQueue.append(("Touche", event))

    def event_handler_button2(self, event):
        self.eventQueue.append(("ClicDroit", event))

    def event_handler_button1(self, event):
        self.eventQueue.append(("ClicGauche", event))

    def event_quit(self):
        self.eventQueue.append(("Quitte", ""))


__canevas = None
__img = dict()


# ############################################################################
# Exceptions
#############################################################################

class TypeEvenementNonValide(Exception):
    pass


class FenetreNonCree(Exception):
    pass


class FenetreDejaCree(Exception):
    pass


#############################################################################
# Initialisation, mise à jour et fermeture
#############################################################################
def ignore_exception(function):
    def dec(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception:
            exit(0)
    return dec


def auto_update(function):
    def dec(*args, **kwargs):
        global __canevas
        retval = function(*args, **kwargs)
        __canevas.canvas.update()
        return retval
    return dec


def cree_fenetre(largeur, hauteur):
    """
    Crée une fenêtre de dimensions ``largeur`` x ``hauteur`` pixels.
    """
    global __canevas
    if __canevas is not None:
        raise FenetreDejaCree(
            'La fenêtre a déjà été crée avec la fonction "cree_fenetre".')
    __canevas = CustomCanvas(largeur, hauteur)


def ferme_fenetre():
    """
    Détruit la fenêtre.
    """
    global __canevas
    if __canevas is None:
        raise FenetreNonCree(
            "La fenêtre n'a pas été crée avec la fonction \"cree_fenetre\".")
    __canevas.root.destroy()
    __canevas = None


def mise_a_jour():
    """
    Met à jour la fenêtre. Les dessins ne sont affichés qu'après 
    l'appel à  cette fonction.
    """
    global __canevas
    if __canevas is None:
        raise FenetreNonCree(
            "La fenêtre n'a pas été crée avec la fonction \"cree_fenetre\".")
    __canevas.update()


#############################################################################
# Fonctions de dessin
#############################################################################


# Formes géométriques

def ligne(ax, ay, bx, by, couleur='black', epaisseur=1, tag=''):
    """
    Trace un segment reliant le point ``(ax, ay)`` au point ``(bx, by)``.

    :param float ax: abscisse du premier point
    :param float ay: ordonnée du premier point
    :param float bx: abscisse du second point
    :param float by: ordonnée du second point
    :param str couleur: couleur de trait (défaut 'black')
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    global __canevas
    return __canevas.canvas.create_line(
        ax, ay, bx, by,
        fill=couleur,
        width=epaisseur,
        tag=tag)


def fleche(ax, ay, bx, by, couleur='black', epaisseur=1, tag=''):
    """
    Trace une flèche du point ``(ax, ay)`` au point ``(bx, by)``.

    :param float ax: abscisse du premier point
    :param float ay: ordonnée du premier point
    :param float bx: abscisse du second point
    :param float by: ordonnée du second point
    :param str couleur: couleur de trait (défaut 'black')
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    global __canevas
    x, y = (bx - ax, by - ay)
    n = (x**2 + y**2)**.5
    x, y = x/n, y/n    
    points = [bx, by, bx-x*5-2*y, by-5*y+2*x, bx-x*5+2*y, by-5*y-2*x]
    return __canevas.canvas.create_polygon(
        points, 
        fill=couleur, 
        outline=couleur,
        width=epaisseur,
        tag=tag)


def rectangle(ax, ay, bx, by,
              couleur='black', remplissage='', epaisseur=1, tag=''):
    """
    Trace un rectangle noir ayant les point ``(ax, ay)`` et ``(bx, by)``
    comme coins opposés.

    :param float ax: abscisse du premier coin
    :param float ay: ordonnée du premier coin
    :param float bx: abscisse du second coin
    :param float by: ordonnée du second coin
    :param str couleur: couleur de trait (défaut 'black')
    :param str remplissage: couleur de fond (défaut transparent)
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    global __canevas
    return __canevas.canvas.create_rectangle(
        ax, ay, bx, by,
        outline=couleur,
        fill=remplissage,
        width=epaisseur,
        tag=tag)


def cercle(x, y, r, couleur='black', remplissage='', epaisseur=1, tag=''):
    """ 
    Trace un cercle de centre ``(x, y)`` et de rayon ``r`` en noir.

    :param float x: abscisse du centre
    :param float y: ordonnée du centre
    :param float r: rayon
    :param str couleur: couleur de trait (défaut 'black')
    :param str remplissage: couleur de fond (défaut transparent)
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    global __canevas
    return __canevas.canvas.create_oval(
        x - r, y - r, x + r, y + r,
        outline=couleur,
        fill=remplissage,
        width=epaisseur,
        tag=tag)


def arc(x, y, r, ouverture=90, depart=0, couleur='black', remplissage='',
        epaisseur=1, tag=''):
    """
    Trace un arc de cercle de centre ``(x, y)``, de rayon ``r`` et
    d'angle d'ouverture ``ouverture`` (défaut : 90 degrés, dans le sens
    contraire des aiguilles d'une montre) depuis l'angle initial ``depart``
    (défaut : direction 'est').

    :param float x: abscisse du centre
    :param float y: ordonnée du centre
    :param float r: rayon
    :param float ouverture: abscisse du centre
    :param float depart: ordonnée du centre
    :param str couleur: couleur de trait (défaut 'black')
    :param str remplissage: couleur de fond (défaut transparent)
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    global __canevas
    return __canevas.canvas.create_arc(
        x - r, y - r, x + r, y + r,
        extent=ouverture,
        start=init,
        style=ARC,
        outline=couleur,
        fill=remplissage,
        width=epaisseur,
        tag=tag)



def point(x, y, couleur='black', epaisseur=1, tag=''):
    """
    Trace un point aux coordonnées ``(x, y)`` en noir.

    :param float x: abscisse
    :param float y: ordonnée
    :param str couleur: couleur du point (défaut 'black')
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    return ligne(x, y, x + epaisseur, y + epaisseur,
                 couleur, epaisseur, tag)


# Marques

def marque(x, y, couleur="red"):
    """
    Place la marque sur la position (x, y) qui peut être effacé en appelant
    ``efface_marque()`` ou ``efface('marque')``. Une seule marque peut être
    présente simultanément.

    :param float x: abscisse
    :param float y: ordonnée
    :param str couleur: couleur de trait (défaut 'black')
    :return: ``None``
    """
    global __canevas
    efface_marque()
    __canevas.marqueh = ligne(
        x - __canevas.tailleMarque, y,
        x + __canevas.tailleMarque, y, couleur, tag='marque')
    __canevas.marquev = ligne(
        x, y - __canevas.tailleMarque,
        x, y + __canevas.tailleMarque, couleur, tag='marque')


# Image

def image(x, y, fichier, ancrage='center', tag=''):
    """
    Affiche l'image contenue dans ``fichier`` avec ``(x, y)`` comme centre. Les
    valeurs possibles du point d'ancrage sont ``'center'``, ``'nw'``, etc.

    :param float x: abscisse du point d'ancrage
    :param float y: ordonnée du point d'ancrage
    :param str fichier: nom du fichier contenant l'image
    :param ancrage: position du point d'ancrage par rapport à l'image
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    global __canevas
    global __img
    img = PhotoImage(file=fichier)
    img_object = __canevas.canvas.create_image(
        x, y, anchor=ancrage, image=img, tag=tag)
    __img[img_object] = img
    return img_object


# Texte

def texte(x, y, chaine,
          couleur='black', ancrage='nw', police="Purisa", taille=24, tag=''):
    """
    Affiche la chaîne ``chaine`` avec ``(x, y)`` comme point d'ancrage (par
    défaut le coin supérieur gauche).

    :param float x: abscisse du point d'ancrage
    :param float y: ordonnée du point d'ancrage
    :param str couleur: couleur de trait (défaut 'black')
    :param ancrage: position du point d'ancrage (défaut 'nw')
    :param police: police de caractères (défaut : 'Purisa')
    :param taille: taille de police (défaut 24)
    :param tag: étiquette d'objet (défaut : pas d'étiquette
    :return: identificateur d'objet
    """
    global __canevas
    __canevas.set_font(police, taille)
    return __canevas.canvas.create_text(
        x, y,
        text=chaine, font=__canevas.tkfont, tag=tag,
        fill=couleur, anchor=ancrage)


def longueur_texte(chaine):
    """
    Donne la longueur en pixel nécessaire pour afficher ``chaine``.

    :param str chaine: chaîne à mesurer
    :return: longueur de la chaîne en pixels (int)
    """
    global __canevas
    return __canevas.tkfont.measure(chaine)


def hauteur_texte():
    """
    Donne la hauteur en pixel nécessaire pour afficher du texte.

    :return: hauteur en pixels (int)
    """
    global __canevas
    return __canevas.tkfont.height


#############################################################################
# Effacer
#############################################################################

def efface_tout():
    """
    Efface la fenêtre.
    """
    global __canevas
    global __img
    __img.clear()
    __canevas.canvas.delete("all")


def efface(objet):
    """
    Efface ``objet`` de la fenêtre.

    :param: objet ou étiquette d'objet à supprimer
    :type: ``int`` ou ``str``
    """
    global __canevas
    if objet in __img:
        del __img[objet]
    __canevas.canvas.delete(objet)


def efface_marque():
    """
    Efface la marque créée par la fonction :py:func:``marque``.
    """
    efface('marque')


#############################################################################
# Utilitaires
#############################################################################


def attente_clic():
    """
    Attend que l'utilisateur clique sur la fenêtre et renvoie un triplet ``(
    x, y, type_clic)``, où ``x`` et ``y`` sont l'abscisse et l'ordonnée du
    point cliqué, et type_clic une chaîne valant ``'ClicGauche'`` ou
    ``'ClicDroit'`` selon le type de clic effectué.

    :return: un triplet ``(x, y, 'ClicDroit')`` ou ``(x, y, 'ClicGauche')``
    """
    while True:
        ev = donne_evenement()
        type_ev = type_evenement(ev)
        if type_ev == "ClicDroit" or type_ev == "ClicGauche":
            return clic_x(ev), clic_y(ev), type_ev
        mise_a_jour()


def attente_touche():
    """
    Attend que l'utilisateur appuie sur une touche.
    """
    while True:
        ev = donne_evenement()
        type_ev = type_evenement(ev)
        if type_ev == "Touche":
            break
        mise_a_jour()


def attente_clic_ou_touche():
    """
    Attend que l'utilisateur clique sur la fenêtre ou appuie sur une touche.
    La fonction renvoie un triplet de la forme ``(x, y, type)`` si l'événement
    est un clic de souris de type ``type`` et de coordonnées ``(x, y)``, ou (-1,
    touche, type) si l'événement est un appui sur la touche ``val``.

    :return: ``(x, y, 'ClicDroit')``, ``(x, y, 'ClicGauche')`` ou ``(-1, val,\
    'Touche')``

    """
    while True:
        ev = donne_evenement()
        type_ev = type_evenement(ev)
        if "Clic" in type_ev:
            return clic_x(ev), clic_y(ev), type_ev
        elif type_ev == "Touche":
            return -1, touche(ev), type_ev
        mise_a_jour()


def clic():
    """
    Attend que l'utilisateur clique sur la fenêtre, sans récupérer les
    détails de l'événement.
    """
    attente_clic()


def capture_ecran(file):
    """
    Fait une capture d'écran sauvegardée dans ``file.png``.
    """
    global __canevas
    __canevas.canvas.postscript(file=file + ".ps", height=__canevas.height,
                                width=__canevas.width, colormode="color")
    subprocess.call(
        "convert -density 150 -geometry 100% -background white -flatten",
        file + ".ps", file + ".png", shell=True)
    subprocess.call("rm", file + ".ps", shell=True)


#############################################################################
# Gestions des évènements
#############################################################################

def donne_evenement():
    """ 
    Renvoie l'événement associé à la fenêtre.
    """
    global __canevas
    if __canevas is None:
        raise FenetreNonCree(
            "La fenêtre n'a pas été crée avec la fonction \"cree_fenetre\".")
    if len(__canevas.eventQueue) == 0:
        return "RAS", ""
    else:
        return __canevas.eventQueue.pop()


def type_evenement(evenement):
    """ 
    Renvoie une chaîne donnant le type de ``evenement``. Les types
    possibles sont 'ClicDroit', 'ClicGauche', 'Touche' ou 'RAS'.
    """
    nom, ev = evenement
    return nom


def clic_x(evenement):
    """ 
    Renvoie la coordonnée X associé à ``evenement`` qui doit être de type
    'ClicDroit' ou 'ClicGauche'
    """
    nom, ev = evenement
    if not (nom == "ClicDroit" or nom == "ClicGauche"):
        raise TypeEvenementNonValide(
            'On ne peut pas utiliser "clic_x" sur un évènement de type', nom)
    return ev.x


def clic_y(evenement):
    """ 
    Renvoie la coordonnée Y associé à ``evenement``, qui doit être de type
    'ClicDroit' ou 'ClicGauche'.
    """
    nom, ev = evenement
    if not (nom == "ClicDroit" or nom == "ClicGauche"):
        raise TypeEvenementNonValide(
            'On ne peut pas utiliser "clic_y" sur un évènement de type', nom)
    return ev.y


def touche(evenement):
    """ 
    Renvoie une string correspondant à la touche associé à ``evenement``
    qui doit être de type 'Touche'.
    """
    nom, ev = evenement
    if not (nom == "Touche"):
        raise TypeEvenementNonValide(
            'On peut pas utiliser "touche" sur un évènement de type', nom)
    return ev.keysym
