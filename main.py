import algoritmos
import grafos
from collections import defaultdict
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

# Cria o conteúdo completo para salvar no arquivo
conteudo = "⋆⁺₊⋆ ━━━━⊱❀ TDE 5 - REDES COMPLEXAS ❀⊰━━━━ ⋆⁺₊⋆\n"
conteudo += "ˋ°•*⁀➷ Alex Menegatti Secco, Mariana de Castro e Tarso Bertolini Rodrigues ✶࿐\n\n"
conteudo += "╰┈┈➤ Criação dos Grafos\n"
conteudo += f"Grafo Direcionado (Ator->Diretor): {nodes_d} vértices, {edges_d} arestas\n"
conteudo += f"Grafo Não Direcionado (Ator<->Ator): {nodes_u} vértices, {edges_u} arestas\n\n"

print("cfc em andamento")
# Componentes fortemente conexas (direcionado)
conteudo += "╰┈┈➤ Componentes Fortemente conexas (direcionado)\n"
comp_fortemente_conexas = algoritmos.comp_fortemente_conexas(grafo_direcionado)
conteudo += f"Número de componentes fortemente conexas: {len(comp_fortemente_conexas)}\n\n"

for i, componente in enumerate(comp_fortemente_conexas, 1):
    conteudo += f"Componente Fortemente Conexa {i} ({len(componente)} nós):\n"
    conteudo += f"  {', '.join(componente)}\n\n"

print("cfc concluido")

print("cc em andamento")
# Componentes conexas (não direcionado)
conteudo += "╰┈┈➤ Componentes Conexas (não direcionado)\n"
comp_conexas = algoritmos.comp_conexas(grafo_nao_direcionado)
conteudo += f"Número de componentes conexas: {len(comp_conexas)}\n\n"

for i, componente in enumerate(comp_conexas, 1):
    conteudo += f"Componente Conexa {i} ({len(componente)} nós):\n"
    conteudo += f"  {', '.join(componente)}\n\n"

print("cc concluido")

print("arvore em andamento")
conteudo += "╰┈┈➤ Árvore Geradora Mínima\n"
test_node = "BOB ODENKIRK"
mst_edges, total_cost = algoritmos.mst_prim(grafo_nao_direcionado, test_node)
conteudo += algoritmos.get_mst_info_string(test_node, mst_edges, total_cost)
print("arvore concluido")

print("grau em andamento")
conteudo += "╰┈┈➤ Centralidade de Grau\n"

conteudo += "✿ GRAFO NÃO DIRECIONADO ✿\n"
conteudo += algoritmos.get_degree_centrality_string(grafo_nao_direcionado, test_node)

conteudo += "━⊱⋆⊰"*10 + "\n"
conteudo += "✿ GRAFO DIRECIONADO ✿\n"
conteudo += algoritmos.get_degree_centrality_string(grafo_direcionado, test_node)
print("grau concluido")

print("intermed em andamento")
conteudo += "╰┈┈➤ Centralidade de Intermediação\n"
conteudo += algoritmos.get_betweenness_centrality_string(grafo_nao_direcionado, test_node)
print("intermed concluido")

print("prox em andamento")
conteudo += "╰┈┈➤ Centralidade de Proximidade\n"
conteudo += algoritmos.get_closeness_centrality_string(grafo_nao_direcionado, test_node)
print("prox concluido")

# Salva tudo em um arquivo
to_txt("resultados_completos.txt", conteudo)
print("Resultados salvos em 'resultados/resultados_completos.txt'")


