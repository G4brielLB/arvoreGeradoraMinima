from GrafoTestes import Grafo

grafo = Grafo()
grafo.adicionar_arestas()

EXECUCOES = 10

media_prim = 0
media_kruskal = 0

for i in range(EXECUCOES):
  prim, arestas_prim, tempo_prim = grafo.prim()

  kruskal, custo_kruskal, tempo_kruskal = grafo.kruskal()

  soma = 0
  for i in range(len(prim)):
    for j in range(len(prim[i])):
      soma += prim[i][j][1]
  soma = int(soma/2)

  print("Soma dos pesos da árvore geradora mínima por Prim: ", soma)
  print(f"Tempo de execução do Prim: {tempo_prim} µs")
  media_prim += tempo_prim

  print("Soma dos pesos da árvore geradora mínima por Kruskal: ", custo_kruskal)
  print(f"Tempo de execução do Kruskal: {tempo_kruskal} ns")
  media_kruskal += tempo_kruskal

print(f"Média do tempo de execução do Prim: {media_prim/EXECUCOES} µs")
print(f"Média do tempo de execução do Kruskal: {media_kruskal/EXECUCOES} µs")
