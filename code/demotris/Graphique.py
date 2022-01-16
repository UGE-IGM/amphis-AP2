#-*-coding:utf-8-*-#
from upemtk import *
from time import sleep

#  Dimensions de la fenetre
LONGFENETRE= 1300
HAUTFENETRE= 700

HAUTBOITE= 50
ENTREBOITE=20

(X,Y)=(0,1)


# Points  de la fenetre de jeu 

#coin Haut gauche de l'ecran de jeu
ECRANGH= [10,10]
X,Y=0,1
BOITE= [ECRANGH[0],HAUTFENETRE-3*HAUTBOITE]

# Dimensions de l'ecran de jeu */
LARGEUR=6
NOMBRE=100
LONG= NOMBRE*LARGEUR*1.5+LARGEUR//2 #pour 100 valeurs
HAUT=HAUTFENETRE-4*HAUTBOITE
def placeEcran():
    efface('ecran')
    rectangle(ECRANGH[X],ECRANGH[Y],ECRANGH[X]+LONG,ECRANGH[Y]+HAUT,remplissage='white',tag='ecran')


def dessineBoite(dic_bouton,nomBouton):
    rectangle(dic_bouton[nomBouton][0],dic_bouton[nomBouton][1],dic_bouton[nomBouton][2],dic_bouton[nomBouton][3],'black',remplissage='white',tag='commande')
    texte(dic_bouton[nomBouton][0]+2,dic_bouton[nomBouton][1] +2,nomBouton,couleur='black',tag='commande')

def dessinecercleStop():
    rayon=10
    efface('stop')
    cercle(ECRANGH[0]+LONG+10+rayon,ECRANGH[Y]+rayon,rayon,'red','red',tag='stop')
    mise_a_jour()

def dessineCompteur(dic_bouton,nomCompteur,valeur):
    """recoit le dictionnaire des emplacements, le nom du compteur
    le nombre a ecrire
    """
    if nomCompteur not in dic_bouton:
      return          
    val=str(valeur)
    longueur=longueur_texte(nomCompteur)
    #hauteur=hauteur_texte()*2+2  
    hautGx=dic_bouton[nomCompteur][0]
    hautGy=dic_bouton[nomCompteur][1]
    rectangle(hautGx,hautGy,dic_bouton[nomCompteur][2],dic_bouton[nomCompteur][3],'black',remplissage='white',tag='compteur')
    texte(hautGx+2,hautGy+2,nomCompteur,couleur='black',tag='compteur')
    texte(hautGx+2,hautGy+hauteur_texte()+2,val,couleur='black',tag='compteur')
    mise_a_jour()
def effaceCompteur():
    efface('compteur')

def PlaceBoiteCommande(dictionnaire):
    # tirage du contenu de la liste 
    #aleatoire
    txt='init'
    longueur=longueur_texte(txt)+2
    dictionnaire['init']=[BOITE[X],BOITE[Y],BOITE[X]+longueur,BOITE[Y]+HAUTBOITE]  
     #decroissant 
    txt='decr'
    longueur=longueur_texte(txt)+2
    dictionnaire['decr']=[BOITE[X],BOITE[Y]+HAUTBOITE+10,BOITE[X]+longueur,BOITE[Y]+2*HAUTBOITE+10]  
    #choix de tri
#selection
    HautX=BOITE[X]+longueur+ENTREBOITE
    txt='selection'
    longueur=longueur_texte(txt)+2
    dictionnaire[txt]=[HautX,BOITE[Y],HautX+longueur,BOITE[Y]+HAUTBOITE]
 #insertion
    txt='insertion'
    longueur=longueur_texte(txt)+2
    dictionnaire[txt]=[HautX,BOITE[Y]+HAUTBOITE+10,HautX+longueur,BOITE[Y]+2*HAUTBOITE+10] 
 #bulle
    HautX=HautX+longueur+ENTREBOITE
    txt='bulle'
    longueur=longueur_texte(txt)+2
    dictionnaire[txt]=[HautX,BOITE[Y],HautX+longueur,BOITE[Y]+HAUTBOITE]
#bulle ameliore
    txt='bulle+'
    longueur=longueur_texte(txt)+2
    dictionnaire[txt]=[HautX,BOITE[Y]+HAUTBOITE+10,HautX+longueur,BOITE[Y]+2*HAUTBOITE+10]
#bullecaillou
    HautX=HautX+longueur+ENTREBOITE
    txt='bullecaillou'
    longueur=longueur_texte(txt)+2
    dictionnaire[txt]=[HautX,BOITE[Y],HautX+longueur,BOITE[Y]+HAUTBOITE]
#bullecaillou+
    
    txt='bullecaillou+'
    longueur=longueur_texte(txt)+2
    dictionnaire[txt]=[HautX,BOITE[Y]+HAUTBOITE+10,HautX+longueur,BOITE[Y]+2*HAUTBOITE+10]

#shell
    txt='shell'
    HautX=HautX+longueur+ENTREBOITE
    longueur=longueur_texte(txt)+2
    dictionnaire[txt]=[HautX,BOITE[Y],HautX+longueur,BOITE[Y]+HAUTBOITE]
#quicksort
    txt='rapide'
    longueur=longueur_texte(txt)+2
    dictionnaire[txt]=[HautX,BOITE[Y]+HAUTBOITE+10,HautX+longueur,BOITE[Y]+2*HAUTBOITE+10]
#tri Fusion
    HautX=HautX+longueur+ENTREBOITE
    txt='fusion'
    longueur=longueur_texte(txt)+2
    dictionnaire[txt]=[HautX,BOITE[Y],HautX+longueur,BOITE[Y]+HAUTBOITE]
   
#bouton pour Quitter  
    txtFin='Quitter'
    HautX=LONGFENETRE-(longueur_texte(txtFin)+ENTREBOITE+4)
    dictionnaire['Quitter']=[ HautX,BOITE[Y],HautX+(longueur_texte(txtFin)+4),BOITE[Y]+HAUTBOITE]

    for nom in dictionnaire:
        dessineBoite(dictionnaire,nom)
#compteurs
    txt='affectations'
    longueur=longueur_texte(txt)
    hauteur=hauteur_texte()*2+2 
    dictionnaire[txt]=[LONGFENETRE-longueur-10,ECRANGH[Y],LONGFENETRE-10,ECRANGH[Y]+hauteur+10]
    
    txt='comparaisons'
    dictionnaire[txt]=[LONGFENETRE-longueur-10,ECRANGH[Y]+hauteur+20,LONGFENETRE-10,ECRANGH[Y]+2*hauteur+30]
   
 
 
    mise_a_jour()
  
def metDeCote(element):
    """" dessine l'element mis de cote en dehors du tableau
    """
    efface('deCoté')
    rectangle(ECRANGH[X]+LONG+LARGEUR,ECRANGH[Y]+HAUT,ECRANGH[X]+LONG+2*LARGEUR,ECRANGH[Y]+HAUT-element,remplissage='darkgreen',tag='deCoté')
    mise_a_jour()
def ramene(element,position):
    """ met a la place position l'élément mis de coté
    """
    efface('deCoté')
    efface('rectangle'+str(position))
    debut=ECRANGH[X]+LARGEUR//2+position*LARGEUR*1.5
    rectangle(debut,ECRANGH[Y]+HAUT,debut+LARGEUR,ECRANGH[Y]+HAUT-element,remplissage='green',tag='rectangle'+str(position))
    sleep(0.1)
    mise_a_jour()

def placeFinal(position,element):
    """ met l'element,precedemment mis de cote,
    a l'indice définitif position 
    la couleur devient bleu
    """
    efface('deCoté')
    efface('rectangle'+str(position))
    debut=ECRANGH[X]+LARGEUR//2+position*LARGEUR*1.5
    rectangle(debut,ECRANGH[Y]+HAUT,debut+LARGEUR,ECRANGH[Y]+HAUT-element,remplissage='green',tag='rectangle'+str(position))
    mise_a_jour()
    sleep(0.1)

def pointeElement(i,txt,couleur):
    efface('pointe'+txt)
    x=LARGEUR*0.5+ECRANGH[X]+i*LARGEUR*1.5
    yh=ECRANGH[Y]+HAUT/7
    yb=ECRANGH[Y]+HAUT/6
    fleche(x,yh,x,yb,couleur,epaisseur=2,tag='pointe'+txt)
    lon=longueur_texte(txt)
    texte(x-lon//2,ECRANGH[Y]+HAUT/10,txt,couleur,taille=12,tag='pointe'+txt)
def dernierEchange(lst,final,deux):
    """ redessine les deux rectangles. L'élément indice final est a sa place definitive et sera colorié en bleu.
    """
    efface('rectangle'+str(final))
    efface('rectangle'+str(deux))
    debut=ECRANGH[X]+LARGEUR//2
    deb_un=debut+final*LARGEUR*1.5
    deb_deux=debut+deux*LARGEUR*1.5

    rectangle(deb_deux,ECRANGH[Y]+HAUT,deb_deux+LARGEUR,ECRANGH[Y]+HAUT-lst[deux],remplissage='green',tag='rectangle'+str(deux))
    rectangle(deb_un,ECRANGH[Y]+HAUT,deb_un+LARGEUR,ECRANGH[Y]+HAUT-lst[final],remplissage='blue',tag='rectangle'+str(final))
    sleep(0.1)
    mise_a_jour()

def clignoteOld(l,un,deux,durée=10):
    """ clignote les rectangles des indices un et deux de la liste l
    """
    debut=ECRANGH[X]+LARGEUR//2
    deb_un=debut+un*LARGEUR*1.5
    deb_deux=debut+deux*LARGEUR*1.5
    for i in range(durée):
        efface('rectangle'+str(un))
        efface('rectangle'+str(deux))
        sleep(0.1)
        mise_a_jour()
        rectangle(deb_un,ECRANGH[Y]+HAUT,deb_un+LARGEUR,ECRANGH[Y]+HAUT-l[un],remplissage='green',tag='rectangle'+str(un))
        rectangle(deb_deux,ECRANGH[Y]+HAUT,deb_deux+LARGEUR,ECRANGH[Y]+HAUT-l[deux],remplissage='green',tag='rectangle'+str(deux))
        sleep(0.1)
        mise_a_jour()

def stopEncore():
    ev = donne_evenement()
    type_ev = type_evenement(ev)
    if type_ev == "ClicDroit" or type_ev == "ClicGauche":
        dessinecercleStop()
        attente_clic()
        efface('stop')


def clignote(l,un,deux,durée):
    """ marque les rectangles des indices un et deux de la liste l
    """
    dessineIndice(l,un,'dark green')
    dessineIndice(l,deux,'dark green')
    sleep(durée)
    stopEncore()
    dessineIndice(l,un)
    dessineIndice(l,deux)
    mise_a_jour()

def effaceEcran(l):
 for i in range(len(l)):
        efface('rectangle'+str(i))
        mise_a_jour()
 
def dessineListe(l,couleur='green'):
    taille=len(l)
    debut=ECRANGH[X]+LARGEUR//2
   # LARGEURtemp=ECRANGH[X]//taille*1.5

    for i in range(len(l)):    
        efface('rectangle'+str(i))
        rectangle(debut,ECRANGH[Y]+HAUT,debut+LARGEUR,ECRANGH[Y]+HAUT-l[i],remplissage=couleur,tag='rectangle'+str(i))
        debut=debut+LARGEUR*1.5
        mise_a_jour()
    
    mise_a_jour()

def dessineIndice(l,indice,couleur='green'):
    efface('rectangle'+str(indice))
    debut=ECRANGH[X]+LARGEUR//2+LARGEUR*1.5*indice
    rectangle(debut,ECRANGH[Y]+HAUT,debut+LARGEUR,ECRANGH[Y]+HAUT-l[indice],remplissage=couleur,tag='rectangle'+str(indice))
    mise_a_jour()

def marquePortion(debut,fin,niv,couleur):
    efface('portion')
    debut=ECRANGH[X]+LARGEUR//2+LARGEUR*1.5*debut
    fin=ECRANGH[X]+LARGEUR//2+LARGEUR*1.5*fin
    ligne(debut,ECRANGH[Y]+HAUT/10+2*niv,fin,ECRANGH[Y]+HAUT/10+2*niv,couleur,tag='portion'+str(niv))
