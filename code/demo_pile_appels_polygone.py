def distance(p, q):
    '''Renvoie la longueur du côté
    defini par p et q.'''
    return ((p[0] - q[0]) ** 2 
           + (p[1] - q[1]) ** 2) ** 0.5

def perimetre(P):
    '''Renvoie le périmètre du polygone 
    défini par la liste P de points.'''
    retval = 0
    for i in range(-1, len(P) - 1):
        retval += distance(P[i], P[i+1])
    return retval

perimetre([(0, 0), (0, 1), (1, 1), (1, 0)])