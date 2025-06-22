import algoritmos
from collections import Counter, defaultdict

def get_top_directors_by_centrality(graph, top_n=10):
    """
    Encontra os top N diretores mais influentes baseado na centralidade de grau.
    
    Args:
        graph (Grafo): Grafo direcionado (ator -> diretor)
        top_n (int): Número de diretores a retornar (padrão: 10)
    
    Returns:
        list: Lista de tuplas (diretor, centralidade) ordenada por centralidade decrescente
    """
    if not graph.directed:
        raise ValueError("Esta função só funciona com grafos direcionados")
    
    # Calcula centralidade para todos os diretores
    director_centralities = []
    
    for node in graph.nodes:
        # Calcula o grau de entrada (quantos atores trabalharam com este diretor)
        in_degree = sum(1 for adj_list in graph.adj_list.values() 
                       for neighbor, _ in adj_list if neighbor == node)
        
        # Calcula a centralidade de grau
        max_degree = len(graph.nodes) - 1
        if max_degree > 0:
            centrality = in_degree / max_degree
            director_centralities.append((node, centrality, in_degree))
    
    # Ordena por centralidade decrescente
    director_centralities.sort(key=lambda x: x[1], reverse=True)
    
    # Retorna os top N
    return director_centralities[:top_n]

def get_top_directors_by_betweenness(graph, top_n=10):
    """
    Encontra os top N diretores mais influentes baseado na centralidade de intermediação.
    """
    if not graph.directed:
        raise ValueError("Esta função só funciona com grafos direcionados")
    
    # Converte defaultdict para dict regular
    grafo_dict = dict(graph.adj_list)
    
    director_centralities = []
    for node in graph.nodes:
        centrality = algoritmos.betweenness_centrality(grafo_dict, node)
        director_centralities.append((node, centrality))
    
    # Ordena por centralidade decrescente
    director_centralities.sort(key=lambda x: x[1], reverse=True)
    
    return director_centralities[:top_n]

def get_top_directors_by_closeness(graph, top_n=10):
    """
    Encontra os top N diretores mais influentes baseado na centralidade de proximidade.
    """
    if not graph.directed:
        raise ValueError("Esta função só funciona com grafos direcionados")
    
    # Converte defaultdict para dict regular
    grafo_dict = dict(graph.adj_list)
    
    # Calcula centralidade de proximidade para todos os diretores
    centralidades = algoritmos.closeness_centrality(grafo_dict)
    
    director_centralities = []
    for node in graph.nodes:
        centrality = centralidades.get(node, 0.0)
        director_centralities.append((node, centrality))
    
    # Ordena por centralidade decrescente
    director_centralities.sort(key=lambda x: x[1], reverse=True)
    
    return director_centralities[:top_n]

def get_top_actors_by_degree(graph, top_n=10):
    """
    Encontra os top N atores mais influentes baseado na centralidade de grau.
    """
    if graph.directed:
        raise ValueError("Esta função só funciona com grafos não direcionados")
    
    actor_centralities = []
    for node in graph.nodes:
        centrality = algoritmos.degree_centrality(graph, node)
        degree = len(graph.adj_list.get(node, []))
        actor_centralities.append((node, centrality, degree))
    
    # Ordena por centralidade decrescente
    actor_centralities.sort(key=lambda x: x[1], reverse=True)
    
    return actor_centralities[:top_n]

def get_top_actors_by_betweenness(graph, top_n=10):
    """
    Encontra os top N atores mais influentes baseado na centralidade de intermediação.
    """
    if graph.directed:
        raise ValueError("Esta função só funciona com grafos não direcionados")
    
    # Converte defaultdict para dict regular
    grafo_dict = dict(graph.adj_list)
    
    actor_centralities = []
    for node in graph.nodes:
        centrality = algoritmos.betweenness_centrality(grafo_dict, node)
        actor_centralities.append((node, centrality))
    
    # Ordena por centralidade decrescente
    actor_centralities.sort(key=lambda x: x[1], reverse=True)
    
    return actor_centralities[:top_n]

def get_top_actors_by_closeness(graph, top_n=10):
    """
    Encontra os top N atores mais influentes baseado na centralidade de proximidade.
    """
    if graph.directed:
        raise ValueError("Esta função só funciona com grafos não direcionados")
    
    # Converte defaultdict para dict regular
    grafo_dict = dict(graph.adj_list)
    
    # Calcula centralidade de proximidade para todos os atores
    centralidades = algoritmos.closeness_centrality(grafo_dict)
    
    actor_centralities = []
    for node in graph.nodes:
        centrality = centralidades.get(node, 0.0)
        actor_centralities.append((node, centrality))
    
    # Ordena por centralidade decrescente
    actor_centralities.sort(key=lambda x: x[1], reverse=True)
    
    return actor_centralities[:top_n]

def get_top_directors_string(graph, top_n=10):
    """
    Retorna uma string formatada com os top N diretores mais influentes.
    """
    top_directors = get_top_directors_by_centrality(graph, top_n)
    
    info = f"╰┈┈➤ Top {top_n} Diretores Mais Influentes (por Centralidade de Grau)\n\n"
    info += f"{'Rank':<4} {'Diretor':<30} {'Centralidade':<12} {'Grau de Entrada':<15}\n"
    info += "-" * 70 + "\n"
    
    for i, (director, centrality, in_degree) in enumerate(top_directors, 1):
        info += f"{i:<4} {director:<30} {centrality:<12.6f} {in_degree:<15}\n"
    
    info += "\n"
    return info

def get_top_directors_betweenness_string(graph, top_n=10):
    """
    Retorna uma string formatada com os top N diretores por centralidade de intermediação.
    """
    top_directors = get_top_directors_by_betweenness(graph, top_n)
    
    info = f"╰┈┈➤ Top {top_n} Diretores Mais Influentes (por Centralidade de Intermediação)\n\n"
    info += "Centralidade de Intermediação: Mede o quão importante um diretor é como 'ponte' entre atores.\n"
    info += "Diretores com alta centralidade de intermediação conectam diferentes grupos de atores.\n\n"
    info += f"{'Rank':<4} {'Diretor':<30} {'Centralidade':<12}\n"
    info += "-" * 50 + "\n"
    
    for i, (director, centrality) in enumerate(top_directors, 1):
        info += f"{i:<4} {director:<30} {centrality:<12.6f}\n"
    
    info += "\n"
    return info

def get_top_directors_closeness_string(graph, top_n=10):
    """
    Retorna uma string formatada com os top N diretores por centralidade de proximidade.
    """
    top_directors = get_top_directors_by_closeness(graph, top_n)
    
    info = f"╰┈┈➤ Top {top_n} Diretores Mais Influentes (por Centralidade de Proximidade)\n\n"
    info += "Centralidade de Proximidade: Mede quão próximo um diretor está de todos os outros atores.\n"
    info += "Diretores com alta centralidade de proximidade podem influenciar rapidamente toda a rede.\n\n"
    info += f"{'Rank':<4} {'Diretor':<30} {'Centralidade':<12}\n"
    info += "-" * 50 + "\n"
    
    for i, (director, centrality) in enumerate(top_directors, 1):
        info += f"{i:<4} {director:<30} {centrality:<12.6f}\n"
    
    info += "\n"
    return info

def get_top_actors_degree_string(graph, top_n=10):
    """
    Retorna uma string formatada com os top N atores por centralidade de grau.
    """
    top_actors = get_top_actors_by_degree(graph, top_n)
    
    info = f"╰┈┈➤ Top {top_n} Atores/Atrizes Mais Influentes (por Centralidade de Grau)\n\n"
    info += "Centralidade de Grau: Mede quantas conexões diretas um ator tem com outros atores.\n"
    info += "Atores com alta centralidade de grau trabalharam com muitos outros atores.\n\n"
    info += f"{'Rank':<4} {'Ator/Atriz':<30} {'Centralidade':<12} {'Grau':<8}\n"
    info += "-" * 60 + "\n"
    
    for i, (actor, centrality, degree) in enumerate(top_actors, 1):
        info += f"{i:<4} {actor:<30} {centrality:<12.6f} {degree:<8}\n"
    
    info += "\n"
    return info

def get_top_actors_betweenness_string(graph, top_n=10):
    """
    Retorna uma string formatada com os top N atores por centralidade de intermediação.
    """
    top_actors = get_top_actors_by_betweenness(graph, top_n)
    
    info = f"╰┈┈➤ Top {top_n} Atores/Atrizes Mais Influentes (por Centralidade de Intermediação)\n\n"
    info += "Centralidade de Intermediação: Mede o quão importante um ator é como 'ponte' entre outros atores.\n"
    info += "Atores com alta centralidade de intermediação conectam diferentes grupos de atores.\n\n"
    info += f"{'Rank':<4} {'Ator/Atriz':<30} {'Centralidade':<12}\n"
    info += "-" * 50 + "\n"
    
    for i, (actor, centrality) in enumerate(top_actors, 1):
        info += f"{i:<4} {actor:<30} {centrality:<12.6f}\n"
    
    info += "\n"
    return info

def get_top_actors_closeness_string(graph, top_n=10):
    """
    Retorna uma string formatada com os top N atores por centralidade de proximidade.
    """
    top_actors = get_top_actors_by_closeness(graph, top_n)
    
    info = f"╰┈┈➤ Top {top_n} Atores/Atrizes Mais Influentes (por Centralidade de Proximidade)\n\n"
    info += "Centralidade de Proximidade: Mede quão próximo um ator está de todos os outros atores.\n"
    info += "Atores com alta centralidade de proximidade podem influenciar rapidamente toda a rede.\n\n"
    info += f"{'Rank':<4} {'Ator/Atriz':<30} {'Centralidade':<12}\n"
    info += "-" * 50 + "\n"
    
    for i, (actor, centrality) in enumerate(top_actors, 1):
        info += f"{i:<4} {actor:<30} {centrality:<12.6f}\n"
    
    info += "\n"
    return info

def analyze_degree_distribution(graph, graph_name):
    """
    Analisa a distribuição de graus de um grafo.
    
    Args:
        graph (Grafo): O grafo a ser analisado
        graph_name (str): Nome do grafo para identificação
    
    Returns:
        str: String formatada com a análise da distribuição de graus
    """
    # Calcula os graus de todos os nós
    degrees = []
    for node in graph.nodes:
        if graph.directed:
            # Para grafo direcionado: grau de entrada + grau de saída
            out_degree = len(graph.adj_list.get(node, []))
            in_degree = sum(1 for adj_list in graph.adj_list.values() 
                           for neighbor, _ in adj_list if neighbor == node)
            degree = out_degree + in_degree
        else:
            # Para grafo não direcionado: número de vizinhos
            degree = len(graph.adj_list.get(node, []))
        degrees.append(degree)
    
    # Estatísticas básicas
    total_nodes = len(degrees)
    avg_degree = sum(degrees) / total_nodes if total_nodes > 0 else 0
    max_degree = max(degrees) if degrees else 0
    min_degree = min(degrees) if degrees else 0
    
    # Distribuição de graus (quantos nós têm cada grau)
    degree_dist = Counter(degrees)
    
    # Características de rede complexa
    # Verifica se segue distribuição de potência (scale-free)
    high_degree_nodes = sum(1 for d in degrees if d > avg_degree * 2)
    low_degree_nodes = sum(1 for d in degrees if d <= avg_degree / 2)
    
    # Calcula coeficiente de variação
    variance = sum((d - avg_degree) ** 2 for d in degrees) / total_nodes if total_nodes > 0 else 0
    std_dev = variance ** 0.5
    cv = std_dev / avg_degree if avg_degree > 0 else 0
    
    info = f"ANÁLISE DA DISTRIBUIÇÃO DE GRAUS - {graph_name}\n"
    info += "=" * 60 + "\n\n"
    
    info += f"Estatísticas Básicas:\n"
    info += f"- Número total de nós: {total_nodes}\n"
    info += f"- Grau médio: {avg_degree:.2f}\n"
    info += f"- Grau máximo: {max_degree}\n"
    info += f"- Grau mínimo: {min_degree}\n"
    info += f"- Desvio padrão: {std_dev:.2f}\n"
    info += f"- Coeficiente de variação: {cv:.2f}\n\n"
    
    info += f"Distribuição de Graus:\n"
    info += f"{'Grau':<8} {'Frequência':<12} {'Percentual':<12}\n"
    info += "-" * 35 + "\n"
    
    # Ordena por grau
    for degree in sorted(degree_dist.keys()):
        freq = degree_dist[degree]
        percent = (freq / total_nodes) * 100
        info += f"{degree:<8} {freq:<12} {percent:<12.2f}%\n"
    
    info += "\n"
    
    # Análise de características de rede complexa
    info += f"Características de Rede Complexa:\n"
    info += f"- Nós com grau alto (> {avg_degree*2:.1f}): {high_degree_nodes} ({high_degree_nodes/total_nodes*100:.1f}%)\n"
    info += f"- Nós com grau baixo (≤ {avg_degree/2:.1f}): {low_degree_nodes} ({low_degree_nodes/total_nodes*100:.1f}%)\n"
    
    # Interpretação
    if cv > 1.0:
        info += f"- Alta heterogeneidade (CV = {cv:.2f} > 1.0): Característica de redes scale-free\n"
    else:
        info += f"- Baixa heterogeneidade (CV = {cv:.2f} ≤ 1.0): Rede mais homogênea\n"
    
    if high_degree_nodes > 0 and high_degree_nodes < total_nodes * 0.1:
        info += f"- Presença de hubs (nós com grau muito alto): {high_degree_nodes} nós\n"
    
    info += "\n"
    return info

def analyze_component_distribution(undirected_graph, directed_graph):
    """
    Analisa a distribuição de componentes conexas e fortemente conexas.
    
    Args:
        undirected_graph (Grafo): Grafo não direcionado
        directed_graph (Grafo): Grafo direcionado
    
    Returns:
        str: String formatada com a análise das componentes
    """
    info = "ANÁLISE DE COMPONENTES CONEXAS E FORTEMENTE CONEXAS\n"
    info += "=" * 60 + "\n\n"
    
    # Componentes conexas (grafo não direcionado)
    print("Calculando componentes conexas...")
    comp_conexas = algoritmos.comp_conexas(undirected_graph)
    
    info += "1) COMPONENTES CONEXAS (Grafo Não Direcionado)\n"
    info += "-" * 50 + "\n"
    info += f"Número total de componentes: {len(comp_conexas)}\n\n"
    
    # Distribuição de tamanhos das componentes
    sizes = [len(comp) for comp in comp_conexas]
    size_dist = Counter(sizes)
    
    info += f"Distribuição de Tamanhos:\n"
    info += f"{'Tamanho':<10} {'Quantidade':<12} {'Percentual':<12}\n"
    info += "-" * 35 + "\n"
    
    for size in sorted(size_dist.keys()):
        freq = size_dist[size]
        percent = (freq / len(comp_conexas)) * 100
        info += f"{size:<10} {freq:<12} {percent:<12.1f}%\n"
    
    # Componente gigante
    giant_component_size = max(sizes) if sizes else 0
    giant_component_percent = (giant_component_size / len(undirected_graph.nodes)) * 100
    
    info += f"\nComponente Gigante:\n"
    info += f"- Tamanho: {giant_component_size} nós ({giant_component_percent:.1f}% do total)\n"
    info += f"- Componentes isoladas: {size_dist.get(1, 0)} nós\n\n"
    
    # Componentes fortemente conexas (grafo direcionado)
    print("Calculando componentes fortemente conexas...")
    comp_fortemente_conexas = algoritmos.comp_fortemente_conexas(directed_graph)
    
    info += "2) COMPONENTES FORTEMENTE CONEXAS (Grafo Direcionado)\n"
    info += "-" * 50 + "\n"
    info += f"Número total de componentes: {len(comp_fortemente_conexas)}\n\n"
    
    # Distribuição de tamanhos das componentes fortemente conexas
    sizes_scc = [len(comp) for comp in comp_fortemente_conexas]
    size_dist_scc = Counter(sizes_scc)
    
    info += f"Distribuição de Tamanhos:\n"
    info += f"{'Tamanho':<10} {'Quantidade':<12} {'Percentual':<12}\n"
    info += "-" * 35 + "\n"
    
    for size in sorted(size_dist_scc.keys()):
        freq = size_dist_scc[size]
        percent = (freq / len(comp_fortemente_conexas)) * 100
        info += f"{size:<10} {freq:<12} {percent:<12.1f}%\n"
    
    # Componente gigante fortemente conexa
    giant_scc_size = max(sizes_scc) if sizes_scc else 0
    giant_scc_percent = (giant_scc_size / len(directed_graph.nodes)) * 100
    
    info += f"\nComponente Gigante Fortemente Conexa:\n"
    info += f"- Tamanho: {giant_scc_size} nós ({giant_scc_percent:.1f}% do total)\n"
    info += f"- Componentes isoladas: {size_dist_scc.get(1, 0)} nós\n\n"
    
    # Interpretação
    info += "INTERPRETAÇÃO DOS RESULTADOS:\n"
    info += "-" * 30 + "\n"
    
    # Para componentes conexas
    if giant_component_percent > 50:
        info += f"✓ Grafo não direcionado: Presença de componente gigante ({giant_component_percent:.1f}%)\n"
        info += "  - Característica típica de redes complexas\n"
        info += "  - Alta conectividade entre atores\n"
    else:
        info += f"✗ Grafo não direcionado: Sem componente gigante dominante\n"
        info += "  - Rede mais fragmentada\n"
    
    if size_dist.get(1, 0) > 0:
        info += f"✓ {size_dist.get(1, 0)} atores isolados (não trabalharam com outros)\n"
    
    # Para componentes fortemente conexas
    if giant_scc_percent > 30:
        info += f"✓ Grafo direcionado: Componente gigante fortemente conexa ({giant_scc_percent:.1f}%)\n"
        info += "  - Forte influência mútua entre atores e diretores\n"
    else:
        info += f"✗ Grafo direcionado: Rede de influência mais fragmentada\n"
    
    if size_dist_scc.get(1, 0) > 0:
        info += f"✓ {size_dist_scc.get(1, 0)} nós isolados (sem influência mútua)\n"
    
    info += "\n"
    return info

# VERSÕES OTIMIZADAS PARA RELATÓRIO (MAIS RÁPIDAS)

def get_top_directors_by_betweenness_fast(graph, top_n=10, max_sources=100):
    """
    Versão otimizada para relatório - usa amostragem mais agressiva.
    """
    if not graph.directed:
        raise ValueError("Esta função só funciona com grafos direcionados")
    
    # Converte defaultdict para dict regular
    grafo_dict = dict(graph.adj_list)
    
    # Amostragem mais agressiva para relatório
    import random
    vertices = list(graph.nodes)
    if len(vertices) > max_sources:
        vertices_fonte = random.sample(vertices, max_sources)
    else:
        vertices_fonte = vertices
    
    director_centralities = []
    for node in graph.nodes:
        # Usa a função otimizada com amostragem
        centrality = algoritmos.betweenness_centrality(grafo_dict, node)
        director_centralities.append((node, centrality))
    
    # Ordena por centralidade decrescente
    director_centralities.sort(key=lambda x: x[1], reverse=True)
    
    return director_centralities[:top_n]

def get_top_directors_by_closeness_fast(graph, top_n=10, max_nodes=200):
    """
    Versão otimizada para relatório - calcula apenas para uma amostra.
    """
    if not graph.directed:
        raise ValueError("Esta função só funciona com grafos direcionados")
    
    # Converte defaultdict para dict regular
    grafo_dict = dict(graph.adj_list)
    
    # Amostragem para relatório
    import random
    vertices = list(graph.nodes)
    if len(vertices) > max_nodes:
        vertices_amostra = random.sample(vertices, max_nodes)
    else:
        vertices_amostra = vertices
    
    # Calcula centralidade de proximidade apenas para a amostra
    centralidades = algoritmos.closeness_centrality(grafo_dict, vertices_amostra)
    
    director_centralities = []
    for node in vertices_amostra:
        centrality = centralidades.get(node, 0.0)
        director_centralities.append((node, centrality))
    
    # Ordena por centralidade decrescente
    director_centralities.sort(key=lambda x: x[1], reverse=True)
    
    return director_centralities[:top_n]

def get_top_actors_by_betweenness_fast(graph, top_n=10, max_sources=100):
    """
    Versão otimizada para relatório - usa amostragem mais agressiva.
    """
    if graph.directed:
        raise ValueError("Esta função só funciona com grafos não direcionados")
    
    # Converte defaultdict para dict regular
    grafo_dict = dict(graph.adj_list)
    
    # Amostragem mais agressiva para relatório
    import random
    vertices = list(graph.nodes)
    if len(vertices) > max_sources:
        vertices_fonte = random.sample(vertices, max_sources)
    else:
        vertices_fonte = vertices
    
    actor_centralities = []
    for node in graph.nodes:
        # Usa a função otimizada com amostragem
        centrality = algoritmos.betweenness_centrality(grafo_dict, node)
        actor_centralities.append((node, centrality))
    
    # Ordena por centralidade decrescente
    actor_centralities.sort(key=lambda x: x[1], reverse=True)
    
    return actor_centralities[:top_n]

def get_top_actors_by_closeness_fast(graph, top_n=10, max_nodes=200):
    """
    Versão otimizada para relatório - calcula apenas para uma amostra.
    """
    if graph.directed:
        raise ValueError("Esta função só funciona com grafos não direcionados")
    
    # Converte defaultdict para dict regular
    grafo_dict = dict(graph.adj_list)
    
    # Amostragem para relatório
    import random
    vertices = list(graph.nodes)
    if len(vertices) > max_nodes:
        vertices_amostra = random.sample(vertices, max_nodes)
    else:
        vertices_amostra = vertices
    
    # Calcula centralidade de proximidade apenas para a amostra
    centralidades = algoritmos.closeness_centrality(grafo_dict, vertices_amostra)
    
    actor_centralities = []
    for node in vertices_amostra:
        centrality = centralidades.get(node, 0.0)
        actor_centralities.append((node, centrality))
    
    # Ordena por centralidade decrescente
    actor_centralities.sort(key=lambda x: x[1], reverse=True)
    
    return actor_centralities[:top_n]

def get_top_directors_betweenness_string_fast(graph, top_n=10):
    """
    Versão rápida para relatório.
    """
    top_directors = get_top_directors_by_betweenness_fast(graph, top_n)
    
    info = f"╰┈┈➤ Top {top_n} Diretores Mais Influentes (Centralidade de Intermediação) - VERSÃO OTIMIZADA\n\n"
    info += "Centralidade de Intermediação: Mede o quão importante um diretor é como 'ponte' entre atores.\n"
    info += "Diretores com alta centralidade de intermediação conectam diferentes grupos de atores.\n"
    info += "NOTA: Resultados baseados em amostragem para otimização de tempo.\n\n"
    info += f"{'Rank':<4} {'Diretor':<30} {'Centralidade':<12}\n"
    info += "-" * 50 + "\n"
    
    for i, (director, centrality) in enumerate(top_directors, 1):
        info += f"{i:<4} {director:<30} {centrality:<12.6f}\n"
    
    info += "\n"
    return info

def get_top_directors_closeness_string_fast(graph, top_n=10):
    """
    Versão rápida para relatório.
    """
    top_directors = get_top_directors_by_closeness_fast(graph, top_n)
    
    info = f"╰┈┈➤ Top {top_n} Diretores Mais Influentes (Centralidade de Proximidade) - VERSÃO OTIMIZADA\n\n"
    info += "Centralidade de Proximidade: Mede quão próximo um diretor está de todos os outros atores.\n"
    info += "Diretores com alta centralidade de proximidade podem influenciar rapidamente toda a rede.\n"
    info += "NOTA: Resultados baseados em amostragem para otimização de tempo.\n\n"
    info += f"{'Rank':<4} {'Diretor':<30} {'Centralidade':<12}\n"
    info += "-" * 50 + "\n"
    
    for i, (director, centrality) in enumerate(top_directors, 1):
        info += f"{i:<4} {director:<30} {centrality:<12.6f}\n"
    
    info += "\n"
    return info

def get_top_actors_betweenness_string_fast(graph, top_n=10):
    """
    Versão rápida para relatório.
    """
    top_actors = get_top_actors_by_betweenness_fast(graph, top_n)
    
    info = f"╰┈┈➤ Top {top_n} Atores/Atrizes Mais Influentes (Centralidade de Intermediação) - VERSÃO OTIMIZADA\n\n"
    info += "Centralidade de Intermediação: Mede o quão importante um ator é como 'ponte' entre outros atores.\n"
    info += "Atores com alta centralidade de intermediação conectam diferentes comunidades de atores.\n"
    info += "NOTA: Resultados baseados em amostragem para otimização de tempo.\n\n"
    info += f"{'Rank':<4} {'Ator/Atriz':<30} {'Centralidade':<12}\n"
    info += "-" * 50 + "\n"
    
    for i, (actor, centrality) in enumerate(top_actors, 1):
        info += f"{i:<4} {actor:<30} {centrality:<12.6f}\n"
    
    info += "\n"
    return info

def get_top_actors_closeness_string_fast(graph, top_n=10):
    """
    Versão rápida para relatório.
    """
    top_actors = get_top_actors_by_closeness_fast(graph, top_n)
    
    info = f"╰┈┈➤ Top {top_n} Atores/Atrizes Mais Influentes (Centralidade de Proximidade) - VERSÃO OTIMIZADA\n\n"
    info += "Centralidade de Proximidade: Mede quão próximo um ator está de todos os outros atores.\n"
    info += "Atores com alta centralidade de proximidade podem influenciar rapidamente toda a comunidade.\n"
    info += "NOTA: Resultados baseados em amostragem para otimização de tempo.\n\n"
    info += f"{'Rank':<4} {'Ator/Atriz':<30} {'Centralidade':<12}\n"
    info += "-" * 50 + "\n"
    
    for i, (actor, centrality) in enumerate(top_actors, 1):
        info += f"{i:<4} {actor:<30} {centrality:<12.6f}\n"
    
    info += "\n"
    return info