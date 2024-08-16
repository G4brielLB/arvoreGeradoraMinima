from UnionFind import UnionFind
import time

VERTICES = 20
arquivo_grafo = "grafos/completos/g1_20.txt"

class Grafo:
    def __init__(self):
        self.num_vertices = VERTICES
        self.grafo = self.construir_grafo(VERTICES)
        self.arvore_geradora = []

    def construir_grafo(self, num_vertices):
        return [[] for _ in range(num_vertices)]

    def adicionar_arestas(self):
        with open(arquivo_grafo, "r") as file:
            for line in file:
                v1, v2, p = map(int, line.split())
                self.grafo[v1-1].append((v2-1, p))
                self.grafo[v2-1].append((v1-1, p))

    def imprimir_arestas(self):
        for i in range(self.num_vertices):
            for j in range(len(self.grafo[i])):
                v1 = i + 1
                v2 = self.grafo[i][j][0] + 1
                p = self.grafo[i][j][1]
                print(v1, v2, p)

    def kruskal(self):
        inicio = time.time_ns()
        arestas = self.obter_arestas_ord()
        uf = UnionFind(self.num_vertices)
        kruskal = []
        custo_total = 0

        for u, v, p in arestas:
            if len(kruskal) == self.num_vertices - 1:
                break
            if uf.find(u) != uf.find(v):
                uf.union(u, v)
                kruskal.append((u, v, p))
                custo_total += p

        fim = time.time_ns()
        tempo = (fim - inicio) / 1000
        return kruskal, custo_total, tempo

    def obter_arestas_ord(self):
        arestas = []
        for v1 in range(self.num_vertices):
            for v2, peso in self.grafo[v1]:
                if v1 < v2: 
                    arestas.append((v1, v2, peso))
        return sorted(arestas, key=lambda item: item[2])


    def prim(self):
        inicio = time.time_ns()
        arvore_prim = self.construir_grafo(self.num_vertices)
        vv = [0]  
        prox = []
        arestas = []
        index = 0
        while len(vv) < self.num_vertices:
            if index <= len(vv)-1:
                for v, p in self.grafo[vv[index]]:
                    if v not in vv:
                        prox.append((vv[index], v, p))
            else:
                index -= 1

            prox.sort(key=lambda y: y[2])  
            v1, v2, p = prox.pop(0)
            if v2 not in vv:
                arvore_prim[v1].append((v2, p))
                arvore_prim[v2].append((v1, p))
                vv.append(v2)
                arestas.append((v1, v2, p))

            if len(vv) == self.num_vertices:
                break
            index += 1

        self.arvore_geradora = arvore_prim
        fim = time.time_ns()
        tempo = (fim - inicio) / 1000
        return arvore_prim, arestas, tempo
