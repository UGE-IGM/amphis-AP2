#-*-coding:utf-8-*-#
from Graphique import *
#from upemtk import *
from time import sleep
from random import randint


def selection(tableau):
    vitesse=0.5 # marque les element comparé
    repetition=1
    nbaffect,nbcompar=0,0
    
    for i in range(0,len(tableau)):# pour colorer le dernier
        mini=i
        pointeElement(i,'min','red')
        for j in range(i+1,len(tableau)):
            if i<2:
                clignote(tableau,mini,j,vitesse)            
            if tableau[mini]>tableau[j]:
                mini=j
                pointeElement(mini,'min','red')
            nbcompar+=1   
            if nbcompar%10==0 and vitesse>0.01:
                vitesse *=0.8
            stopEncore()
   
        clignote(tableau,mini,i,vitesse)
        tableau[mini],tableau[i]=tableau[i],tableau[mini]
        nbaffect+=3
        dernierEchange(tableau,i,mini)  
        efface('pointe'+'min')
        
    return nbaffect,nbcompar

def insertion(tableau):
    vitesse=0.5 
    nbaffect,nbcompar=0,0

    for i in range(1,len(tableau)):
        element=tableau[i]
        nbaffect+=1
        metDeCote(element)
        j=i
        while j>0 and tableau[j-1]>element:
            nbcompar+=1
            if nbcompar%10==0 and vitesse>0.01:
                vitesse *=0.8
            dessineIndice(tableau,j,couleur='dark green')   
            sleep(vitesse)
            tableau[j]=tableau[j-1]
            dessineIndice(tableau,j)
            j-=1
            stopEncore()
        nbcompar+=1     
        tableau[j]=element
        nbaffect+=1
        ramene(element,j)
        marquePortion(0,i,0,'red')
    sleep(1)
    efface('portion')
    dessineListe(tableau,couleur='blue')
    return nbaffect,nbcompar

def bulle(tableau):
    vitesse=0.5

    nbaffect,nbcompar=0,0
  
    for i in range(0,len(tableau)): 
        for j in range(len(tableau)-1,i,-1):
            pointeElement(j,'bulle','red')
            if i<2:
                clignote(tableau,j,j-1,vitesse)
            nbcompar+=1
            if nbcompar%10==0 and vitesse>0.01:
                vitesse *=0.8
            if tableau[j-1]>tableau[j]:
                tableau[j-1],tableau[j]=tableau[j],tableau[j-1]
                nbaffect+=3
                if i<1:
                             
                    clignote(tableau,j,j-1,vitesse)
                else:
                    dessineIndice(tableau,j-1)
                    dessineIndice(tableau,j)
                    if i<2 :
                        sleep(0.1)
            stopEncore()
        dessineIndice(tableau,i,'blue')
        
    efface('pointe'+'bulle')
    return nbaffect,nbcompar

def bulleplus(tableau):
    vitesse=0.2
    debut,fin=0,len(tableau)-1
    nbaffect,nbcompar=0,0
    while debut<fin:
        
        j=fin
        dernierechange=j
        while j>debut:
            pointeElement(j,'bulle','red')
            if debut<2:
                clignote(tableau,j,j-1,vitesse)
            nbcompar+=1
            if nbcompar%10==0 and vitesse>0.01:
                vitesse *=0.8
            if tableau[j-1]>tableau[j]:
                tableau[j-1],tableau[j]=tableau[j],tableau[j-1]
                dernierechange=j
                nbaffect+=3
                if debut<1 :               
                    clignote(tableau,j,j-1,vitesse)
                else:
                    dessineIndice(tableau,j-1)
                    dessineIndice(tableau,j)
                    if debut<2 :
                        sleep(0.1)
            stopEncore()

            j-=1
        dessineIndice(tableau,debut,'blue')
        debut=dernierechange
    efface('pointe'+'bulle')
    return nbaffect,nbcompar

def bullecaillou(tableau):
    vitesse=0.1
    debut,fin=0,len(tableau)-1
    nbaffect,nbcompar=0,0
    while debut<=fin:
        #bulle remonte vers debut
        j=fin
        while j>debut:
            pointeElement(j,'bulle','red')
            if debut<2:
                clignote(tableau,j,j-1,vitesse)
            nbcompar+=1
            if tableau[j-1]>tableau[j]:
                tableau[j-1],tableau[j]=tableau[j],tableau[j-1]
                nbaffect+=3
                if debut<1:
                    clignote(tableau,j,j-1,vitesse)
                else:
                    dessineIndice(tableau,j-1)
                    dessineIndice(tableau,j)
                    if debut<2 :
                        sleep(0.1)
            j-=1
        dessineIndice(tableau,debut,'blue')
        efface('pointe'+'bulle')
        stopEncore()
        
        debut+=1 
         #caillou descend
        j=debut
        while j<fin:
            pointeElement(j,'caillou','red')
            if debut<2:
                clignote(tableau,j,j+1,vitesse)
            nbcompar+=1
            if tableau[j+1]<tableau[j]:
                tableau[j+1],tableau[j]=tableau[j],tableau[j+1]
                nbaffect+=3
                if debut<1:
                    clignote(tableau,j,j+1,vitesse)
                else:
                    dessineIndice(tableau,j+1)
                    dessineIndice(tableau,j)
                    if debut<2 :
                       sleep(0.1)
            stopEncore()
            j+=1
        dessineIndice(tableau,fin,'blue')
        efface('pointe'+'caillou')
        fin-=1   
   
    return nbaffect,nbcompar


def bullecaillouplus(tableau):
    vitesse=0.1
    debut,fin=0,len(tableau)-1
    nbaffect,nbcompar=0,0
    while debut<fin:
        #bulle remonte
        j=fin
        dernierechange=j
        while j>debut:
            pointeElement(j,'bulle','red')
            if debut<2:
                clignote(tableau,j,j-1,vitesse)
            nbcompar+=1
            if tableau[j-1]>tableau[j]:
                tableau[j-1],tableau[j]=tableau[j],tableau[j-1]
                dernierechange=j
                nbaffect+=3
                if debut<1 :                             
                    clignote(tableau,j,j-1,vitesse)
                else:
                    dessineIndice(tableau,j-1)
                    dessineIndice(tableau,j)
                    if debut<2 :
                        sleep(0.1)
            stopEncore()
            j-=1
            efface('pointe'+'bulle')
        #dessineIndice(tableau,debut,'blue')
        dessineIndice(tableau,j,'blue')
        debut=dernierechange
       
         #caillou descend
        j=debut
        while j<fin:           
            pointeElement(j,'caillou','red')
            if debut<2:
                clignote(tableau,j,j+1,vitesse)
            nbcompar+=1
            if tableau[j+1]<tableau[j]:
                tableau[j+1],tableau[j]=tableau[j],tableau[j+1]
                dernierechange=j
                nbaffect+=3
               
                dessineIndice(tableau,j+1)
                dessineIndice(tableau,j)
                if debut<2 :
                    sleep(0.1)
                stopEncore()
            j+=1
        dessineIndice(tableau,fin,'blue') 
        efface('pointe'+'caillou')

        fin=dernierechange  
       
    
    return nbaffect,nbcompar

def shell(tableau):
    vitesse=0.1
    n=len(tableau)
    incr=n//2
    nbaffect,nbcompar=0,0
    while(incr>0):
        for i in range(incr,n):
            #ordonne tableau[i] et ceux situiés tous les incr avant
            for j in range(i-incr,-1,-incr):
                marquePortion(j,j+incr,0,'red')
                nbcompar+=1
               
                clignote(tableau,j,j+incr,vitesse)
                if incr<10:
                    vitesse=0.01

                if tableau[j]>tableau[j+incr]:
                    clignote(tableau,j,j+incr,0.2)
                    
                    sleep(0.05)
                    nbaffect+=3
                    tableau[j],tableau[j+incr]=tableau[j+incr],tableau[j]
                    if incr>10:
                        clignote(tableau,j,j+incr,0.2)
                    dessineIndice(tableau,j+incr)
                    dessineIndice(tableau,j)
                    efface('portion')
                    stopEncore()
                else:
                    efface('portion')
                    break
                stopEncore()    
        incr//=2
    dessineListe(tableau,'blue')
    return nbaffect,nbcompar

def triRapide(tableau):
        a,c=triRapideAux(tableau,0,len(tableau)-1) 
        return a,c
def triRapideAux(tableau,debut,fin,niveau=0):
# niveau indique le numero du sous appel recursif
    affect,compar=0,0
    if debut<fin:
        marquePortion(debut,fin,niveau,'red')
        pivot=randint(debut,fin)
        #metDeCote(tableau[pivot])
        position,a,c=partition(tableau,debut,fin,pivot)
        affect+=a
        compar+=c
        #ramene(tableau[position],position)
        dessineIndice(tableau,position,'blue')
        if fin-debut >40:
            sleep(0.2)
        stopEncore()
        a,c= triRapideAux(tableau, debut,position-1,niveau+1)
        affect+=a
        compar+=c
        a,c= triRapideAux(tableau, position+1,fin,niveau+1)
        affect+=a
        compar+=c
    elif debut==fin:
        dessineIndice(tableau,debut,'blue')
    efface('portion'+str(niveau))
    return affect,compar

def partition(tableau,debut,fin,pivot):
    vitesse=0.5
    if fin-debut<40:
        vitesse=0.1
    affect,compar=0,0
   # marquePortion(debut,fin,'red')
    clignote(tableau,debut,pivot,vitesse)
    tableau[debut],tableau[pivot]=tableau[pivot],tableau[debut]
    clignote(tableau,debut,pivot,vitesse)
    dessineIndice(tableau,debut,'dark green')
    inf,sup=debut+1,fin
    dist=fin-debut
    while inf<=sup:
        if dist >20:
            pointeElement(inf,'inf','dark green')
            pointeElement(sup,'sup','dark green')
        compar+=1
        while  inf<=sup and tableau[inf]<=tableau[debut]:
            inf+=1
            compar+=1
            if dist>20:
                pointeElement(inf,'inf','dark green')
           
            stopEncore()
        compar+=1
        while tableau[sup]>tableau[debut]:
            sup-=1
            compar+=1
            if dist >20:
                pointeElement(sup,'sup','dark green')
            #clignote(tableau,inf,sup,vitesse//5)
            stopEncore()
        if inf<sup:
            tableau[inf],tableau[sup]=tableau[sup],tableau[inf]
            affect+=3
            clignote(tableau,inf,sup,vitesse)
            efface('pointe'+'inf')
            efface('pointe'+'sup')
            inf+=1
            sup-=1
            stopEncore()

    efface('pointe'+'inf')
    efface('pointe'+'sup')
    stopEncore()
    tableau[debut],tableau[sup]=tableau[sup],tableau[debut]
    affect+=3
    clignote(tableau,sup,debut,vitesse)
    efface('portion')
    return sup,affect,compar
 
def fusion(lst,debut,frontiere,fin,niveau):
    """ fusionne les parties tries de lst 
    indices
    debut, frontiere compris
    et
    frontiere+1, fin compris
    """
    affect,compar=0,0
    lstintermediaire=[0]*(fin-debut+1)
    indUn=debut
    indDeux=frontiere+1
    remplit=0
#copie ordonnee tant qu'aucune partie n'est vide
    while indUn<=frontiere and indDeux<=fin:
        if lst[indUn]<lst[indDeux]:
            lstintermediaire[remplit]=lst[indUn]
            indUn+=1
        else:
            lstintermediaire[remplit]=lst[indDeux]
            indDeux+=1
        remplit+=1
        affect+=1
        compar+=1
#copie de la partie restante
    if indUn>frontiere :
        while indDeux<=fin:
            lstintermediaire[remplit]=lst[indDeux]
            indDeux+=1
            remplit+=1
            affect+=1
    else:
        while indUn<=frontiere:
            lstintermediaire[remplit]=lst[indUn]
            indUn+=1
            remplit+=1
            affect+=1
#recopie dans la partie de lst
    lst[debut:fin+1]=lstintermediaire[:]
    if niveau==0:
        dessineListe(lst,'blue')
    else:
        dessineListe(lst)
    sleep(0.5)
    affect+=fin-debut
    return affect,compar

def triFusionAux(lst,debut,fin,niveau=0):
# niveau indique le numero du sous appel recursif
    a,c=0,0
    affect,comp=0,0
    if debut<fin:
        marquePortion(debut,fin+1,niveau,'red')
        milieu=(debut+fin)//2     
        a,c= triFusionAux(lst,debut,milieu,niveau+1)
        affect+=a
        comp+=c
        a,c=  triFusionAux(lst,milieu+1,fin,niveau+1)
        affect+=a
        comp+=c
        a,c=  fusion(lst,debut,milieu,fin,niveau)
        affect+=a
        comp+=c
        efface('portion'+str(niveau))
    return  affect,comp

def triFusion(tableau):
    effaceEcran(tableau)
    #l=[2*x//3 for x in tableau]
    l=1*tableau
    dessineListe(l)
    a,c=triFusionAux(l,0,len(tableau)-1) 

    return a,c

