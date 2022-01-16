class ListeObservable(list):
    def __init__(self, *args):
        """Initialisation de la liste observable de la même manière qu'une
        liste Python "traditionnelle"."""
        list.__init__(self, *args)
        self.observateurs = list()

    def enregistrer(self, obs):
        """Enregistre un observateur qui sera prévenu des changements d'état
        de la liste."""
        self.observateurs.append(obs)

    def echanger(self, i, j):
        """Echange les éléments en positions i et j."""
        self[i], self[j] = self[j], self[i]
        for obs in self.observateurs:
            obs.notify(self, "echange", (i, j))

    def reinserer(self, i, j):
        """Réinsère l'élément self[i] en position j."""
        e = self[i]
        if i < j:  # décaler les éléments d'une position vers la gauche
            for k in range(i, j):
                self[k] = self[k + 1]
        else:  # décaler les éléments d'une position vers la droite
            k = i
            while k > j:
                self[k] = self[k - 1]
                k = k - 1
        self[j] = e
        for obs in self.observateurs:
            obs.changement_de_contenu(self)

    """On redéfinit toutes les méthodes qui changent la liste; elles feront
    exactement la même chose que dans la classe list, mais préviendront en
    outre les observateurs qu'un changement de contenu s'est produit."""

    def append(self, element):
        """Cf. documentation de list.append()."""
        list.append(self, element)
        for obs in self.observateurs:
            obs.changement_de_contenu(self)

    def clear(self):
        """Cf. documentation de list.clear()."""
        list.clear(self)
        for obs in self.observateurs:
            obs.changement_de_contenu(self)

    def extend(self, iterable):
        """Cf. documentation de list.extend()."""
        list.extend(self, iterable)
        for obs in self.observateurs:
            obs.changement_de_contenu(self)

    def insert(self, position, element):
        """Cf. documentation de list.insert()."""
        list.insert(self, position, element)
        for obs in self.observateurs:
            obs.changement_de_contenu(self)

    def pop(self, position: int = 0):
        """Cf. documentation de list.pop()."""
        res = list.pop(self, position)
        for obs in self.observateurs:
            obs.changement_de_contenu(self)
        return res

    def remove(self, element):
        """Cf. documentation de list.remove()."""
        list.remove(self, element)
        for obs in self.observateurs:
            obs.changement_de_contenu(self)

    def sort(self, key=None, reverse=False):
        """Cf. documentation de list.sort()."""
        list.sort(self, key=key, reverse=reverse)
        for obs in self.observateurs:
            obs.changement_de_contenu(self)

    def reverse(self):
        """Cf. documentation de list.reverse()."""
        list.reverse(self)
        for obs in self.observateurs:
            obs.changement_de_contenu(self)

    # def __setitem__(self, position, element):
    # """Permet d'observer les affectations réalisées à l'aide de l'opérateur
    # []."""
    # list.__setitem__(self, position, element)
    # for obs in self.observateurs:
    # obs.changement_de_contenu(self)
