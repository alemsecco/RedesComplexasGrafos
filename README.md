﻿# Análise de Redes Complexas na Indústria do Entretenimento

## 📋 Descrição do Projeto

Este projeto implementa uma análise completa de redes complexas aplicada à indústria do entretenimento, utilizando dados de filmes e séries da Netflix, Amazon e Disney. O sistema constrói e analisa dois tipos de grafos:

1. **Grafo Direcionado (Ator → Diretor)**: Representa colaborações entre atores e diretores
2. **Grafo Não Direcionado (Ator ↔ Ator)**: Representa co-atuacões entre atores

## 🏗️ Estrutura do Projeto

```
RedesComplexasGrafos/
├── grafos.py              # Implementação da classe Grafo e construção dos grafos
├── algoritmos.py          # Algoritmos de análise (componentes, MST, centralidades)
├── analises.py            # Funções de análise e ranking de influência
├── main.py                # Análise básica e salvamento de resultados
├── relatorio.py           # Relatório completo com todas as análises
├── netflix_amazon_disney_titles.csv  # Dataset de entrada
├── resultados/            # Pasta com arquivos de saída
│   ├── resultados_completos.txt
│   └── relatorio_completo.txt
└── README.md
```

## 🚀 Funcionalidades Implementadas

### 1. Construção de Grafos
- **Classe Grafo**: Implementação com lista de adjacências
- **Grafos Ponderados**: Pesos representam frequência de colaboração
- **Padronização**: Nomes em maiúsculas, ignorando entradas vazias
- **Suporte**: Grafos direcionados e não direcionados

### 2. Análise de Componentes
- **Componentes Conexas**: Para grafo não direcionado (DFS)
- **Componentes Fortemente Conexas**: Para grafo direcionado (Algoritmo de Kosaraju)
- **Distribuição de Tamanhos**: Análise estatística das componentes

### 3. Árvore Geradora Mínima (MST)
- **Algoritmo de Prim**: Implementação com heap para eficiência
- **Componente Específica**: MST da componente que contém um nó dado
- **Custo Total**: Cálculo do peso total da MST

### 4. Métricas de Centralidade
- **Centralidade de Grau**: Número de conexões diretas
- **Centralidade de Intermediação**: Importância como "ponte" na rede
- **Centralidade de Proximidade**: Proximidade a todos os outros nós
- **Grafos Ponderados**: Todas as métricas adaptadas para pesos

### 5. Análise Estrutural
- **Distribuição de Graus**: Estatísticas e características de rede complexa
- **Identificação de Hubs**: Nós com grau muito alto
- **Características Scale-free**: Análise de heterogeneidade
- **Componente Gigante**: Análise de conectividade

### 6. Ranking de Influência
- **Top 10 Diretores**: Por cada métrica de centralidade
- **Top 10 Atores/Atrizes**: Por cada métrica de centralidade
- **Análise Comparativa**: Entre diferentes métricas

## 📊 Métricas de Centralidade

### Centralidade de Grau
- **O que mede**: Número de conexões diretas
- **Para diretores**: Quantos atores trabalharam com ele
- **Para atores**: Quantos outros atores trabalharam com ele

### Centralidade de Intermediação
- **O que mede**: Importância como "ponte" entre outros nós
- **Contexto**: Controle do fluxo de informação/influência
- **Algoritmo**: Brandes para grafos ponderados (Dijkstra)

### Centralidade de Proximidade
- **O que mede**: Proximidade a todos os outros nós
- **Contexto**: Capacidade de influenciar rapidamente toda a rede
- **Algoritmo**: Dijkstra para distâncias mínimas

## 🔧 Como Usar

### Pré-requisitos
```bash
pip install pandas
```

### Execução Básica
```bash
python main.py
```

### Relatório Completo
```bash
python relatorio.py
```

### Análise Individual
```python
import grafos
import algoritmos
import analises

# Carregar dados
cast_list, director_list = grafos.read_csv('netflix_amazon_disney_titles.csv')

# Construir grafos
grafo_direcionado = grafos.directed_graph(cast_list, director_list)
grafo_nao_direcionado = grafos.undirected_graph(cast_list)

# Análises específicas
centralidade = algoritmos.degree_centrality(grafo_nao_direcionado, "BOB ODENKIRK")
componentes = algoritmos.comp_conexas(grafo_nao_direcionado)
mst = algoritmos.mst_prim(grafo_nao_direcionado, "BOB ODENKIRK")
```

## 📈 Análises Disponíveis

### 1. Análise Estrutural
- Distribuição de graus e características de rede complexa
- Análise de componentes conexas e fortemente conexas
- Identificação de hubs e padrões scale-free

### 2. Análise de Centralidade
- Ranking dos 10 diretores mais influentes por cada métrica
- Ranking dos 10 atores/atrizes mais influentes por cada métrica
- Comparação entre diferentes métricas de influência

### 3. Análise de Conectividade
- Componente gigante e fragmentação da rede
- Isolamento de nós e padrões de colaboração
- Estrutura de influência na indústria

## 📁 Arquivos de Saída

### resultados_completos.txt
- Informações básicas dos grafos
- Componentes conexas e fortemente conexas
- Árvore geradora mínima
- Centralidades para nó de teste

### relatorio_completo.txt
- **Parte 1**: Análise estrutural completa
- **Parte 2**: Rankings de influência
- **Parte 3**: Explicações e interpretações

## 🎯 Questões Respondidas

### Análise Estrutural
1. **Distribuição de graus**: Características de rede complexa e scale-free
2. **Componentes**: Conectividade e fragmentação da rede

### Análise de Influência
4. **Top 10 diretores** - Centralidade de intermediação
5. **Top 10 diretores** - Centralidade de proximidade
6. **Top 10 atores** - Centralidade de grau
7. **Top 10 atores** - Centralidade de intermediação
8. **Top 10 atores** - Centralidade de proximidade

## 🔬 Algoritmos Implementados

- **DFS/BFS**: Para componentes conexas
- **Kosaraju**: Para componentes fortemente conexas
- **Prim**: Para árvore geradora mínima
- **Brandes**: Para centralidade de intermediação
- **Dijkstra**: Para centralidade de proximidade
- **Amostragem**: Para otimização em grafos grandes

## 👥 Autores

- Alex Menegatti Secco
- Mariana de Castro
- Tarso Bertolini Rodrigues

## 📝 Licença

Este projeto foi desenvolvido para o TDE 5 - Redes Complexas da disciplina de Resolução de Problemas com Grafos, ministrada pelo Prof. Dr. Vinícius Mourão Alves de Souza.
