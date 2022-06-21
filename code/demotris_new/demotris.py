# -*-coding:utf-8-*-#

import tkinter as tk
from tkinter import ttk
from tkinter import font
from tris import *
from generateurs import *

# TODO : essayer de faire une liste auxiliaire pour le tri fusion
#
#     self.dessins = ttk.Frame(self.root)
#     self.dessins.grid(column=0, row=0, sticky='nsew')
#     self.dessins.bind("<Configure>", self.resize)
#
#     self.dessin = tk.Canvas(self.dessins, width=largeur, height=hauteur / 2,
#                             background='lightgray', bd=0,
#                             highlightthickness=0)
#     self.dessin.grid(column=0, row=1, sticky='nsew')
#
#     self.aux = tk.Canvas(self.dessins, width=largeur, height=hauteur / 2,
#                          background='darkgray', bd=0,
#                          highlightthickness=0)
#     self.aux.grid(column=0, row=0, sticky='nsew')


class StopAnimation(Exception):
    pass


class DemoTris:
    algos_generation = [
        ('Liste aléatoire', aleatoire),
        ('Liste sans doublons', permutation),
        ('Liste croissante', croissante),
        ('Liste décroissante', decroissante),
        ('Liste à répétitions', repetitions)
    ]

    def __init__(self,
                 nb_elems=32,
                 largeur=1000,
                 hauteur=600,
                 marge=10,
                 couleur='lightgreen',
                 pause=False,
                 delay=200,
                 stepwise=False):
        self.nb_elems = nb_elems
        self.min_elems = 8
        self.default_elems = 32
        self.max_elems = 128
        self.marge = marge
        self.largeur = largeur
        self.hauteur = hauteur
        self.pause = pause
        self.stop = False
        self.delay = delay
        self.stepwise = stepwise
        self.couleur = couleur

        self.vars_by_name = {}
        self.vars_by_index = {}

        self.root = tk.Tk()
        self.dessin = tk.Canvas(self.root, width=largeur, height=hauteur,
                                background='lightgray', bd=0,
                                highlightthickness=0)
        self.menu = ttk.Frame(self.root)
        self.create_buttons(DemoTris.algos_generation, algos_tri)

        self.dessin.grid(column=0, row=0, sticky='nsew')
        self.dessin.bind("<Configure>", self.resize)
        self.menu.grid(column=1, row=0, sticky='ns')

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.police = font.Font(self.dessin, font=('Arial', 10))

        self.elems = aleatoire(self.nb_elems)
        self.rectangles = self.create_rectangles()
        self.redraw_list()
        self.root.mainloop()

    def resize(self, event):
        echelle_l = event.width / self.dessin.winfo_reqwidth()
        echelle_h = event.height / self.dessin.winfo_reqheight()
        self.largeur = event.width
        self.hauteur = event.height
        self.dessin.config(width=event.width, height=event.height)
        self.dessin.scale("element", 0, 0, echelle_l, echelle_h)

    def run_sort(self, fonction):
        def f():
            self.reset_all()
            try:
                fonction(self)
            except StopAnimation:
                self.reset_all()
                self.stop = False

        return f

    def create_buttons(self, generateurs, tris):
        label = ttk.Label(self.menu, text="Générer une liste :")
        label.pack(side='top', fill='x')
        for nom, fonction in generateurs:
            bouton = ttk.Button(self.menu, text=nom,
                                command=self.change_list(fonction))
            bouton.pack(side='top', fill='x')

        label = ttk.Label(self.menu, text="Animation :")
        label.pack(side='top', fill='x')

        frame = ttk.Frame(self.menu)
        frame.pack(side='top')
        bouton = ttk.Button(frame, text='Moins vite',
                            command=self.slowdown)
        bouton.pack(side='left', fill='x')
        bouton = ttk.Button(frame, text='Défaut',
                            command=self.reset_speed)
        bouton.pack(side='left', fill='x')
        bouton = ttk.Button(frame, text='Plus vite',
                            command=self.speedup)
        bouton.pack(side='left', fill='x')

        frame = ttk.Frame(self.menu)
        frame.pack(side='top')
        bouton = ttk.Button(frame, text='Stop',
                            command=self.interrupt)
        bouton.pack(side='left', fill='x')
        bouton = ttk.Button(frame, text='Continue',
                            command=self.resume)
        bouton.pack(side='left', fill='x')
        bouton = ttk.Button(frame, text='Un pas',
                            command=self.step)
        bouton.pack(side='left', fill='x')

        label = ttk.Label(self.menu, text="Nombre d'éléments :")
        label.pack(side='top', fill='x')
        frame = ttk.Frame(self.menu)
        frame.pack(side='top')
        bouton = ttk.Button(frame, text='Moins',
                            command=self.decrease_size)
        bouton.pack(side='left', fill='x')
        bouton = ttk.Button(frame, text='Défaut',
                            command=self.reset_size)
        bouton.pack(side='left', fill='x')
        bouton = ttk.Button(frame, text='Plus',
                            command=self.increase_size)
        bouton.pack(side='left', fill='x')

        label = ttk.Label(self.menu, text="Lancer le tri :")
        label.pack(side='top', fill='x')
        for nom, fonction in tris:
            bouton = ttk.Button(self.menu, text=nom,
                                command=self.run_sort(fonction))
            bouton.pack(side='top', fill='x')

    def create_rectangles(self):
        self.dessin.delete('element')
        return [self.dessin.create_rectangle(0, 0, 0, 0,
                fill=self.couleur, tag='element')
                for _ in self.elems]

    def redraw_list(self):
        n = len(self.elems)
        maxi = max(self.elems)
        bas = int(self.dessin["height"])
        droite = int(self.dessin["width"])
        largeur = 0.7 * droite / n
        ecart_elems = 0.3 * droite / n

        echelle = 0.9 * bas / maxi

        x = ecart_elems / 2
        for i, elem in enumerate(self.elems):
            rect = self.rectangles[i]
            self.dessin.coords(rect, x, bas, x + largeur, bas - elem * echelle)
            x += largeur + ecart_elems

        for nom, (i, text, couleur) in self.vars_by_name.items():
            self.dessin.delete(text)
            self.draw_var(nom, i, couleur)

        self.dessin.update()

    def change_list(self, fonction):
        def f():
            self.reset_all()
            self.elems = fonction(self.nb_elems)
            self.redraw_list()
        return f

    def above_rect(self, i):
        rect = self.rectangles[i]
        x1, y1, x2, _ = self.dessin.coords(rect)
        return (x1 + x2) / 2, y1 - self.marge

    def draw_var(self, nom, i, couleur='red'):
        rect = self.rectangles[i]
        x1, y1, x2, y2 = self.dessin.coords(rect)
        self.dessin.itemconfig(rect, fill=couleur)
        other_vars = self.vars_by_index.setdefault(i, [])
        other_vars.append(nom)
        text = self.dessin.create_text(
            (x1 + x2) / 2, y1 - self.marge * len(other_vars),
            text=nom, font=self.police, fill=couleur)
        self.vars_by_name[nom] = i, text, couleur

    def set_var(self, nom, i, couleur='red'):
        self.unset_var(nom)
        self.draw_var(nom, i, couleur)
        self.pace()

    def unset_var(self, nom):
        if nom in self.vars_by_name:
            i, text, _ = self.vars_by_name[nom]
            self.reset(i)
            self.dessin.delete(text)
            del self.vars_by_name[nom]
            self.vars_by_index[i].remove(nom)

    def get_var(self, nom):
        i, _, _ = self.vars_by_name[nom]
        return i

    def compare(self, i, j):
        if self.stop:
            raise StopAnimation
        # self.dessin.delete('compare')
        # rect1 = self.rectangles[i]
        # x1, y1 = self.above_rect(i)
        # x3, y3 = self.above_rect(j)
        # x2 = (x1 + x3) / 2
        # y2 = self.marge
        # self.dessin.create_line(x1, y1, x1, y2, x1, y2,
        #                         x2, y2, x3, y2, x3, y2, x3, y3,
        #                         smooth="raw", splinesteps=24,
        #                         tag='compare')
        return self.elems[i] - self.elems[j]

    def highlight(self, i, color='blue', no_delay=False):
        if self.stop:
            raise StopAnimation
        rect = self.rectangles[i]
        self.dessin.itemconfig(rect, fill=color)
        if not no_delay:
            self.pace()

    def highlight_range(self, start, end, color='blue', no_delay=False):
        for i in range(start, end):
            self.highlight(i, color, True)
        if not no_delay:
            self.pace()

    def pace(self):
        while self.stop:
            self.root.update()
            self.root.after(self.delay)    
        self.root.update()
        if self.stepwise:
            self.interrupt()
        else:
            self.root.after(self.delay)

    def reset(self, i):
        rect = self.rectangles[i]
        self.dessin.itemconfig(rect, fill=self.couleur)
        # self.root.update()

    def reset_all(self):
        while self.vars_by_name:
            nom, (i, text, _) = self.vars_by_name.popitem()
            self.reset(i)
            self.dessin.delete(text)
        for i in range(self.nb_elems):
            self.reset(i)
        self.root.update()

    def swap(self, i, j):
        self.elems[i], self.elems[j] = self.elems[j], self.elems[i]
        rect_i, rect_j = self.rectangles[i], self.rectangles[j]
        self.rectangles[i], self.rectangles[j] = rect_j, rect_i
        self.redraw_list()
        self.pace()

    def anime(self, steps):
        try:
            next(steps)
            self.root.after(self.delay, self.anime, steps)
        except StopIteration as e:
            pass

    def speedup(self):
        self.delay -= 50

    def reset_speed(self):
        self.delay = 200

    def slowdown(self):
        self.delay += 50

    def step(self):
        self.stepwise = True

    def resume(self):
        self.stepwise = False
        self.stop = False

    def interrupt(self):
        self.stop = True

    def increase_size(self):
        if self.nb_elems < self.max_elems:
            self.set_size(min(self.max_elems, self.nb_elems * 2))

    def reset_size(self):
        if self.nb_elems != self.default_elems:
            self.set_size(self.default_elems)

    def decrease_size(self):
        if self.nb_elems > self.min_elems:
            self.set_size(max(self.nb_elems // 2, self.min_elems))

    def set_size(self, nb_elems):
        self.nb_elems = nb_elems
        self.elems = aleatoire(nb_elems)
        self.rectangles = self.create_rectangles()
        self.redraw_list()

    # def dessine_boutons(self, liste_boutons):
    #     xb, yb = self.largeur_d + 2 * self.marge, self.marge
    #     res = {}
    #     for nom, fonction in liste_boutons:
    #         self.dessine_bouton((xb, yb), nom)
    #         xb2 = xb + self.largeur_b
    #         yb2 = yb + self.hauteur_b
    #         res[(xb, yb, xb2, yb2)] = (nom, fonction)
    #         yb += self.hauteur_b + self.marge
    #     mise_a_jour()
    #     return res
    #
    #     # compteurs
    #     # txt = 'affectations'
    #     # longueur = longueur_texte(txt)
    #     # hauteur = hauteur_texte() * 2 + 2
    #     # liste_boutons[txt] = [largeur_fenetre - longueur - 10, self.haut,
    #     #                       largeur_fenetre - 10, self.haut + hauteur + 10]
    #     #
    #     # txt = 'comparaisons'
    #     # liste_boutons[txt] = [largeur_fenetre - longueur - 10, self.haut + hauteur + 20,
    #     #                       largeur_fenetre - 10, self.haut + 2 * hauteur + 30]
    #
    #
    #
    #
    # def init_liste(self, lst):
    #     self.largeur_e = ((self.largeur_d
    #                        - self.ecart_elems * (self.nb_elems + 1))
    #                       / self.nb_elems)
    #
    # def dessine_cadre(self):
    #     efface('cadre')
    #     rectangle(*self.coin_haut_gauche, *self.coin_bas_droite,
    #               remplissage='white', tag='cadre')
    #
    # def dessine_bouton(self, position, nom):
    #     xb, yb = position
    #     rectangle(xb, yb, xb + self.largeur_b, yb + self.hauteur_b,
    #               couleur='black', tag='commande')
    #     texte(xb + self.largeur_b / 2, yb + self.hauteur_b / 2, nom,
    #           ancrage='center', couleur='black', tag='commande', taille='20')
    #
    # def dessinecercleStop(self):
    #     rayon = 10
    #     efface('stop')
    #     cercle(self.gauche + self.largeur_d + 10 + rayon, self.haut + rayon,
    #            rayon, 'red',
    #            'red', tag='stop')
    #     mise_a_jour()
    #
    # def dessineCompteur(self, dic_bouton, nomCompteur, valeur):
    #     """recoit le dictionnaire des emplacements, le nom du compteur
    #     le nombre a ecrire
    #     """
    #     if nomCompteur not in dic_bouton:
    #         return
    #     val = str(valeur)
    #     longueur = longueur_texte(nomCompteur)
    #     # hauteur=hauteur_texte()*2+2
    #     hautGx = dic_bouton[nomCompteur][0]
    #     hautGy = dic_bouton[nomCompteur][1]
    #     rectangle(hautGx, hautGy, dic_bouton[nomCompteur][2],
    #               dic_bouton[nomCompteur][3], 'black', remplissage='white',
    #               tag='compteur')
    #     texte(hautGx + 2, hautGy + 2, nomCompteur, couleur='black',
    #           tag='compteur')
    #     texte(hautGx + 2, hautGy + hauteur_texte() + 2, val, couleur='black',
    #           tag='compteur')
    #     mise_a_jour()
    #
    # def metDeCote(element):
    #     """" dessine l'element mis de cote en dehors du tableau
    #     """
    #     efface('deCoté')
    #     rectangle(self.gauche + self.largeur_d + largeur_element,
    #               self.haut + self.hauteur_d,
    #               self.gauche + self.largeur_d + 2 * largeur_element,
    #               self.haut + self.hauteur_d - element,
    #               remplissage='darkgreen', tag='deCoté')
    #     mise_a_jour()
    #
    # def ramene(element, position):
    #     """ met a la place position l'élément mis de coté
    #     """
    #     efface('deCoté')
    #     efface('rectangle' + str(position))
    #     debut = self.gauche + largeur_element // 2 + position * largeur_element * 1.5
    #     rectangle(debut, self.haut + self.hauteur_d, debut + largeur_element,
    #               self.haut + self.hauteur_d - element, remplissage='green',
    #               tag='rectangle' + str(position))
    #     sleep(0.1)
    #     mise_a_jour()
    #
    # def placeFinal(position, element):
    #     """ met l'element,precedemment mis de cote,
    #     a l'indice définitif position
    #     la couleur devient bleu
    #     """
    #     efface('deCoté')
    #     efface('rectangle' + str(position))
    #     debut = self.gauche + largeur_element // 2 + position * largeur_element * 1.5
    #     rectangle(debut, self.haut + self.hauteur_d, debut + largeur_element,
    #               self.haut + self.hauteur_d - element, remplissage='green',
    #               tag='rectangle' + str(position))
    #     mise_a_jour()
    #     sleep(0.1)
    #
    #
    # def dernierEchange(lst, final, deux):
    #     """ redessine les deux rectangles. L'élément indice final est a sa place definitive et sera colorié en bleu.
    #     """
    #     efface('rectangle' + str(final))
    #     efface('rectangle' + str(deux))
    #     debut = self.gauche + largeur_element // 2
    #     deb_un = debut + final * largeur_element * 1.5
    #     deb_deux = debut + deux * largeur_element * 1.5
    #
    #     rectangle(deb_deux, self.haut + self.hauteur_d,
    #               deb_deux + largeur_element,
    #               self.haut + self.hauteur_d - lst[deux], remplissage='green',
    #               tag='rectangle' + str(deux))
    #     rectangle(deb_un, self.haut + self.hauteur_d, deb_un + largeur_element,
    #               self.haut + self.hauteur_d - lst[final], remplissage='blue',
    #               tag='rectangle' + str(final))
    #     sleep(0.1)
    #     mise_a_jour()
    #
    # def clignoteOld(l, un, deux, durée=10):
    #     """ clignote les rectangles des indices un et deux de la liste l
    #     """
    #     debut = self.gauche + largeur_element // 2
    #     deb_un = debut + un * largeur_element * 1.5
    #     deb_deux = debut + deux * largeur_element * 1.5
    #     for i in range(durée):
    #         efface('rectangle' + str(un))
    #         efface('rectangle' + str(deux))
    #         sleep(0.1)
    #         mise_a_jour()
    #         rectangle(deb_un, self.haut + self.hauteur_d,
    #                   deb_un + largeur_element,
    #                   self.haut + self.hauteur_d - l[un], remplissage='green',
    #                   tag='rectangle' + str(un))
    #         rectangle(deb_deux, self.haut + self.hauteur_d,
    #                   deb_deux + largeur_element,
    #                   self.haut + self.hauteur_d - l[deux], remplissage='green',
    #                   tag='rectangle' + str(deux))
    #         sleep(0.1)
    #         mise_a_jour()
    #
    # def stopEncore():
    #     ev = donne_evenement()
    #     type_ev = type_evenement(ev)
    #     if type_ev == "ClicDroit" or type_ev == "ClicGauche":
    #         dessinecercleStop()
    #         attente_clic()
    #         efface('stop')
    #
    # def clignote(l, un, deux, durée):
    #     """ marque les rectangles des indices un et deux de la liste l
    #     """
    #     dessineIndice(l, un, 'dark green')
    #     dessineIndice(l, deux, 'dark green')
    #     sleep(durée)
    #     stopEncore()
    #     dessineIndice(l, un)
    #     dessineIndice(l, deux)
    #     mise_a_jour()
    #
    # def effaceEcran(l):
    #     for i in range(len(l)):
    #         efface('element')
    #     mise_a_jour()
    #
    # def create_rectangles(l, couleur='green'):
    #     debut = self.gauche + ecart_elements
    #
    #     for i in range(len(l)):
    #         rectangle(debut, self.haut + self.hauteur_d,
    #                   debut + largeur_element,
    #                   self.haut + self.hauteur_d - l[i],
    #                   remplissage=couleur, tag=('element', 'e' + str(i)))
    #         debut += largeur_element + ecart_elements
    #
    #     mise_a_jour()
    #
    # def dessineIndice(l, indice, couleur='green'):
    #     efface('rectangle' + str(indice))
    #     debut = self.gauche + largeur_element // 2 + largeur_element * 1.5 * indice
    #     rectangle(debut, self.haut + self.hauteur_d, debut + largeur_element,
    #               self.haut + self.hauteur_d - l[indice], remplissage=couleur,
    #               tag='rectangle' + str(indice))
    #     mise_a_jour()
    #
    # def marquePortion(debut, fin, niv, couleur):
    #     efface('portion')
    #     debut = self.gauche + largeur_element // 2 + largeur_element * 1.5 * debut
    #     fin = self.gauche + largeur_element // 2 + largeur_element * 1.5 * fin
    #     ligne(debut, self.haut + self.hauteur_d / 10 + 2 * niv, fin,
    #           self.haut + self.hauteur_d / 10 + 2 * niv, couleur,
    #           tag='portion' + str(niv))
    #
    # def menu(dic_bouton):
    #     while True:
    #         pos = attente_clic()
    #         for (x, y, z, t), fonction in dic_bouton.items():
    #             if x <= pos[0] <= z and y <= pos[1] <= t:
    #                 return fonction


if __name__ == '__main__':
    main = DemoTris()

    # commande, fonction = menu(bouton)
    # while commande != 'quitter':
    #     efface('compteur')
    #     if commande in ['aleatoire', 'permutation', 'décroissante']:
    #         efface('element')
    #         tableau = fonction(nombre_elements)
    #         create_rectangles(tableau)
    #     else:
    #         affecte, compare = fonction(tableau)
    #         dessineCompteur(bouton, 'affectations', affecte)
    #         dessineCompteur(bouton, 'comparaisons', compare)
    #     commande, fonction = menu(bouton)
    # ferme_fenetre()
