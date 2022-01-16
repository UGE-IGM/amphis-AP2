#-*-coding:utf-8-*-#

from upemtk import *
from Graphique import *
from lesAlgo import *
from random import randint
from time import sleep

def init(l):  
   
    n=HAUT*2//3  #valeur maximum pour laisser la place aux textes
    for i in range(len(l)):
        l[i]=randint(5,n)
    dessineListe(l)

def decroissante(l):
    n=HAUT*2//3
    for i in range(len(l)):
        l[i]=randint(5,n) 
    l.sort(reverse=True)
    dessineListe(l)

def menu(dic_bouton):
    while True:
        pos=attente_clic()
        for bout in dic_bouton:
            if dic_bouton[bout][0]<=pos[0]<=dic_bouton[bout][2] and \
            dic_bouton[bout][1]<=pos[1]<=dic_bouton[bout][3]:
                return bout


    
if __name__=='__main__': 
    cree_fenetre(LONGFENETRE,HAUTFENETRE)
    placeEcran()
  
   #rectangle(ECRANGH[X],ECRANGH[Y],ECRANGH[X]+LONG,ECRANGH[Y]+HAUT,remplissage='white',tag='ecran')
   # input()
    bouton={}
    PlaceBoiteCommande(bouton)    
    tableau=[]
    copie=[]
    dicofonctions={'selection':selection,'insertion':insertion,'bulle':bulle,
                   'bulle+':bulleplus,'bullecaillou':bullecaillou,
                   'bullecaillou+':bullecaillouplus
                   ,'shell':shell,'rapide':triRapide,'fusion':triFusion}
    commande=menu(bouton)
    while commande!='Quitter':        
#        effaceCompteur()        
        efface('compteur')
        if commande=='init':
            tableau=[0]*NOMBRE
            effaceEcran(tableau)
            init(tableau )           
            copie=tableau[:]
        if commande=='decr':
            tableau=[0]*NOMBRE
            effaceEcran(tableau)
            decroissante(tableau)           
            copie=tableau[:]       
        elif commande in dicofonctions:
            if copie==[]:
                print("rien a trier")
            else:
                tableau=copie[:]
                dessineListe(tableau)
                affecte,compare=dicofonctions[commande](tableau)
                dessineCompteur(bouton,'affectations',affecte)
                dessineCompteur(bouton,'comparaisons',compare)

        commande=menu(bouton)  
    ferme_fenetre() 
     

       
          
 
