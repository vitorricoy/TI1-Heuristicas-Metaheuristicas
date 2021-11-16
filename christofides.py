import math
import random
import time
import os
from queue import PriorityQueue

def lerArquivosDiretorio(diretorio, att = False):
    for filename in os.listdir(diretorio):
        coordenadas = []
        cont = 0
        with open(diretorio+filename) as file:
            for line in file:
                line = line.strip()
                if line == 'EOF':
                    break
                if cont < 6:
                    cont+=1
                else:
                    partes = line.split()
                    x = float(partes[1])
                    y = float(partes[2])
                    coordenadas.append((x, y))
        somaResultados = 0.0
        somaTempo = 0.0
        for i in range(20):
            inicio = time.time()
            resultado = calcularHeuristica(coordenadas, att)
            tempoGasto = time.time() - inicio
            somaResultados += resultado
            somaTempo += tempoGasto
        print("Média dos resultados encontrados para o arquivo", filename, ":", somaResultados/20.0)
        print("Média de tempo gasto para o arquivo", filename, ":", (somaTempo/20.0)*1000.0, "ms")
        print()

def distancia(p1, p2, att):
    if att:
        xd = p1[0]-p2[0]
        yd = p1[1]-p2[1]
        r = math.sqrt((xd*xd + yd*yd)/10.0)
        t = int(round(r))
        if t < r:
            return t+1
        else:
            return t 
    else:
        xd = p1[0]-p2[0]
        yd = p1[1]-p2[1]
        return int(round(math.sqrt(xd*xd + yd*yd)))

def unionFindBusca(pai, i):
    if pai[i] == i:
        return i
    return unionFindBusca(pai, pai[i])
 
def unionFindUne(pai, rank, x, y):
    raizX = unionFindBusca(pai, x)
    raizY = unionFindBusca(pai, y)
    if rank[raizX] < rank[raizY]:
        pai[raizX] = raizY
    elif rank[raizX] > rank[raizY]:
        pai[raizY] = raizX
    else:
        pai[raizY] = raizX
        rank[raizX] += 1
        

def kruskalMst(listaArestas, numeroVertices):
    result = []
    i = 0
    e = 0
    listaArestas = sorted(listaArestas, key=lambda item: item[2])
    pai = []
    rank = []
    for no in range(numeroVertices):
        pai.append(no)
        rank.append(0)
    while e < numeroVertices-1:
        u, v, w = listaArestas[i]
        i = i + 1
        x = unionFindBusca(pai, u)
        y = unionFindBusca(pai, v)
        if x != y:
            e = e + 1
            result.append([u, v, w])
            unionFindUne(pai, rank, x, y)
    return result

def minimum_weight_matching(mst, matrizDistancia, verticesImpares):
    random.shuffle(verticesImpares)

    while verticesImpares:
        v = verticesImpares.pop()
        tamanho = float("inf")
        u = 1
        maisProximo = 0
        for u in verticesImpares:
            if v != u and matrizDistancia[v][u] < tamanho:
                tamanho = matrizDistancia[v][u]
                maisProximo = u

        mst.append((v, maisProximo, tamanho))
        verticesImpares.remove(maisProximo)

def find_eulerian_tour(mst, matrizDistancia):
    # find neigbours
    neighbours = {}
    for edge in mst:
        if edge[0] not in neighbours:
            neighbours[edge[0]] = []

        if edge[1] not in neighbours:
            neighbours[edge[1]] = []

        neighbours[edge[0]].append(edge[1])
        neighbours[edge[1]].append(edge[0])

    # print("Neighbours: ", neighbours)

    # finds the hamiltonian circuit
    start_vertex = mst[0][0]
    EP = [neighbours[start_vertex][0]]

    while len(mst) > 0:
        for i, v in enumerate(EP):
            if len(neighbours[v]) > 0:
                break

        while len(neighbours[v]) > 0:
            w = neighbours[v][0]

            remove_edge_from_matchedMST(mst, v, w)

            del neighbours[v][(neighbours[v].index(w))]
            del neighbours[w][(neighbours[w].index(v))]

            i += 1
            EP.insert(i, w)

            v = w

    return EP


def remove_edge_from_matchedMST(mst, v1, v2):

    for i, item in enumerate(mst):
        if (item[0] == v2 and item[1] == v1) or (item[0] == v1 and item[1] == v2):
            del mst[i]

    return mst

def find_odd_vertexes(mst):
    tmp_g = {}
    vertexes = []
    for edge in mst:
        if edge[0] not in tmp_g:
            tmp_g[edge[0]] = 0

        if edge[1] not in tmp_g:
            tmp_g[edge[1]] = 0

        tmp_g[edge[0]] += 1
        tmp_g[edge[1]] += 1

    for vertex in tmp_g:
        if tmp_g[vertex] % 2 == 1:
            vertexes.append(vertex)

    return vertexes

def calcularHeuristica(coordenadas, att):
    matrizDistancias = []
    listaArestas = []
    for i in range(len(coordenadas)):
        temp = []
        for j in range(len(coordenadas)):
            if i == j:
                temp.append(0)
            else:
                temp.append(distancia(coordenadas[i], coordenadas[j], att))
            if j > i:
                listaArestas.append((i, j, distancia(coordenadas[i], coordenadas[j], att)))
        matrizDistancias.append(temp)
    mst = kruskalMst(listaArestas, len(coordenadas))
    verticesImpares = find_odd_vertexes(mst)
    minimum_weight_matching(mst, matrizDistancias, verticesImpares)
    eulerian_tour = find_eulerian_tour(mst, matrizDistancias)
    
    current = eulerian_tour[0]
    visited = [False] * len(eulerian_tour)
    visited[0] = True
    length = 0
    for v in eulerian_tour[1:]:
        if not visited[v]:
            visited[v] = True
            length += matrizDistancias[current][v]
            current = v
    return length

lerArquivosDiretorio("ATT/", True)
lerArquivosDiretorio("EUC_2D/")