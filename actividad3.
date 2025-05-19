import random
import string
import networkx as nx
import matplotlib.pyplot as plt
import heapq

def generar_grafo_aleatorio(min_n=10, max_n=15, peso_min=4, peso_max=15):
    n = random.randint(min_n, max_n)
    letras = [f"{letra}{i+1}" for i, letra in enumerate(string.ascii_uppercase[:n])]
    G = nx.Graph()

    for letra in letras:
        G.add_node(letra)

    for i in range(1, n):
        u = letras[i]
        v = random.choice(letras[:i])
        peso = random.randint(peso_min, peso_max)
        G.add_edge(u, v, weight=peso)

    extra_aristas = random.randint(n, 2 * n)
    for _ in range(extra_aristas):
        u, v = random.sample(letras, 2)
        if not G.has_edge(u, v):
            peso = random.randint(peso_min, peso_max)
            G.add_edge(u, v, weight=peso)
    return G

def dijkstra_con_camino(G, origen):
    dist = {n: float('inf') for n in G.nodes}
    prev = {n: None for n in G.nodes}
    dist[origen] = 0
    heap = [(0, origen)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v in G.neighbors(u):
            peso = G[u][v]['weight']
            if dist[u] + peso < dist[v]:
                dist[v] = dist[u] + peso
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))
    return dist, prev

def reconstruir_camino(prev, destino):
    camino = []
    while destino and prev[destino]:
        camino.append((prev[destino], destino))
        destino = prev[destino]
    return camino[::-1]

def dibujar_grafo(G, camino, origen, destino):
    pos = nx.spring_layout(G, seed=42, k=0.15, iterations=20, scale=2)  # k pequeño = mayor separación
    pesos = nx.get_edge_attributes(G, 'weight')

    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='lightgray', node_size=400, font_size=8)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=pesos, font_size=7)

    if camino:
        nx.draw_networkx_edges(G, pos, edgelist=camino, edge_color='red', width=2)

    plt.title(f"Camino mínimo de {origen} a {destino}")
    plt.show()

def imprimir_camino(camino, G):
    total = 0
    for u, v in camino:
        peso = G[u][v]['weight']
        print(f"{u} -> {v} (peso: {peso})")
        total += peso
    print(f"Peso total del camino: {total}\n")

G = generar_grafo_aleatorio()
nodos = sorted(G.nodes)
origen = nodos[0]
destinos = random.sample([n for n in nodos if n != origen], 5)

print(f"Nodo origen: {origen}")
print(f"Nodos destino: {', '.join(destinos)}\n")

for destino in destinos:
    distancias, anteriores = dijkstra_con_camino(G, origen)
    camino = reconstruir_camino(anteriores, destino)
    dibujar_grafo(G, camino, origen, destino)
    print(f"Camino de {origen} a {destino}:")
    imprimir_camino(camino, G)
