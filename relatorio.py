import grafos
import analises
import os

def to_txt(file_name, content):
    os.makedirs("resultados", exist_ok=True)
    caminho = os.path.join("resultados", file_name)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(content)

# lê os dados do csv
cast_list, director_list = grafos.read_csv('netflix_amazon_disney_titles.csv')
    
# constrói o grafo direcionado (ator -> diretor)
grafo_direcionado = grafos.directed_graph(cast_list, director_list)
nodes_d, edges_d = grafo_direcionado.get_numbers()
    
# constrói o grafo não direcionado (ator <-> ator)
grafo_nao_direcionado = grafos.undirected_graph(cast_list)
nodes_u, edges_u = grafo_nao_direcionado.get_numbers()

# RELATÓRIO COMPLETO
relatorio = "ִ ࣪𖤐 RELATÓRIO COMPLETO - ANÁLISE DE REDES COMPLEXAS ִ ࣪𖤐\n\n"

# Informações básicas dos grafos
relatorio += "INFORMAÇÕES BÁSICAS DOS GRAFOS\n"
relatorio += "=" * 50 + "\n"
relatorio += f"Grafo Direcionado (Ator->Diretor): {nodes_d} vértices, {edges_d} arestas\n"
relatorio += f"Grafo Não Direcionado (Ator<->Ator): {nodes_u} vértices, {edges_u} arestas\n\n"

# ============================================================================
# ANÁLISE ESTRUTURAL
# ============================================================================

relatorio += "PARTE 1: ANÁLISE ESTRUTURAL DOS GRAFOS\n"
relatorio += "=" * 60 + "\n\n"

# 1) Análise da distribuição de graus
print("Analisando distribuição de graus do grafo direcionado...")
relatorio += "1) DISTRIBUIÇÃO DE GRAUS\n"
relatorio += "-" * 40 + "\n\n"

relatorio += analises.analyze_degree_distribution(grafo_direcionado, "GRAFO DIRECIONADO (ATOR->DIRETOR)", sample_size=100)

print("Analisando distribuição de graus do grafo não direcionado...")
relatorio += analises.analyze_degree_distribution(grafo_nao_direcionado, "GRAFO NÃO DIRECIONADO (ATOR<->ATOR)", sample_size=100)

# 2) Análise das componentes
print("Analisando distribuição de componentes...")
relatorio += "2) DISTRIBUIÇÃO DE COMPONENTES\n"
relatorio += "-" * 40 + "\n\n"

relatorio += analises.analyze_component_distribution(grafo_nao_direcionado, grafo_direcionado, sample_size=100)

# ============================================================================
# ANÁLISE DE CENTRALIDADE
# ============================================================================

relatorio += "PARTE 2: ANÁLISE DE CENTRALIDADE\n"
relatorio += "=" * 60 + "\n\n"

# 3) Top 10 diretores por centralidade de grau
print("Calculando centralidade de grau para diretores...")
relatorio += "3) TOP 10 DIRETORES MAIS INFLUENTES (Centralidade de Grau)\n"
relatorio += "-" * 60 + "\n"
relatorio += analises.get_top_directors_string(grafo_direcionado, 10)

# 4) Top 10 diretores por centralidade de intermediação
print("Calculando centralidade de intermediação para diretores...")
relatorio += "4) TOP 10 DIRETORES MAIS INFLUENTES (Centralidade de Intermediação)\n"
relatorio += "-" * 60 + "\n"
relatorio += analises.get_top_directors_betweenness_string_fast(grafo_direcionado, 10, sample_size=50)

# 5) Top 10 diretores por centralidade de proximidade
print("Calculando centralidade de proximidade para diretores...")
relatorio += "5) TOP 10 DIRETORES MAIS INFLUENTES (Centralidade de Proximidade)\n"
relatorio += "-" * 60 + "\n"
relatorio += analises.get_top_directors_closeness_string(grafo_direcionado, 10, sample_size=50)

# 6) Top 10 atores por centralidade de grau
print("Calculando centralidade de grau para atores...")
relatorio += "6) TOP 10 ATORES/ATRIZES MAIS INFLUENTES (Centralidade de Grau)\n"
relatorio += "-" * 60 + "\n"
relatorio += analises.get_top_actors_degree_string(grafo_nao_direcionado, 10)

# 7) Top 10 atores por centralidade de intermediação
print("Calculando centralidade de intermediação para atores...")
relatorio += "7) TOP 10 ATORES/ATRIZES MAIS INFLUENTES (Centralidade de Intermediação)\n"
relatorio += "-" * 60 + "\n"
relatorio += analises.fast_betweenness_actors(grafo_nao_direcionado, 10, sample_size=50)

# 8) Top 10 atores por centralidade de proximidade
print("Calculando centralidade de proximidade para atores...")
relatorio += "8) TOP 10 ATORES/ATRIZES MAIS INFLUENTES (Centralidade de Proximidade)\n"
relatorio += "-" * 60 + "\n"
relatorio += analises.get_top_actors_closeness_string(grafo_nao_direcionado, 10, sample_size=50)

# ============================================================================
# EXPLICAÇÕES E INTERPRETAÇÕES
# ============================================================================

relatorio += "PARTE 3: EXPLICAÇÕES E INTERPRETAÇÕES\n"
relatorio += "=" * 60 + "\n\n"

# Explicação das métricas de centralidade
relatorio += "EXPLICAÇÃO DAS MÉTRICAS DE CENTRALIDADE\n"
relatorio += "-" * 40 + "\n\n"

relatorio += "CENTRALIDADE DE GRAU:\n"
relatorio += "- Mede quantas conexões diretas um nó tem.\n"
relatorio += "- Para diretores: quantos atores trabalharam com ele.\n"
relatorio += "- Para atores: quantos outros atores trabalharam com ele.\n\n"

relatorio += "CENTRALIDADE DE INTERMEDIAÇÃO:\n"
relatorio += "- Mede o quão importante um nó é como 'ponte' entre outros nós.\n"
relatorio += "- Nós com alta centralidade controlam o fluxo de informação/influência.\n"
relatorio += "- Para diretores: conectam diferentes grupos de atores.\n"
relatorio += "- Para atores: conectam diferentes comunidades de atores.\n\n"

relatorio += "CENTRALIDADE DE PROXIMIDADE:\n"
relatorio += "- Mede quão próximo um nó está de todos os outros nós.\n"
relatorio += "- Nós com alta centralidade podem influenciar rapidamente toda a rede.\n"
relatorio += "- Para diretores: podem alcançar muitos atores rapidamente.\n"
relatorio += "- Para atores: podem influenciar toda a comunidade rapidamente.\n\n"

# Explicação das características de rede complexa
relatorio += "CARACTERÍSTICAS DE REDE COMPLEXA\n"
relatorio += "-" * 40 + "\n\n"

relatorio += "✓ Distribuição de Graus:\n"
relatorio += "  - Análise da heterogeneidade dos graus\n"
relatorio += "  - Identificação de hubs (nós com grau muito alto)\n"
relatorio += "  - Verificação de características scale-free\n\n"

relatorio += "✓ Componentes:\n"
relatorio += "  - Presença de componente gigante\n"
relatorio += "  - Fragmentação da rede\n"
relatorio += "  - Isolamento de nós\n\n"

relatorio += "✓ Interpretação:\n"
relatorio += "  - Redes scale-free têm alta heterogeneidade (CV > 1.0)\n"
relatorio += "  - Componente gigante indica alta conectividade\n"
relatorio += "  - Hubs são nós com grau muito superior à média\n\n"

relatorio += "✓ Contexto da Indústria do Entretenimento:\n"
relatorio += "  - Hubs representam atores/diretores muito ativos\n"
relatorio += "  - Componente gigante mostra a conectividade da indústria\n"
relatorio += "  - Centralidade indica influência e acesso a oportunidades\n"

to_txt("relatorio_completo.txt", relatorio)
print("Relatório completo gerado com sucesso em 'resultados/relatorio_completo.txt'.")