from random import randint
from upemtk import *
from time import sleep


def coord_case(x, y):
    i = (y - marge) // taille_px
    j = (x - marge) // taille_px
    return i, j


def dessine_pixel(i, j, couleur):
    efface_pixel(i, j)
    rectangle(marge + j * taille_px,
              marge + i * taille_px,
              marge + (j+1) * taille_px,
              marge + (i+1) * taille_px,
              remplissage=couleur,
              tag='ecran' + str(i) + '*' + str(j))


def efface_pixel(i, j):
    efface('ecran' + str(i) + '*' + str(j))


def dessine_cercle(i, j, c):
    efface_cercle(i, j)
    cercle(marge + j*taille_px + taille_px/2,
           marge + i*taille_px + taille_px/2,
           taille_px/4,
           couleur=c, remplissage=c,
           tag='cercle' + str(i) + '*' + str(j))
    mise_a_jour()


def efface_cercle(i, j):
    efface('cercle' + str(i) + '*' + str(j))


def dessine_ecran(ecran, couleurs):
    for i in range(len(ecran)):
        for j in range(len(ecran[i])):
            dessine_pixel(i, j, couleurs[ecran[i][j]])
    mise_a_jour()


def clignote(i, j, nv, nbfois=5, temps=0.05):
    """ verifie que la nouvelle valeur n'est pas egale a l'ancienne
    puis clignote 
    la derniere couleur l'ancienne
    """
    if ecran[i][j] == nv:
        return
    nouvelle = couleurs[nv]
    ancienne = couleurs[ecran[i][j]]
    for _ in range(nbfois):
        for c in (nouvelle, ancienne):
            dessine_pixel(i, j, c)
            mise_a_jour()
            sleep(temps)


def dessine_fleche(i, j, c, direction):
    efface_fleche(i, j)
    x_centre = marge + j*taille_px + taille_px/2
    y_centre = marge + i*taille_px + taille_px/2
    dx = taille_px * 0.2 * direction[1]
    dy = taille_px * 0.2 * direction[0]
    fleche(x_centre - dx, y_centre - dy, x_centre + dx, y_centre + dy,
           tag='fleche' + str(i) + '*' + str(j), epaisseur=2, couleur=c)
    mise_a_jour()


def efface_fleche(i, j):
    efface('fleche' + str(i) + '*' + str(j))


def remplit(i, j, c, pause=False, temps=0.5):
    """change recursivement la c de la zone contenant le point (i,j)
    si pause==0 attend un clic entre chaque point
    """
    if pause:
        temps *= 0.8
    
    if ecran[i][j] == c:
        return

    clignote(i, j, c, temps=temps/10)
    ancienne = ecran[i][j]
    ecran[i][j] = c
    dessine_pixel(i, j, couleurs[c])
    dessine_cercle(i, j, couleurs[ancienne])

    for d in directions:
        if pause == 0:
            _, _, t = attente_clic()
            if t == 'ClicDroit':
                exit()
        else:
            if type_evenement(donne_evenement()) == 'ClicDroit':
                exit()
            sleep(temps)

        efface_fleche(i, j)
        mise_a_jour()

        ii, jj = i + d[0], j + d[1]
        dessine_fleche(i, j, couleurs[c], d)
        if 0 <= ii < len(ecran) and 0 <= jj < len(ecran[j]):
            if ecran[ii][jj] == ancienne:
                remplit(ii, jj, c, pause, temps)

    if pause == 0:
        _, _, t = attente_clic()
        if t == 'ClicDroit':
            exit()
    else:
        sleep(temps)

    efface_cercle(i, j)
    mise_a_jour()


def nouvelle_couleur(i, j):
    offset = randint(1, len(couleurs)-1)
    return (ecran[i][j] + offset) % len(couleurs)


if __name__ == '__main__':
    ecran = [
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2],
        [2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 3, 3, 3, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 3, 3, 3, 2, 3, 3, 2, 2],
        [2, 2, 2, 2, 3, 3, 3, 2, 2, 2, 3, 2],
        [2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 6, 6, 6, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 6, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 6, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 5, 5, 5, 5, 5, 5, 2, 2, 2, 2, 2]]

    couleurs = [
        'black',
        'yellow',
        'green',
        'white',
        'blue',
        'gray',
        'red',
        'magenta',
        'brown',
        'light blue',
        'pink']

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    nb_lignes = len(ecran)
    nb_col = len(ecran[0])
    marge = 10
    taille_px = 50
    cree_fenetre(2 * marge + nb_col * taille_px,
                 2 * marge + nb_lignes * taille_px)
    dessine_ecran(ecran, couleurs)

    remplit(8, 6, 4)

    x, y, t_clic = attente_clic()
    while t_clic == 'ClicGauche':
        i, j = coord_case(x, y)
        nouv = nouvelle_couleur(i, j)
        remplit(i, j, nouv, pause=1)
        x, y, t_clic = attente_clic()

    ferme_fenetre()
