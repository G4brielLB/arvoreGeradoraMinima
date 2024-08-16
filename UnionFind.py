#para Kruskal

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])  # Path compression
        return self.parent[u]

    def union(self, u, v):
        raiz_u = self.find(u)
        raiz_v = self.find(v)

        if raiz_u != raiz_v:
            if self.rank[raiz_u] > self.rank[raiz_v]:
                self.parent[raiz_v] = raiz_u
            elif self.rank[raiz_u] < self.rank[raiz_v]:
                self.parent[raiz_u] = raiz_v
            else:
                self.parent[raiz_v] = raiz_u
                self.rank[raiz_u] += 1