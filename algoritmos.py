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

# ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚

# ÁRVORE GERADORA MÍNIMA

def mst_prim(graph, start):
    """
    Implementação do algoritmo de Prim usando heapq para encontrar a MST
    da componente que contém o vértice start.
    """
    if graph.directed:
        raise ValueError("Esta função só funciona com grafos não direcionados")
    
    if start not in graph.nodes:
        print(f"Vértice '{start}' não encontrado no grafo")
        return [], 0
    
    print(f"Calculando Árvore Geradora Mínima a partir do vértice '{start}'...")
    
    # Encontra a componente conexa que contém start
    component = get_component_nodes(graph, start)
    if len(component) <= 1:
        print(f"Vértice '{start}' está isolado")
        return [], 0
    
    # Implementação de Prim com heapq
    visitado = set()
    agm = []
    custo_total = 0
    fila = []

    # Inicializa com o vértice start
    visitado.add(start)
    for viz, peso in graph.adj_list.get(start, []):
        if viz in component:  # Só adiciona arestas para vértices da componente
            heapq.heappush(fila, (peso, start, viz))

    while fila and len(visitado) < len(component):
        peso, u, v = heapq.heappop(fila)
        if v not in visitado:
            visitado.add(v)
            agm.append((u, v, peso))
            custo_total += peso
            for viz, p in graph.adj_list.get(v, []):
                if viz in component and viz not in visitado:  # Só adiciona arestas para vértices da componente
                    heapq.heappush(fila, (p, v, viz))

    print(f"Árvore Geradora Mínima calculada com custo total: {custo_total}")
    return agm, custo_total

def get_component_nodes(graph, start_node):
    """
    Encontra todos os nós da componente conexa que contém start_node.
    Usa busca em largura (BFS).
    """
    if start_node not in graph.nodes:
        return set()
    
    component = set()
    queue = [start_node]
    component.add(start_node)
    
    while queue:
        current = queue.pop(0)
        for neighbor, weight in graph.adj_list[current]:
            if neighbor not in component:
                component.add(neighbor)
                queue.append(neighbor)
    
    return component

def print_mst_info(node_x, mst_edges, total_cost):
    """Imprime informações sobre a MST encontrada"""
    if mst_edges:
        print("\nArestas da MST:")
        for u, v, weight in mst_edges:
            print(f"  {u} -- {weight} -- {v}")
    else:
        print("Nenhuma MST encontrada (nó isolado ou não existe no grafo)")

    print(f"\n=== Árvore Geradora Mínima para '{node_x}' ===")
    print(f"Número de arestas na MST: {len(mst_edges)}")
    print(f"Custo total da MST: {total_cost}")

# Função de teste
def test_mst():
    """Função de teste para demonstrar o uso"""
    from grafos import read_csv, undirected_graph
    
    # Carrega os dados e constrói o grafo
    cast_list, director_list = read_csv('netflix_amazon_disney_titles.csv')
    graph = undirected_graph(cast_list)
    
    # Testa com um nó específico
    test_node = "BOB ODENKIRK"
    mst_edges, total_cost = mst_prim(graph, test_node)
    print_mst_info(test_node, mst_edges, total_cost)

if __name__ == "__main__":
    test_mst()


# ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚