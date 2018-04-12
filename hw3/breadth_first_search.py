# Author(s): Lucas Duarte Bahia
#            Jordan Giebas
#            Harveen Oberoi
#            Daniel Rojas Coy

# breadth_first_search.py


class Tree:
    def __init__(self, value, parent):
        self._value = value
        self._parent = parent


def BFS(G, root, target): # Pythonish pseudocode
    S = {root}
    T={root:[]}
    Q = [root]

    while Q:
        cur = Q.pop(0)
        if cur is target:
            parent_list = [cur]

            aux=cur
            while root not in parent_list:
                for v,k in zip(T.values(),T.keys()):
                   if aux in v:
                    parent_list.append(k)
                    aux = k
                    break

            parent_list = list(reversed(parent_list))
            return parent_list

        aux_list = []
        for v in G[cur]:
            if v not in S:
                S.add(v)
                aux_list += [v]
                Q += [v]

        T[cur] = aux_list  # parent:nodes

def main():
    G = { 'A' : [ 'B', 'J', 'Me' ],
         'B' : [ 'A' ],
         'C' : [ 'D', 'P' ],
         'D' : [ 'C', 'O' ],
         'E' : [ 'F', 'J', 'K' ],
         'F' : [ 'E', 'M' ],
         'G' : [ 'K', 'S', 'Ed' ],
         'H' : [ 'O', 'U' ],
         'Me': [ 'A', 'I', 'N', 'V' ],
         'I' : [ 'Me', 'Q' ],
         'J' : [ 'A', 'E', 'L', 'Q', 'W' ],
         'K' : [ 'E', 'G' ],
         'L' : [ 'J', 'W' ],
         'M' : [ 'E', 'S', 'T' ],
         'N' : [ 'Me', 'V' ],
         'O' : [ 'H', 'D' ],
         'P' : [ 'C', 'U' ],
         'Q' : [ 'I', 'J', 'X', 'Y' ],
         'R' : [ 'Ed' ],
         'S' : [ 'G', 'M', 'Y', 'Z' ],
         'T' : [ 'M' ],
         'U' : [ 'H', 'P' ],
         'V' : [ 'Me', 'N' ],
         'W' : [ 'J', 'L' ],
         'X' : [ 'Q', 'Y' ],
         'Y' : [ 'Q', 'S', 'X', 'Z' ],
         'Ed': [ 'G', 'R', 'Z' ],
         'Z' : [ 'S', 'Y', 'Ed' ] }
    print('Shortest path from Me to Ed:', BFS(G, 'Me', 'Ed'))
    print('Shortest path from A to I:', BFS(G, 'A', 'I'))
    print('Shortest path from B to R:', BFS(G, 'B', 'R'))
    print('Shortest path from C to H:', BFS(G, 'C', 'H'))
    print('Shortest path from M to T:', BFS(G, 'M', 'T'))


if __name__ == '__main__':
    main()
