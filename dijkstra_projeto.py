"""
Projeto Integrador II - Algoritmo de Dijkstra (menor rota)
-----------------------------------------------------------
Este script implementa o algoritmo de Dijkstra de forma didática,
mostrando passo a passo como o menor caminho é calculado.

Como usar:
    python dijkstra_projeto.py

O programa vai LISTAR os pontos disponíveis e PEDIR que você digite
a origem e o destino. Em seguida calcula o menor caminho, mostra o
passo a passo e gera as imagens do grafo.

Ideia de aplicação: encontrar a rota mais curta entre pontos de uma
cidade (ex: praça, escola, mercado, hospital), simulando um "mini Google Maps".
"""

import heapq
import networkx as nx
import matplotlib.pyplot as plt


def dijkstra(grafo, origem, destino, verbose=True):
    """
    grafo: dicionário no formato:
        {
            'A': {'B': 5, 'C': 2},
            'B': {'D': 3},
            ...
        }
        onde as chaves são os nós, e os valores são dicionários
        {vizinho: peso_da_aresta}

    origem: nó inicial (string)
    destino: nó final (string)
    verbose: se True, imprime o passo a passo (ótimo para apresentação)

    Retorna: (distancia_total, caminho como lista de nós)
    """

    # Inicializa todas as distâncias como infinito, exceto a origem
    distancias = {no: float('inf') for no in grafo}
    distancias[origem] = 0

    # Guarda de onde viemos, para reconstruir o caminho no final
    anterior = {no: None for no in grafo}

    # Fila de prioridade (min-heap): (distancia_atual, no)
    fila = [(0, origem)]
    visitados = set()

    if verbose:
        print(f"\n=== Iniciando Dijkstra de '{origem}' até '{destino}' ===\n")

    while fila:
        dist_atual, no_atual = heapq.heappop(fila)

        if no_atual in visitados:
            continue
        visitados.add(no_atual)

        if verbose:
            print(f"Visitando '{no_atual}' (distância acumulada: {dist_atual})")

        # Se já chegamos no destino, podemos parar (otimização)
        if no_atual == destino:
            if verbose:
                print(f"Chegamos ao destino '{destino}'! Parando busca.\n")
            break

        # Analisa os vizinhos do nó atual
        for vizinho, peso in grafo[no_atual].items():
            if vizinho in visitados:
                continue

            nova_distancia = dist_atual + peso

            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                anterior[vizinho] = no_atual
                heapq.heappush(fila, (nova_distancia, vizinho))
                if verbose:
                    print(f"    -> Atualizando '{vizinho}': nova menor distância = {nova_distancia}")

    # Reconstrói o caminho percorrendo o dicionário 'anterior' de trás pra frente
    caminho = []
    no = destino
    while no is not None:
        caminho.insert(0, no)
        no = anterior[no]

    # Se a distância continua infinita, não existe caminho possível
    if distancias[destino] == float('inf'):
        return None, []

    return distancias[destino], caminho


def desenhar_grafo(grafo, caminho=None, nome_arquivo="grafo_dijkstra.png"):
    """
    Desenha o grafo usando networkx + matplotlib.
    Se um 'caminho' (lista de nós) for passado, ele é destacado em vermelho.

    Correções aplicadas:
    - Usa Graph (não-direcionado): como as distâncias são simétricas
      (ir de A para B custa o mesmo que voltar), cada ligação vira UMA
      aresta reta, sem setas duplicadas nem rótulos sobrepostos.
    - Layout kamada_kawai ponderado: o comprimento VISUAL de cada aresta
      tenta respeitar o peso real (pesos maiores = nós mais afastados).
    """
    # Graph simples (não-direcionado). Ao adicionar A-B e depois B-A,
    # o networkx entende que é a mesma aresta e não duplica.
    G = nx.Graph()
    for no, vizinhos in grafo.items():
        for vizinho, peso in vizinhos.items():
            G.add_edge(no, vizinho, weight=peso)

    # Layout que posiciona os nós tentando respeitar os pesos das arestas.
    # seed fixa deixa o desenho estável entre execuções.
    pos = nx.kamada_kawai_layout(G, weight="weight")

    plt.figure(figsize=(11, 7.5))

    # Nós e rótulos dos nós
    nx.draw_networkx_nodes(G, pos, node_color="#dbeafe",
                           node_size=2200, edgecolors="#1e3a8a")
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")

    # Arestas retas em cinza (uma por ligação, sem sobreposição)
    nx.draw_networkx_edges(G, pos, edge_color="#9ca3af", width=1.5)

    # Rótulos com o peso de cada aresta, com fundo branco para leitura limpa
    pesos = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=pesos, font_size=9, label_pos=0.5,
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85)
    )

    # Se houver caminho, destaca nós e arestas dele em vermelho
    if caminho and len(caminho) > 1:
        nx.draw_networkx_nodes(G, pos, nodelist=caminho, node_color="#fecaca",
                               node_size=2200, edgecolors="#b91c1c", linewidths=2)
        arestas_caminho = list(zip(caminho[:-1], caminho[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=arestas_caminho,
                               edge_color="#dc2626", width=3.5)
        titulo = f"Menor caminho: {' -> '.join(caminho)}"
    else:
        titulo = "Grafo da cidade (pontos e distâncias)"

    plt.title(titulo, fontsize=13, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(nome_arquivo, dpi=150)
    plt.close()
    print(f"Imagem salva em: {nome_arquivo}")


def imprimir_resultado(distancia, caminho):
    if distancia is None:
        print("Não existe caminho entre os pontos escolhidos.")
        return
    print("=" * 40)
    print(f"Menor distância encontrada: {distancia}")
    print(f"Caminho percorrido: {' -> '.join(caminho)}")
    print("=" * 40)


def escolher_ponto(grafo, texto):
    """
    Mostra os pontos numerados e deixa o usuário digitar o NOME ou o NÚMERO.
    Repete até receber uma entrada válida.
    """
    pontos = list(grafo.keys())
    while True:
        escolha = input(texto).strip()

        # Permite digitar pelo número da lista
        if escolha.isdigit():
            indice = int(escolha) - 1
            if 0 <= indice < len(pontos):
                return pontos[indice]
            print("  Número fora da lista. Tente novamente.")
            continue

        # Permite digitar o nome exato
        if escolha in grafo:
            return escolha

        # Aceita nome sem diferenciar maiúsculas/minúsculas
        for p in pontos:
            if p.lower() == escolha.lower():
                return p

        print("  Ponto não encontrado. Digite o nome exato ou o número da lista.")


if __name__ == "__main__":

    # -----------------------------------------------------------
    # EXEMPLO: pontos de uma cidade pequena (fictício)
    # Pode trocar pelos nomes reais que o grupo quiser usar
    # -----------------------------------------------------------
    grafo_cidade = {
        'Praça':        {'Escola': 4, 'Mercado': 2, 'Igreja': 3},
        'Escola':       {'Praça': 4, 'Mercado': 1, 'Hospital': 5},
        'Mercado':      {'Praça': 2, 'Escola': 1, 'Hospital': 8, 'Rodoviária': 6, 'Igreja': 2, 'Bar': 4},
        'Hospital':     {'Escola': 5, 'Mercado': 8, 'Rodoviária': 3, 'Universidade': 6},
        'Rodoviária':   {'Mercado': 6, 'Hospital': 3, 'Universidade': 3, 'Bairro Norte': 5},
        'Igreja':       {'Praça': 3, 'Mercado': 2, 'Praça de Esportes': 4},
        'Universidade': {'Hospital': 6, 'Rodoviária': 3, 'Bairro Norte': 4},
        'Bairro Norte': {'Rodoviária': 5, 'Universidade': 4, 'Praça de Esportes': 6, 'Bar': 3},
        'Praça de Esportes': {'Igreja': 4, 'Bairro Norte': 6},
        'Bar': {'Mercado': 4, 'Bairro Norte': 3},
    }

    # -------- Entrada interativa: usuário escolhe origem e destino --------
    print("\nPontos disponíveis:")
    for i, ponto in enumerate(grafo_cidade.keys(), start=1):
        print(f"  {i}. {ponto}")

    print("\n(Você pode digitar o NOME do ponto ou o NÚMERO correspondente)")
    origem = escolher_ponto(grafo_cidade, "\nDigite a ORIGEM: ")
    destino = escolher_ponto(grafo_cidade, "Digite o DESTINO: ")

    distancia, caminho = dijkstra(grafo_cidade, origem, destino, verbose=True)
    imprimir_resultado(distancia, caminho)

    # Gera duas imagens: o grafo "cru" e o grafo com o menor caminho destacado
    desenhar_grafo(grafo_cidade, caminho=None, nome_arquivo="grafo_cidade.png")
    if caminho:
        desenhar_grafo(grafo_cidade, caminho=caminho,
                       nome_arquivo="grafo_caminho_destacado.png")
