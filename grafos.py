import csv
from collections import defaultdict

class Grafo:
    def __init__(self, directed=False):
        self.directed = directed # se o grafo é direcionado ou não
        self.adj_list = defaultdict(list)  # Lista de adjacências
        self.nodes = set()               # Conjunto de vértices
        self.n_edges = 0

    def add_node(self, v):
        #Adiciona um vértice 
        self.nodes.add(v)

    def add_edge(self, u, v, weight=1): # u e v são os vértices e weight é o peso da aresta (se n tiver peso fica 1)
        """
        add aresta entre dois vértices
        se o grafo for direcionado, adiciona a aresta no sentido u -> v
        se o grafo não for direcionado, adiciona a aresta nos 2 sentidos
        """
        self.nodes.update([u, v])

        # se a aresta já existir, soma o peso
        for idx, (viz, peso_atual) in enumerate(self.adj_list[u]):
            if viz == v:
                self.adj_list[u][idx] = (viz, peso_atual + weight)
                if not self.directed:
                    for jdx, (viz2, peso_atual2) in enumerate(self.adj_list[v]):
                        if viz2 == u:
                            self.adj_list[v][jdx] = (viz2, peso_atual2 + weight)
                return

        # se a aresta ainda não existir, cria
        self.adj_list[u].append((v, weight))
        self.n_edges += 1

        if not self.directed:
            # se a aresta pro outro sentido ainda não existir, cria
            if not any(viz == u for viz, _ in self.adj_list[v]):
                self.adj_list[v].append((u, weight))

    def get_numbers(self):
        # número de vértices e arestas do grafo
        n_nodes = len(self.nodes)
        if self.directed:
            n_edges = self.n_edges  # cada aresta contada uma vez
        else:
            n_edges = self.n_edges // 2  # cada aresta contada duas vezes (a-b e b-a), então divide por 2
        return n_nodes, n_edges



def directed_graph(cast_list, director_list):
    """
    grafo direcionado atores -> diretores
    peso = quantas vezes o ator trabalhou com o diretor
    """
    graph = Grafo(directed=True)

    for cast, director_list in zip(cast_list, director_list):
        for actor in cast:
            for director in director_list:
                graph.add_edge(actor, director, 1)

    return graph

def undirected_graph(cast_list):
    """
    grafo não direcionado atores <-> atores
    peso = quantas vezes os atores atuaram juntos
    """
    graph = Grafo(directed=False)

    for cast in cast_list:
        for i in range(len(cast)):
            for j in range(i + 1, len(cast)):
                graph.add_edge(cast[i], cast[j], 1)

    return graph


def to_upper(name):
    # padroniza o nome em maiúsculas sem espaços extras
    return name.strip().upper()


def read_csv(file_csv):
    # lê os dados do csv e retorna listas de elenco e diretores
    cast_list = []
    director_list = []
    
    with open(file_csv, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # processa diretores
            directors = [to_upper(d) for d in row['director'].split(',') if d.strip()]
            
            # processa elenco
            cast = [to_upper(a) for a in row['cast'].split(',') if a.strip()]
            
            # ignora entradas com diretor ou elenco vazios
            if directors and cast:
                director_list.append(directors)
                cast_list.append(cast)
    
    return cast_list, director_list


if __name__ == "__main__":
    # lê os dados do csv
    cast_list, director_list = read_csv('netflix_amazon_disney_titles.csv')
    
    # constrói o grafo direcionado (ator -> diretor)
    grafo_direcionado = directed_graph(cast_list, director_list)
    nodes_d, edges_d = grafo_direcionado.get_numbers()
    
    # constrói o grafo não direcionado (ator <-> ator)
    grafo_atores = undirected_graph(cast_list)
    nodes_u, edges_u = grafo_atores.get_numbers()
    
    # exibe os resultados
    print(f"Grafo Direcionado (Ator->Diretor): {nodes_d} vértices, {edges_d} arestas")
    print(f"Grafo Não Direcionado (Ator<->Ator): {nodes_u} vértices, {edges_u} arestas")
