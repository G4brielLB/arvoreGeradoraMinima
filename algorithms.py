import random
from operator import itemgetter

from Grafo import Grafo

def Prim(edges_list):
    grafo = Grafo(len(edges_list))
    grafo.setGrafo(edges_list)
    try:
        prim = grafo.prim()
    except Exception as e:
        raise e

    arvore_binaria = prim[1]

    return arvore_binaria

def Kruskal(edges_list):
    grafo = Grafo(len(edges_list))
    grafo.setGrafo(edges_list)

    try:
        kruskal = grafo.kruskal()
    except Exception as e:
        raise e
    
    arvore_binaria = kruskal[0]
    
    return arvore_binaria