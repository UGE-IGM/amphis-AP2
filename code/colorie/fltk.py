import subprocess
import sys
import tkinter as tk
from collections import deque
from os import system
from time import time, sleep
from tkinter.font import Font

try:
    from PIL import Image, ImageTk
    print("Bibliothèque PIL chargée.", file=sys.stderr)
    PIL_AVAILABLE = True
except ImportError as e:
    PIL_AVAILABLE = False

__all__ = [
    # gestion de fenêtre
    'cree_fenetre',
    'ferme_fenetre',
    'mise_a_jour',
    # dessin
    'ligne',
    'fleche',
    'polygone',
    'rectangle',
    'cercle',
    'point',
    'image',
    'texte',
    'taille_texte',
    # effacer
    'efface_tout',
    'efface',
    # utilitaires
    'attente',
    'capture_ecran',
    'touche_pressee',
    'abscisse_souris',
    'ordonnee_souris',
    # événements
    'donne_ev',
    'attend_ev',
    'attend_clic_gauche',
    'attend_fermeture',
    'type_ev',
    'abscisse',
    'ordonnee',
    'touche'
]


class CustomCanvas:
    """
    Classe qui encapsule tous les objets tkinter nécessaires à la création
    d'un canevas.
    """

    _on_osx = sys.platform.startswith("darwin")

    _ev_mapping = {
        'ClicGauche': '<Button-1>',
        'ClicMilieu': '<Button-2>',
        'ClicDroit': '<Button-2>' if _on_osx else '<Button-3>',
        'Deplacement': '<Motion>',
        'Touche': '<Key>'
    }

    _default_ev = ['ClicGauche', 'ClicDroit', 'Touche']

    def __init__(self, width, height, refresh_rate=100, events=None):
        # width and height of the canvas
        self.width = width
        self.height = height
        self.interval = 1/refresh_rate

        # root Tk object
        self.root = tk.Tk()

        # canvas attached to the root object
        self.canvas = tk.Canvas(self.root, width=width,
                                height=height, highlightthickness=0)

        # adding the canvas to the root window and giving it focus
        self.canvas.pack()
        self.canvas.focus_set()

        # binding events
        self.ev_queue = deque()
        self.pressed_keys = set()
        self.events = CustomCanvas._default_ev if events is None else events
        self.bind_events()

        # marque
        self.tailleMarque = 5

        # update for the first time
        self.last_update = time()
        self.root.update()

        if CustomCanvas._on_osx:
            system('''/usr/bin/osascript -e 'tell app "Finder" \
                   to set frontmost of process "Python" to true' ''')

    def update(self):
        t = time()
        self.root.update()
        sleep(max(0., self.interval - (t - self.last_update)))
        self.last_update = time()

    def bind_events(self):
        self.root.protocol("WM_DELETE_WINDOW", self.event_quit)
        self.canvas.bind('<KeyPress>', self.register_key)
        self.canvas.bind('<KeyRelease>', self.release_key)
        for name in self.events:
            self.bind_event(name)

    def register_key(self, ev):
        self.pressed_keys.add(ev.keysym)

    def release_key(self, ev):
        if ev.keysym in self.pressed_keys:
            self.pressed_keys.remove(ev.keysym)

    def event_quit(self):
        self.ev_queue.append(("Quitte", ""))

    def bind_event(self, name):
        e_type = CustomCanvas._ev_mapping.get(name, name)

        def handler(event, _name=name):
            self.ev_queue.append((_name, event))
        self.canvas.bind(e_type, handler, '+')

    def unbind_event(self, name):
        e_type = CustomCanvas._ev_mapping.get(name, name)
        self.canvas.unbind(e_type)


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


def cree_fenetre(largeur, hauteur, frequence=100):
    """
    Crée une fenêtre de dimensions ``largeur`` x ``hauteur`` pixels.
    :rtype:
    """
    global __canevas
    if __canevas is not None:
        raise FenetreDejaCree(
            'La fenêtre a déjà été crée avec la fonction "cree_fenetre".')
    __canevas = CustomCanvas(largeur, hauteur, frequence)


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


def polygone(points, couleur='black', remplissage='', epaisseur=1, tag=''):
    """
    Trace un polygone dont la liste de points est fournie.

    :param list points: liste de couples (abscisse, ordonnee) de points
    :param str couleur: couleur de trait (défaut 'black')
    :param str remplissage: couleur de fond (défaut transparent)
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    return __canevas.canvas.create_polygon(
        points, 
        fill=remplissage, 
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
    return __canevas.canvas.create_arc(
        x - r, y - r, x + r, y + r,
        extent=ouverture,
        start=depart,
        style=tk.ARC,
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
    return cercle(x, y, epaisseur,
                  couleur=couleur,
                  remplissage=couleur,
                  tag=tag)


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
    if PIL_AVAILABLE:
        img = Image.open(fichier)
        tkimage = ImageTk.PhotoImage(img)
    else:
        tkimage = tk.PhotoImage(file=fichier)
    img_object = __canevas.canvas.create_image(
        x, y, anchor=ancrage, image=tkimage, tag=tag)
    __img[img_object] = tkimage
    return img_object


# Texte

def texte(x, y, chaine,
          couleur='black', ancrage='nw', police='Helvetica', taille=24, tag=''):
    """
    Affiche la chaîne ``chaine`` avec ``(x, y)`` comme point d'ancrage (par
    défaut le coin supérieur gauche).

    :param float x: abscisse du point d'ancrage
    :param float y: ordonnée du point d'ancrage
    :param str chaine: texte à afficher
    :param str couleur: couleur de trait (défaut 'black')
    :param ancrage: position du point d'ancrage (défaut 'nw')
    :param police: police de caractères (défaut : `Helvetica`)
    :param taille: taille de police (défaut 24)
    :param tag: étiquette d'objet (défaut : pas d'étiquette
    :return: identificateur d'objet
    """

    return __canevas.canvas.create_text(
        x, y,
        text=chaine, font=(police, taille), tag=tag,
        fill=couleur, anchor=ancrage)


def taille_texte(chaine, police='Helvetica', taille='24'):
    """
    Donne la largeur et la hauteur en pixel nécessaires pour afficher
    ``chaine`` dans la police et la taille données.

    :param str chaine: chaîne à mesurer
    :param police: police de caractères (défaut : `Helvetica`)
    :param taille: taille de police (défaut 24)
    :return: couple (w, h) constitué de la largeur et la hauteur de la chaîne
        en pixels (int), dans la police et la taille données.
    """
    font = Font(family=police, size=taille)
    return font.measure(chaine), font.metrics("linespace")


#############################################################################
# Effacer
#############################################################################

def efface_tout():
    """
    Efface la fenêtre.
    """
    __img.clear()
    __canevas.canvas.delete("all")


def efface(objet):
    """
    Efface ``objet`` de la fenêtre.

    :param: objet ou étiquette d'objet à supprimer
    :type: ``int`` ou ``str``
    """
    if objet in __img:
        del __img[objet]
    __canevas.canvas.delete(objet)


#############################################################################
# Utilitaires
#############################################################################


def attente(temps):
    start = time()
    while time() - start < temps:
        mise_a_jour()


def capture_ecran(file):
    """
    Fait une capture d'écran sauvegardée dans ``file.png``.
    """
    __canevas.canvas.postscript(file=file + ".ps", height=__canevas.height,
                                width=__canevas.width, colormode="color")

    subprocess.call(
        "convert -density 150 -geometry 100% -background white -flatten"
        " " + file + ".ps " + file + ".png", shell=True)
    subprocess.call("rm " + file + ".ps", shell=True)


def touche_pressee(keysym):
    """
    Renvoie `True` si ``keysym`` est actuellement pressée.
    :param keysym: symbole associé à la touche à tester.
    :return: `True` si ``keysym`` est actuellement pressée, `False` sinon.
    """
    return keysym in __canevas.pressed_keys


#############################################################################
# Gestions des évènements
#############################################################################

def donne_ev():
    """ 
    Renvoie immédiatement l'événement en attente le plus ancien,
    ou ``None`` si aucun événement n'est en attente.
    """
    if __canevas is None:
        raise FenetreNonCree(
            "La fenêtre n'a pas été créée avec la fonction \"cree_fenetre\".")
    if len(__canevas.ev_queue) == 0:
        return None
    else:
        return __canevas.ev_queue.popleft()


def attend_ev():
    """Attend qu'un événement ait lieu et renvoie le premier événement qui
    se produit."""
    while True:
        ev = donne_ev()
        if ev is not None:
            return ev
        mise_a_jour()


def attend_clic_gauche():
    """Attend qu'un clic gauche sur la fenêtre ait lieu et renvoie ses
    coordonnées. **Attention**, cette fonction empêche la détection d'autres
    événements ou la fermeture de la fenêtre."""
    while True:
        ev = donne_ev()
        if ev is not None and type_ev(ev) == 'ClicGauche':
            return abscisse(ev), ordonnee(ev)
        mise_a_jour()


def attend_fermeture():
    """Attend la fermeture de la fenêtre. Cette fonction renvoie None.
    **Attention**, cette fonction empêche la détection d'autres événements."""
    while True:
        ev = donne_ev()
        if ev is not None and type_ev(ev) == 'Quitte':
            ferme_fenetre()
            return
        mise_a_jour()


def type_ev(ev):
    """ 
    Renvoie une chaîne donnant le type de ``ev``. Les types
    possibles sont 'ClicDroit', 'ClicGauche', 'Touche' et 'Quitte'.
    Renvoie ``None`` si ``evenement`` vaut ``None``.
    """
    return ev if ev is None else ev[0]


def abscisse(ev):
    """ 
    Renvoie la coordonnée x associé à ``ev`` si elle existe, None sinon.
    """
    return attribut(ev, 'x')


def ordonnee(ev):
    """ 
    Renvoie la coordonnée y associé à ``ev`` si elle existe, None sinon.
    """
    return attribut(ev, 'y')


def touche(ev):
    """ 
    Renvoie une chaîne correspondant à la touche associé à ``ev``,
    si elle existe.
    """
    return attribut(ev, 'keysym')


def attribut(ev, nom):
    if ev is None:
        raise TypeEvenementNonValide(
            "Accès à l'attribut", nom, 'impossible sur un événement vide')
    tev, ev = ev
    if hasattr(ev, nom):
        return getattr(ev, nom)
    else:
        raise TypeEvenementNonValide(
            "Accès à l'attribut", nom,
            'impossible sur un événement de type', tev)


def abscisse_souris():
    return __canevas.canvas.winfo_pointerx() - __canevas.canvas.winfo_rootx()


def ordonnee_souris():
    return __canevas.canvas.winfo_pointery() - __canevas.canvas.winfo_rooty()
