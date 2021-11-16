import math
import random
import time
import os

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

def calcularHeuristica(coordenadas, att):
    matrizDistancias = []
    for i in range(len(coordenadas)):
        temp = []
        for j in range(len(coordenadas)):
            if i == j:
                temp.append(0)
            else:
                temp.append(distancia(coordenadas[i], coordenadas[j], att))
        matrizDistancias.append(temp)
    visitados = set()
    noInicial = random.randint(0, len(coordenadas)-1) # escolhe o nó de inicio aleatoriamente
    noAtual = noInicial
    distanciaFinal = 0
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