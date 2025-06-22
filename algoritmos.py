import heapq
from collections import defaultdict, deque

#CONTAGEM DE COMPONENTES CONEXAS

#GRAFO NÃO DIRECIONADO
def comp_conexas(grafo):
    visitados = set() # nos visitados
    componentes = [] # componentes conexas

    for vertice in grafo.nodes:
        if vertice not in visitados:
            componente = []
            fila = [vertice] #inicio da DFS 
            while fila:
                atual = heapq.heappop(fila) # pilha utilizando heapq
                if atual not in visitados:
                    visitados.add(atual) # marca o nó como já visitado
                    componente.append(atual)
                    for vizinho in grafo.adj_list[atual]:
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
            for vizinho in grafo.adj_list[atual]:
                if isinstance(vizinho, tuple):
                    vizinho = vizinho[0]
                if vizinho not in visitados:
                    heapq.heappush(fila, vizinho)
    pilha.extend(caminho[::-1])  # adiciona o caminho percorrido na pilha em ordem inversa

#grafo transposto (inverte as arestas)
def transpor_grafo(grafo):
    grafo_transposto = defaultdict(list) #novo grafo com arestas invertidas
    for u in grafo.nodes:
        for v in grafo.adj_list[u]:
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
    for vertice in grafo.nodes:
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


def get_mst_info_string(node_x, mst_edges, total_cost):
    """Retorna informações sobre a MST como string para salvar em arquivo"""
    info = f"𓂃༞♡ Árvore Geradora Mínima para '{node_x}' ♡༞𓂃\n"
    info += f"Número de arestas na MST: {len(mst_edges)}\n"
    info += f"Custo total da MST: {total_cost}\n\n"
    
    if mst_edges:
        info += "Arestas da MST:\n"
        for u, v, weight in mst_edges:
            info += f"  {u} -- {weight} -- {v}\n"
    else:
        info += "Nenhuma MST encontrada (nó isolado ou não existe no grafo)\n"
    
    return info

# ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚

# CENTRALIDADE DE GRAU

def degree_centrality(graph, node):
    """
    Calcula a centralidade de grau de um nó.
    
    Args:
        graph (Grafo): O grafo (direcionado ou não direcionado)
        node (str): O nó para calcular a centralidade
    
    Returns:
        float: Centralidade de grau entre 0 e 1
    """
    if node not in graph.nodes:
        return 0.0
    
    # Calcula o grau do nó
    if graph.directed:
        # Para grafo direcionado: grau de entrada + grau de saída
        out_degree = len(graph.adj_list.get(node, []))
        in_degree = sum(1 for adj_list in graph.adj_list.values() 
                       for neighbor, _ in adj_list if neighbor == node)
        degree = out_degree + in_degree
    else:
        # Para grafo não direcionado: número de vizinhos
        degree = len(graph.adj_list.get(node, []))
    
    # Número máximo de conexões possíveis (n-1)
    max_degree = len(graph.nodes) - 1
    
    # Evita divisão por zero
    if max_degree == 0:
        return 0.0
    
    return degree / max_degree

def print_degree_centrality(graph, node):
    """Imprime a centralidade de grau de um nó"""
    centrality = degree_centrality(graph, node)
    print(f"\n ˗ˋˏ ♡ ˎˊ˗ Centralidade de Grau para '{node}'  ˗ˋˏ ♡ ˎˊ˗")
    print(f"Centralidade: {centrality:.4f}")
    
    if graph.directed:
        out_degree = len(graph.adj_list.get(node, []))
        in_degree = sum(1 for adj_list in graph.adj_list.values() 
                       for neighbor, _ in adj_list if neighbor == node)
        print(f"Grau de saída: {out_degree}")
        print(f"Grau de entrada: {in_degree}")
        print(f"Grau total: {out_degree + in_degree}")
    else:
        degree = len(graph.adj_list.get(node, []))
        print(f"Grau: {degree}")
    
    print(f"Número total de nós no grafo: {len(graph.nodes)}")
    print(f"Grau máximo possível: {len(graph.nodes) - 1}")

def get_degree_centrality_string(graph, node):
    """Retorna a centralidade de grau de um nó como string"""
    centrality = degree_centrality(graph, node)
    info = f"˗ˋˏ ♡ ˎˊ˗ Centralidade de Grau para '{node}'  ˗ˋˏ ♡ ˎˊ˗\n"
    info += f"Centralidade: {centrality:.4f}\n"
    
    if graph.directed:
        out_degree = len(graph.adj_list.get(node, []))
        in_degree = sum(1 for adj_list in graph.adj_list.values() 
                       for neighbor, _ in adj_list if neighbor == node)
        info += f"Grau de saída: {out_degree}\n"
        info += f"Grau de entrada: {in_degree}\n"
        info += f"Grau total: {out_degree + in_degree}\n"
    else:
        degree = len(graph.adj_list.get(node, []))
        info += f"Grau: {degree}\n"
    
    info += f"Número total de nós no grafo: {len(graph.nodes)}\n"
    info += f"Grau máximo possível: {len(graph.nodes) - 1}\n\n"
    
    return info

# Função de teste para centralidade
def test_degree_centrality():
    """Função de teste para demonstrar o uso da centralidade de grau"""
    from grafos import read_csv, undirected_graph, directed_graph
    
    # Carrega os dados e constrói os grafos
    cast_list, director_list = read_csv('netflix_amazon_disney_titles.csv')
    graph_undirected = undirected_graph(cast_list)
    graph_directed = directed_graph(cast_list, director_list)
    
    # Testa com um nó específico
    test_node = "BOB ODENKIRK"
    
    print("ִ ࣪𖤐  TESTE DE CENTRALIDADE DE GRAU ִ ࣪𖤐")
    print("\n✿ GRAFO NÃO DIRECIONADO ✿")
    print_degree_centrality(graph_undirected, test_node)
    print("\n" + "━⊱⋆⊰"*10)
    print("\n✿ GRAFO DIRECIONADO ✿")
    print_degree_centrality(graph_directed, test_node)

# ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚

#CENTRALIDADE DE INTERMEDIAÇÃO

def betweenness_centrality(grafo, vertice_alvo):
    """
    Calcula a centralidade de intermediação de um vértice no grafo ponderado,
    retornando um valor normalizado entre 0 e 1.
    
    grafo: dict {vertice: lista de (vizinho, peso)}
    vertice_alvo: vértice para o cálculo da centralidade
    
    Usa algoritmo de Brandes para grafos ponderados (Dijkstra).
    """
    #verifica se o vertice alvo está no grafo, se não retorna 0
    if vertice_alvo not in grafo:
        print(f"Vértice '{vertice_alvo}' não encontrado no grafo")
        return 0.0
    
    vertices = list(grafo.keys())
    n = len(vertices)
    if n < 3:
        return 0.0  # centralidade = 0 para grafos muito pequenos
    
    centralidade = 0.0 # acumulador de centralidade

    # Otimização: para grafos grandes, limitar o número de vértices fonte
    max_sources = min(500, n)  # máximo 500 vértices fonte para grafos ponderados
    
    # Se o grafo é muito grande, amostrar vértices fonte
    if n > max_sources:
        import random
        vertices_fonte = random.sample(vertices, max_sources)
        # Sempre incluir o vértice alvo se não estiver na amostra
        if vertice_alvo not in vertices_fonte:
            vertices_fonte[0] = vertice_alvo
    else:
        vertices_fonte = vertices

    for s in vertices_fonte:
        # Inicializa estruturas para Dijkstra de Brandes
        pilha = []
        predecessores = defaultdict(list)
        sigma = defaultdict(int) # numero de caminhos mais curtos de s ate v
        distancia = defaultdict(lambda: float('inf')) # distancia de s ate v
        sigma[s] = 1
        distancia[s] = 0

        # Dijkstra com heap para encontrar caminhos mais curtos
        heap = [(0, s)]
        visitados = set()
        
        while heap:
            dist_v, v = heapq.heappop(heap)
            
            if v in visitados:
                continue
                
            visitados.add(v)
            pilha.append(v)
            
            for w, peso in grafo.get(v, []):
                if w in visitados:
                    continue
                    
                # Se encontrou um caminho mais curto
                if distancia[w] > dist_v + peso:
                    distancia[w] = dist_v + peso
                    sigma[w] = sigma[v]
                    predecessores[w] = [v]
                    heapq.heappush(heap, (distancia[w], w))
                # Se encontrou um caminho de mesmo comprimento
                elif distancia[w] == dist_v + peso:
                    sigma[w] += sigma[v]
                    predecessores[w].append(v)

        delta = defaultdict(float) #inicia dependencias a zero
        while pilha:
            w = pilha.pop() #processa os vértices na ordem inversa do Dijkstra
            for v in predecessores[w]:
                if sigma[w] != 0: #evita divisão por zero
                    # Atualiza a dependência de v com base na dependência de w e nos caminhos mínimos
                    delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
            # se w é o vertice alvo, soma o delta para a centralidade
            if w == vertice_alvo and w != s:
                centralidade += delta[w]

    #normaliza para que o resultado fique entre 0 e 1
    # Ajusta a normalização baseado no número de vértices fonte usados
    if n > max_sources:
        # Para amostragem, ajusta a normalização
        normalizacao = (max_sources / n) / ((n - 1) * (n - 2)) if n > 2 else 1
    else:
        normalizacao = 1 / ((n - 1) * (n - 2)) if n > 2 else 1
    
    centralidade_normalizada = centralidade * normalizacao

    return centralidade_normalizada

def get_betweenness_centrality_string(graph, node):
    """Retorna a centralidade de intermediação de um nó como string"""
    # Converte defaultdict para dict regular para evitar problemas
    grafo_dict = dict(graph.adj_list)
    centrality = betweenness_centrality(grafo_dict, node)
    info = f"˗ˋˏ ♡ ˎˊ˗ Centralidade de Intermediação para '{node}'  ˗ˋˏ ♡ ˎˊ˗\n"
    info += f"Centralidade: {centrality:.6f}\n\n"
    
    return info

# ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚

#CENTRALIDADE DE PROXIMIDADE

def closeness_centrality(grafo, vertices=None):
    """
    Calcula a centralidade de proximidade para grafos ponderados.
    Usa Dijkstra para encontrar as distâncias mínimas.
    """
    if vertices is None:
        #se não tiver conjunto de vertices especifico utiliza todos do grafo
        vertices = list(grafo.keys())
    
    n = len(grafo) # numero total de vértices no grafo
    centralidade = {} 
    
    for v in vertices:
        # Dijkstra para calcular todas as distancias mínimas a partir de v
        distancia = {v: 0} # armazena a distancia de v ate cada vertice alcançavel
        heap = [(0, v)] # heap para Dijkstra iniciando em v
        visitados = set()
        
        while heap:
            dist_u, u = heapq.heappop(heap)
            
            if u in visitados:
                continue
                
            visitados.add(u)
            
            for w, peso in grafo.get(u, []):
                if w not in distancia or distancia[w] > dist_u + peso:
                    distancia[w] = dist_u + peso
                    heapq.heappush(heap, (distancia[w], w))
        
        # número de nós alcançados (exceto ele mesmo)
        reach = len(distancia) - 1
        # soma das distâncias para os nós alcançados
        total_dist = sum(distancia.values())
        
        if reach > 0 and total_dist > 0:
            # fórmula da centralidade de proximidade (quanto menor a soma das distancias, maior a centralidade)
            valor = reach / total_dist
            # normalização para grafos desconexos (manter valor entre 0 e 1)
            valor *= (n - 1) / reach
            centralidade[v] = valor
        else:
            #se o vertice esta isolado, ou não chega em ninguém centralidade = 0
            centralidade[v] = 0.0
    
    return centralidade

def get_closeness_centrality_string(graph, node):
    """Retorna a centralidade de proximidade de um nó como string"""
    # Converte defaultdict para dict regular para evitar problemas
    grafo_dict = dict(graph.adj_list)
    centralidades = closeness_centrality(grafo_dict, [node])
    centrality = centralidades.get(node, 0.0)
    
    info = f"˗ˋˏ ♡ ˎˊ˗ Centralidade de Proximidade para '{node}'  ˗ˋˏ ♡ ˎˊ˗\n"
    info += f"Centralidade: {centrality:.6f}\n\n"
    
    return info


# ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚ ଘ(੭ˊᵕˋ)੭* ੈ✩‧₊˚