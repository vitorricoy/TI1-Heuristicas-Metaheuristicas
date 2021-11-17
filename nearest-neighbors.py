import math
import random
import time
import os

# Lê os arquivos do diretório indicado, executa a heurística para cada um deles e imprime o resultado
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
        somaResultado = 0.0
        somaTempo = 0.0
        for i in range(1000):
            inicio = time.time()
            resultado = calcularHeuristica(coordenadas, att)
            tempoGasto = time.time() - inicio
            somaResultado += resultado
            somaTempo += tempoGasto
        print("Resultado medio encontrado para o arquivo", filename, ":", somaResultado/1000.0)
        print("Tempo gasto medio para o arquivo", filename, ":", (somaTempo/1000.0)*1000.0, "ms")
        print()

# Calcula a distância de acordo com a formula correta do arquivo
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

def calcularHeuristica(coordenadas, att):
    # Calcula a matriz de distâncias do grafo
    matrizDistancias = []
    for i in range(len(coordenadas)):
        temp = []
        for j in range(len(coordenadas)):
            if i == j:
                temp.append(0)
            else:
                temp.append(distancia(coordenadas[i], coordenadas[j], att))
        matrizDistancias.append(temp)
    # Simula a visitação dos nós escolhendo sempre o menor caminho que leva a um nó não visitado
    visitados = set()
    noInicial = random.randint(0, len(coordenadas)-1) # Escolhe o nó de inicio aleatoriamente
    noAtual = noInicial
    distanciaFinal = 0
    visitados.add(noInicial)
    while len(visitados) != len(coordenadas):
        proximoNo = -1
        menorDistancia = math.inf
        for i in range(len(coordenadas)):
            if i not in visitados:
                if matrizDistancias[noAtual][i] < menorDistancia:
                    menorDistancia = matrizDistancias[noAtual][i]
                    proximoNo = i
        visitados.add(proximoNo)
        distanciaFinal+=menorDistancia
        noAtual = proximoNo
    distanciaFinal += matrizDistancias[noAtual][noInicial]
    return distanciaFinal

lerArquivosDiretorio("ATT/", True)
lerArquivosDiretorio("EUC_2D/")