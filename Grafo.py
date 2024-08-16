from UnionFind import UnionFind

class Grafo:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.grafo = self.construir_grafo(num_vertices)
        self.arvore_geradora = []

    def construir_grafo(self, num_vertices):
        return [[] for _ in range(num_vertices)]

    def setGrafo(self,grafo):
        self.grafo = grafo
        self.num_vertices = len(grafo)

    def adicionar_arestas(self):
        print(f"Digite os dois vértices e o p entre eles (1 a {self.num_vertices}). Os três números devem ser separados por espaço:")
        while True:
            aresta_existe = False
            entrada = input()
            try:
                v1, v2, p = map(int, entrada.split())
            except:
                print("Entrada inválida, tente novamente.")
                continue

            if v1 <= 0 or v2 <= 0 or p <= 0:
                break
            elif v1 > self.num_vertices or v2 > self.num_vertices:
                print(f"Digite um vértice válido (entre 1 e {self.num_vertices}).")
                continue

            v1 -= 1
            v2 -= 1

            for a in self.grafo[v1]:
                if v2 == a[0]:
                    print("Aresta já existe")
                    aresta_existe = True
                    break

            if aresta_existe:
                continue

            self.grafo[v1].append((v2, p))
            self.grafo[v2].append((v1, p))

    def imprimir_arestas(self):
        for i in range(self.num_vertices):
            for j in range(len(self.grafo[i])):
                v1 = i + 1
                v2 = self.grafo[i][j][0] + 1
                p = self.grafo[i][j][1]
                print(v1, v2, p)

    def prim(self):
        arvore_prim = self.construir_grafo(self.num_vertices)
        vv = [0]  
        prox = []
        arestas = []
        index = 0
        while len(vv) < self.num_vertices:
            #for i in range(self.num_vertices):
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
        return arvore_prim, arestas
    
    def obter_arestas_ord(self):
        arestas = []
        for v1 in range(self.num_vertices):
            for v2, p in self.grafo[v1]:
                if v1 < v2: 
                    arestas.append((v1, v2, p))
        return sorted(arestas, key=lambda item: item[2])
    
    def kruskal(self):
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

        return kruskal, custo_total

        