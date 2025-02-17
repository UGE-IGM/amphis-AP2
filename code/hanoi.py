from upemtk import *

nb_disques = 4
nb_tours = 3
largeur = 1000
hauteur = 450
marge = 50
altitude_sol = hauteur - 50
hauteur_tours = hauteur - 2 * marge
hauteur_disques = (hauteur_tours - 30) / nb_disques

unit_diam = (largeur - 2*marge) / nb_tours / nb_disques
demi_intervalle = (largeur - 2*marge) / (2*nb_tours)
pos_tours = [marge + demi_intervalle + 2 * i * demi_intervalle
             for i in range(nb_tours)]

contenu_tours = []
for num_tour in range(nb_tours):
    contenu_tours.append([])
for disque in range(nb_disques):
    contenu_tours[0].append(unit_diam * (nb_disques - disque))


def dessine_sol():
    ligne(0, altitude_sol, largeur, altitude_sol, epaisseur=3)


def dessine_disque(diametre, tour, rang):
    y = altitude_sol - rang * hauteur_disques
    rectangle(pos_tours[tour] - diametre / 2, y,
              pos_tours[tour] + diametre / 2, y - hauteur_disques,
              remplissage='green',
              tag='disques')


def dessine_disques():
    efface('disques')
    for i, tour in enumerate(contenu_tours):
        for j, disque in enumerate(tour):
            dessine_disque(disque, i, j)


def deplace_disque(source, dest):
    if not contenu_tours[source]:
        raise IndexError
    if (contenu_tours[dest]
        and contenu_tours[source][-1] > contenu_tours[dest][-1]):
            raise ValueError
    disque = contenu_tours[source].pop()
    contenu_tours[dest].append(disque)


def traite_clic(x):
    for tour in range(nb_tours - 1):
        if x < (pos_tours[tour + 1] + pos_tours[tour]) / 2:
            return tour
    return nb_tours - 1


def dessine_tours(selection=None):
    efface('tours')
    y1 = altitude_sol
    y2 = altitude_sol - hauteur_tours
    for num_tour in range(nb_tours):
        if num_tour == selection:
            c = 'blue'
        else:
            c = 'black'
        x = pos_tours[num_tour]
        ligne(x, y1, x, y2,
              epaisseur=3, tag='tours', couleur=c)


def joue():
    trace = []

    while len(contenu_tours[nb_tours-1]) != nb_disques:
        # attend la sélection d'une tour source non vide
        x, _, t_clic = attente_clic()
        if t_clic == 'ClicDroit':
            texte(largeur / 2, hauteur - 20, "Clic pour quitter",
                  ancrage='c')
            break
        source = traite_clic(x)
        efface('erreur')
        if not contenu_tours[source]:
            continue
        dessine_tours(source)

        # attend la sélection d'une tour destination
        x, _, t_clic = attente_clic()
        if t_clic == 'ClicDroit':
            break
        dest = traite_clic(x)
        try:
            deplace_disque(source, dest)
        except ValueError:  # déplacement contraire aux règles
            texte(largeur / 2, hauteur - 20, "Déplacement interdit",
                  couleur='red', tag='erreur', ancrage='c')
        finally:
            trace.append((source, dest))
        dessine_disques()
        dessine_tours()
        mise_a_jour()

    if len(contenu_tours[-1]) == nb_disques:
        texte(largeur / 2, hauteur - 20, 
              "Gagné en {} mouvements".format(len(trace)),
              couleur='green', tag='erreur', ancrage='c')
    return trace


if __name__ == '__main__':
    cree_fenetre(largeur, hauteur)
    dessine_sol()
    dessine_disques()
    dessine_tours()
    trace = joue()
    attente_clic()
    ferme_fenetre()
    print(trace)
