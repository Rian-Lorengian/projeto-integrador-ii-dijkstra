import heapq

# Grafo do mapa, representacao 

grafo = {
    "A": {"B": 3},
    "B": {"A": 3, "G": 3, "D": 2},
    "C": {"D": 2, "F": 10},
    "D": {"B": 2, "C": 2, "E": 5},
    "E": {"G": 3, "F": 3, "D": 5},
    "F": {"C": 10, "E": 3},
    "G": {"B": 3, "E": 3}
}

# Cria um dicionario para armazenar a distancia de cada vertice do grafo, inicializando com infinito
# a distancia aqui dentro considera, a disância da origem, até chegar em um ponto especifico
dist_from_origem = dict.fromkeys(grafo.keys(), float('inf'))

# Cria um dicionario para armazenar o vertice anterior de cada vertice do grafo
anterior = {}

# Cria um conjunto para armazenar os vertices visitados
visitados = set()

# Define a origem e o destino
origem = "A"
destino = "F"

# Inicializa a distancia da origem com 0
dist_from_origem[origem] = 0

# Cria uma fila de prioridade para armazenar os vertices a serem visitados
fila = []

# Adiciona a origem na fila de prioridade
heapq.heappush(fila, (dist_from_origem[origem], origem))

while fila:
    elemento_mais_perto = heapq.heappop(fila)
    distancia_atual = elemento_mais_perto[0]
    atual = elemento_mais_perto[1]

    if atual in visitados:
        continue
    else:
        visitados.add(atual)

    for vizinho in grafo[atual].items():    
        vizinho_nome = vizinho[0]
        vizinho_peso = vizinho[1]

        # nova distancia = Distancia percorrida da origem até (Atual) +
        # Distancia do (Atual) até o Vizinho que está sendo iterado
        nova_distancia = distancia_atual + vizinho_peso

        # se a distancia da origem até aqui, for menor, que a distancia da origem salva no 

        if nova_distancia  < dist_from_origem[vizinho_nome]:

            #aqui salvamos a nova melhor distancia
            dist_from_origem[vizinho_nome] = nova_distancia

            #aqui salvamos de onde veio para chegar na melhor distancia para ele
            anterior[vizinho_nome] = atual

            heapq.heappush(fila, (nova_distancia, vizinho_nome))


# print(dist_from_origem)
# print(anterior)

caminho = []
atual = destino

while atual != origem:
    caminho.append(atual)
    atual = anterior[atual]

if atual == origem:
    caminho.append(atual)

print(caminho)

size_caminho = len(caminho)
caminho_correto = []

repetir = True

for ponto in caminho:
    caminho_correto.append(ponto)

for ponto in caminho:
    size_caminho = size_caminho - 1
    caminho_correto[size_caminho] = ponto

print(caminho_correto)