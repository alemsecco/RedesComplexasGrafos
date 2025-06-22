import algoritmos
import random
from collections import defaultdict, deque

# =========================
# Funções rápidas e otimizadas SEM .neighbors
# =========================

def graph_adjlist_neighbors(graph, node):
    """
    Retorna apenas os nós vizinhos (ignorando o peso) de 'node' em 'graph'.
    """
    return [v for (v, _) in graph.adj_list.get(node, [])]

def analyze_degree_distribution(graph, graph_name, sample_size=1000):
    """
    Analisa a distribuição de graus usando amostragem.
    """
    nodes = list(graph.nodes)
    if len(nodes) > sample_size:
        sample = random.sample(nodes, sample_size)
    else:
        sample = nodes
    
    # Para cada nó no sample, grau = tamanho da lista de adjacência (sem peso)
    degrees = [len(graph_adjlist_neighbors(graph, n)) for n in sample]
    if degrees:
        avg = sum(degrees) / len(degrees)
        max_deg = max(degrees)
        min_deg = min(degrees)
    else:
        avg = max_deg = min_deg = 0
    
    info = f"{graph_name} (AMOSTRA DE {len(sample)} NÓS):\n"
    info += f"- Grau médio: {avg:.2f}\n- Grau máximo: {max_deg}\n- Grau mínimo: {min_deg}\n"
    info += f"- Top 5 graus: {sorted(degrees, reverse=True)[:5]}\n\n"
    return info

def analyze_component_distribution(undirected_graph, directed_graph, sample_size=1000):
    """
    Analisa componentes no grafo não direcionado usando BFS a partir de amostras.
    """
    nodes = list(undirected_graph.nodes)
    if len(nodes) > sample_size:
        sample = random.sample(nodes, sample_size)
    else:
        sample = nodes
    
    visited = set()
    comp_sizes = []
    for n in sample:
        if n not in visited:
            queue = deque([n])
            size = 0
            while queue:
                v = queue.popleft()
                if v not in visited:
                    visited.add(v)
                    size += 1
                    for w in graph_adjlist_neighbors(undirected_graph, v):
                        if w not in visited:
                            queue.append(w)
            comp_sizes.append(size)
    
    giant = max(comp_sizes) if comp_sizes else 0
    comp_small = sum(1 for s in comp_sizes if s <= 3)
    info = f"Componentes (AMOSTRA DE {len(sample)} NÓS):\n"
    info += f"- Maior componente: {giant} nós\n"
    info += f"- Componentes pequenas (<=3 nós): {comp_small}\n\n"
    return info

def get_top_actors_degree_string(graph, top_n=10):
    """
    Retorna o top 'top_n' atores/atrizes por grau (contagem de vizinhos).
    """
    nodes = list(graph.nodes)
    # Grau = número de vizinhos
    degrees = [(n, len(graph_adjlist_neighbors(graph, n))) for n in nodes]
    degrees.sort(key=lambda x: x[1], reverse=True)
    
    info = ""
    for i, (n, d) in enumerate(degrees[:top_n], 1):
        info += f"{i}. {n}: {d}\n"
    return info

def fast_betweenness_actors(graph, top_n=10, sample_size=50):
    """
    Betweenness aproximada por amostragem e BFS para atores (grafo não direcionado).
    """
    nodes = list(graph.nodes)
    if len(nodes) > sample_size:
        sample = random.sample(nodes, sample_size)
    else:
        sample = nodes
    
    betw = defaultdict(float)
    
    for s in sample:
        # BFS
        queue = deque([s])
        pred = {s: []}
        dist = {s: 0}
        num_paths = {s: 1}
        stack = []
        
        while queue:
            v = queue.popleft()
            stack.append(v)
            for w in graph_adjlist_neighbors(graph, v):
                if w not in dist:
                    queue.append(w)
                    dist[w] = dist[v] + 1
                    num_paths[w] = num_paths[v]
                    pred[w] = [v]
                elif dist[w] == dist[v] + 1:
                    num_paths[w] += num_paths[v]
                    pred[w].append(v)
        
        delta = dict.fromkeys(stack, 0)
        while stack:
            w = stack.pop()
            for v in pred[w]:
                delta[v] += (num_paths[v] / num_paths[w]) * (1 + delta[w])
            if w != s:
                betw[w] += delta[w]
    
    for k in betw:
        betw[k] /= sample_size
    
    top = sorted(betw.items(), key=lambda x: x[1], reverse=True)[:top_n]
    info = ""
    for i, (n, v) in enumerate(top, 1):
        info += f"{i}. {n}: {v:.2f}\n"
    return info

def get_top_directors_string(graph, top_n=10):
    """
    Top diretores por grau de entrada (quantos atores apontam para cada diretor).
    """
    nodes = list(graph.nodes)
    in_degrees = []
    for node in nodes:
        # Soma de '1' para cada aresta que chega em 'node'
        in_deg = sum(
            1 for adjacency in graph.adj_list.values()
            for (v, _) in adjacency
            if v == node
        )
        in_degrees.append((node, in_deg))
    
    in_degrees.sort(key=lambda x: x[1], reverse=True)
    info = ""
    for i, (n, d) in enumerate(in_degrees[:top_n], 1):
        info += f"{i}. {n}: {d}\n"
    return info

def get_top_directors_betweenness_string_fast(graph, top_n=10, sample_size=50):
    """
    Betweenness aproximada para diretores (grafo direcionado).
    """
    nodes = list(graph.nodes)
    if len(nodes) > sample_size:
        sample = random.sample(nodes, sample_size)
    else:
        sample = nodes
    
    betw = defaultdict(float)
    for s in sample:
        queue = deque([s])
        pred = {s: []}
        dist = {s: 0}
        num_paths = {s: 1}
        stack = []
        
        while queue:
            v = queue.popleft()
            stack.append(v)
            for (w, _) in graph.adj_list.get(v, []):
                if w not in dist:
                    queue.append(w)
                    dist[w] = dist[v] + 1
                    num_paths[w] = num_paths[v]
                    pred[w] = [v]
                elif dist[w] == dist[v] + 1:
                    num_paths[w] += num_paths[v]
                    pred[w].append(v)
        
        delta = dict.fromkeys(stack, 0)
        while stack:
            w = stack.pop()
            for v in pred[w]:
                delta[v] += (num_paths[v] / num_paths[w]) * (1 + delta[w])
            if w != s:
                betw[w] += delta[w]
    
    for k in betw:
        betw[k] /= sample_size
    
    top = sorted(betw.items(), key=lambda x: x[1], reverse=True)[:top_n]
    info = ""
    for i, (n, val) in enumerate(top, 1):
        info += f"{i}. {n}: {val:.2f}\n"
    return info

def get_top_directors_closeness_string(graph, top_n=10, sample_size=50):
    """
    Closeness aproximada para diretores (grafo direcionado),
    penalizando nós inalcançáveis, exibindo 10 casas decimais.
    """
    from collections import deque
    import random

    def neighbors(v):
        return [w for (w, _) in graph.adj_list.get(v, [])]

    nodes = list(graph.nodes)
    if len(nodes) > sample_size:
        sample = random.sample(nodes, sample_size)
    else:
        sample = nodes

    closeness = {}
    total_nodes = len(nodes)  # total de nós no grafo

    for n in sample:
        visited = {n: 0}
        queue = deque([(n, 0)])
        while queue:
            v, dist = queue.popleft()
            for w in neighbors(v):
                if w not in visited:
                    visited[w] = dist + 1
                    queue.append((w, dist + 1))

        # Penaliza nós não alcançáveis, atribuindo-lhes distância grande
        dist_sum = sum(visited.values())
        unreachable = total_nodes - len(visited)
        dist_sum += unreachable * total_nodes

        if dist_sum > 0:
            # Closeness = (nós alcançados) / (soma das distâncias)
            closeness[n] = (len(visited) - 1) / dist_sum
        else:
            closeness[n] = 0

    # Ordena e gera texto final, com 10 casas decimais
    top = sorted(closeness.items(), key=lambda x: x[1], reverse=True)[:top_n]
    info = ""
    for i, (director, val) in enumerate(top, 1):
        info += f"{i}. {director}: {val:.10f}\n"
    return info

def get_top_actors_closeness_string(graph, top_n=10, sample_size=50):
    """
    Closeness aproximada para atores (grafo não direcionado),
    penalizando nós inalcançáveis, exibindo 10 casas decimais.
    """
    from collections import deque
    import random

    nodes = list(graph.nodes)
    if len(nodes) > sample_size:
        sample = random.sample(nodes, sample_size)
    else:
        sample = nodes

    closeness = {}
    total_nodes = len(graph.nodes)

    for n in sample:
        visited = {n: 0}
        queue = deque([(n, 0)])
        while queue:
            v, d = queue.popleft()
            for w, _ in graph.adj_list.get(v, []):
                if w not in visited:
                    visited[w] = d + 1
                    queue.append((w, d + 1))

        # Penaliza nós não alcançáveis
        dist_sum = sum(visited.values())
        unreachable = total_nodes - len(visited)
        dist_sum += unreachable * total_nodes

        if dist_sum > 0:
            closeness[n] = (len(visited) - 1) / dist_sum
        else:
            closeness[n] = 0

    top = sorted(closeness.items(), key=lambda x: x[1], reverse=True)[:top_n]
    info = ""
    for i, (actor, val) in enumerate(top, 1):
        info += f"{i}. {actor}: {val:.10f}\n"
    return info