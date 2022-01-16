def fusion(lst,debut,frontiere,fin):
    """ fusionne les parties tries de lst 
    indices
    debut, frontiere compris
    et
    frontiere+1, fin compris
    """
    
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
    
#copie de la partie restante
    if indUn>frontiere :
        while indDeux<=fin:
            lstintermediaire[remplit]=lst[indDeux]
            indDeux+=1
            remplit+=1
    else:
        while indUn<=frontiere:
            lstintermediaire[remplit]=lst[indUn]
            indUn+=1
            remplit+=1

#recopie dans la partie de lst
    lst[debut:fin+1]=lstintermediaire[:]

def trifusion(lst,debut=0,fin=None):
    if fin==None:
        fin=len(lst)-1

    if (debut<fin):
        milieu=(debut+fin)//2
        print(lst[debut:milieu+1])
        print(lst[milieu+1:fin+1])
        trifusion(lst,debut,milieu)
        trifusion(lst,milieu+1,fin)
        fusion(lst,debut,milieu,fin)
        input()
        print(lst[debut:fin+1])

lst=[17,14,10, 3,12,15,22,7,10,11,21,23,28,6,0,42,9]

print(lst)
input()
trifusion(lst)
print(lst)

