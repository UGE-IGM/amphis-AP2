def hanoi(tours, n, source=0, interm=1, dest=2):
    if n == 0:
        return
    hanoi(tours, n-1, source, dest, interm)
    disque = tours[source].pop()
    tours[dest].append(disque)
    print(source, '->', dest)
    hanoi(tours, n-1, interm, source, dest)

def hanoi_iter(tours, n, source=0, interm=1, dest=2):
    if n == 0:
        return
    while len(tours[dest] < n):
        ...

nb_tours = 3
mes_tours = [list(range(nb_tours, -1, -1)), [],[]]
hanoi(mes_tours, nb_tours)

def hanoi_bis(tours, n, source=0, interm=1, dest=2):
    if n == 0:
        return
    hanoi_bis(tours, n-1, source, dest, interm)
    print(tours)
    assert(tours[n-1] == source)
    tours[n-1] = dest
    print("disque {} : {} -> {}".format(n, source, dest))
    hanoi_bis(tours, n-1, interm, source, dest)

def hanoi_iter(n, source=0, interm=1, dest=2):
    tours = [source] * n
    cpt = 0
    if n % 2 == 0:
        d = 1
    else:
        d = -1
    print(tours)
    while tours[:n] != [dest] * n and cpt < 10:
        cpt += 1
        tours[0] = (tours[0] + d) % 3
        print(tours)
        for i in range(1, n):
            if tours[i] != tours[0]:
                tours[i] = 3 - tours[i] - tours[0]
                break
        print(tours)

hanoi_bis([0, 0, 0], 3)
hanoi_iter(4)
