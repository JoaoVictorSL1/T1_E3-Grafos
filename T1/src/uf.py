# -*- coding: utf-8 -*-

class UF:
    """
    Estrutura de dados Union-Find oficial da base algs4-py (Weighted Quick-Union com compressão de caminhos).
    Usada para gerenciar componentes conectados no algoritmo de Kruskal.
    """
    def __init__(self, n):
        self.count = n
        self.id = list(range(n))
        self.sz = [1] * n

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def find(self, p):
        while self.id[p] != p:
            self.id[p] = self.id[self.id[p]]  # compressão de caminhos (path compression)
            p = self.id[p]
        return p

    def union(self, p, q):
        pId = self.find(p)
        qId = self.find(q)
        if pId == qId:
            return
        if self.sz[pId] < self.sz[qId]:
            self.id[pId] = qId
            self.sz[qId] += self.sz[pId]
        else:
            self.id[qId] = pId
            self.sz[pId] += self.sz[qId]
        self.count -= 1
