def bubble_sort(lst):
    # lst = lst[:]
    for i in range(len(lst)-1):
        for j in range(len(lst)-1, i, -1):
            if lst[j-1] > lst[j]:
                lst[j-1], lst[j] = lst[j], lst[j-1]
    return lst


def bubble_sort_plus(lst):
    # lst = lst[:]
    i = 0
    while i < len(lst)-1:
        dernier = len(lst)-1
        for j in range(len(lst)-1, i, -1):
            if lst[j-1] > lst[j]:
                lst[j-1], lst[j] = lst[j], lst[j-1]
                dernier = j
        i = max(dernier, i+1)
    return lst


def shaker_sort(lst):
    # lst = lst[:]
    g = 0
    d = len(lst)-1
    while g < d:
        for j in range(d, g, -1):
            if lst[j-1] > lst[j]:
                lst[j-1], lst[j] = lst[j], lst[j-1]
        g += 1
        for j in range(g, d):
            if lst[j+1] < lst[j]:
                lst[j+1], lst[j] = lst[j], lst[j+1]
        d -= 1
    return lst


def shaker_sort_plus(lst):
    # lst = lst[:]
    g = 0
    d = len(lst)-1
    while g < d:
        dernier = d
        for j in range(d, g, -1):
            if lst[j-1] > lst[j]:
                lst[j-1], lst[j] = lst[j], lst[j-1]
                dernier = j
        g = max(g+1, dernier)
        premier = g
        for j in range(g, d):
            if lst[j+1] < lst[j]:
                lst[j+1], lst[j] = lst[j], lst[j+1]
                premier = j
        d = min(d-1, premier)
    return lst


def selection_sort(lst):
    """
    Trie la liste passée en argument par le tri par sélection.
    """
    def index_min(start):
        """ Return the index of `lst`'s leftmost least element. """
        i_min = start
        e_min = lst[start]
        for j in range(start+1, len(lst)):
            e = lst[j]
            if e < e_min:
                i_min, e_min = j, e
        return i_min

    # lst = lst[:]
    for i in range(len(lst) - 1):
        j = index_min(i)
        lst[i], lst[j] = lst[j], lst[i]
    return lst


def insertion_sort(lst):
    """
    Trie la liste passée en argument par le tri par insertion.
    """
    def shift_left(index):
        val = lst[index]
        while index > 0 and lst[index-1] > val:
            lst[index] = lst[index-1]
            index -= 1
        lst[index] = val

    # lst = lst[:]
    for i in range(1, len(lst)):
        shift_left(i)
    return lst


def quick_sort(lst):
    """
    Trie la liste passée en argument par le tri rapide (tri par pivot).
    """
    def partition(left, right):
        """
        Partitionne la portion [`left`, `right`] de `lst` selon son premier
        élément.
        """
        pivot = left
        left += 1
        while True:
            # move left marker right and right marker left until
            # the corresponding elements are wrongly placed
            while left <= right and lst[pivot] >= lst[left]:
                left += 1
            while left <= right and lst[pivot] < lst[right]:
                right -= 1
            # if the markers crossed, the whole segment is processed
            if left >= right:
                break
            # otherwise, swap elements and continue scanning
            lst[left], lst[right] = lst[right], lst[left]
        # swap the pivot with last element less than or equal to it
        lst[pivot], lst[right] = lst[right], lst[pivot]
        return right

    def sort(left, right):
        if left >= right:
            return
        p = partition(left, right)
        sort(left, p-1)
        sort(p+1, right)

    # lst = lst[:]
    sort(0, len(lst)-1)
    return lst


def merge_sort(lst):
    """
    Trie la liste passée en argument par le tri par fusion.
    """
    def sort(a, aux, lo, hi):
        if lo >= hi:
            return
        mid = lo + (hi - lo)//2
        sort(aux, a, lo, mid)
        sort(aux, a, mid+1, hi)
        merge(a, aux, lo, mid, hi)

    def merge(a, aux, lo, mid, hi):
        i = lo
        j = mid + 1
        k = lo
        while k <= hi:
            if i > mid:
                aux[k] = a[j]
                j += 1
            elif j > hi:
                aux[k] = a[i]
                i += 1
            elif a[i] < a[j]:
                aux[k] = a[i]
                i += 1
            else:
                aux[k] = a[j]
                j += 1
            k += 1

    # lst = lst[:]
    sort(lst[:], lst, 0, len(lst) - 1)
    return lst
