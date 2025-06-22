import heapq
from collections import defaultdict

#CONTAGEM DE COMPONENTES CONEXAS

#GRAFO NÃO DIRECIONADO
def comp_conexas(grafo):
    visitados = set() # nos visitados
    componentes = [] # componentes conexas

    for vertice in grafo:
        if vertice not in visitados:
            componente = []
            fila = [vertice] #inicio da DFS 
            while fila:
                atual = heapq.heappop(fila) # pilha utilizando heapq
                if atual not in visitados:
                    visitados.add(atual) # marca o nó como já visitado
                    componente.append(atual)
                    for vizinho in grafo[atual]: 
                        if isinstance(vizinho, tuple): # pega apenas o vizinho se vier tupla
                            vizinho = vizinho[0]
                        if vizinho not in visitados:
                            heapq.heappush(fila, vizinho)
            componentes.append(componente)
    return componentes


# GRAFO DIRECIONADO
#Primeira DFS para o grafo original
def dfs_gerar_ordem(grafo, vertice, visitados, pilha):
    fila = [vertice] #simula pilha para DFS
    caminho = [] # ordem de visita dos vertices com base do vertice inicial

    while fila:
        atual = heapq.heappop(fila) #vertice com menor prioridade
        if atual not in visitados:
            visitados.add(atual) 
            caminho.append(atual)
            for vizinho in grafo[atual]:
                if isinstance(vizinho, tuple):
                    vizinho = vizinho[0]
                if vizinho not in visitados:
                    heapq.heappush(fila, vizinho)
    pilha.extend(caminho[::-1])  # adiciona o caminho percorrido na pilha em ordem inversa

#grafo transposto (inverte as arestas)
def transpor_grafo(grafo):
    grafo_transposto = defaultdict(list) #novo grafo com arestas invertidas
    for u in grafo:
        for v in grafo[u]:
            if isinstance(v, tuple):
                v = v[0]
            grafo_transposto[v].append(u)
    
    return grafo_transposto

#dfs no grafo transposto
def dfs_transposto(grafo, vertice, visitados, componente):
    fila = [vertice]
    while fila:
        atual = heapq.heappop(fila)
        if atual not in visitados:
            visitados.add(atual)
            componente.append(atual)
            for vizinho in grafo[atual]:
                if isinstance(vizinho, tuple):
                    vizinho = vizinho[0]
                if vizinho not in visitados:
                    heapq.heappush(fila, vizinho)

#Função principal do Kosaraju, retorna fortemente conexas
def comp_fortemente_conexas(grafo):
    visitados = set() # conjunto de vertices visitados na primeira DFS
    pilha = [] 

    # Percorre todo o grafo original
    for vertice in grafo:
        if vertice not in visitados:
            dfs_gerar_ordem(grafo, vertice, visitados, pilha)
    
    # Transpõe o grafo
    grafo_transposto = transpor_grafo(grafo)

    visitados.clear()  # limpa o conjunto de visitados para a segunda DFS
    componentes = []   # lista final com todas as componentes fortemente conexas

    # Percorre grafo transposto em ordem inversa
    while pilha:
        vertice = pilha.pop()
        if vertice not in visitados:
            componente = []
            dfs_transposto(grafo_transposto, vertice, visitados, componente)
            componentes.append(componente)

    return componentes # retorna todas as componentes achadas
