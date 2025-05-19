import random  # Para generar números aleatorios
import string  # Para generar etiquetas de nodos con letras
import networkx as nx  # Para crear y manipular grafos
import matplotlib.pyplot as plt  # Para dibujar el grafo
import heapq  # Para la cola de prioridad del algoritmo de Dijkstra

# ----------------------------------------
# Bloque: Generar un grafo aleatorio no dirigido con pesos
# ----------------------------------------
def generar_grafo_aleatorio(min_n=10, max_n=15, peso_min=4, peso_max=15):
    n = random.randint(min_n, max_n)  # Número aleatorio de nodos
    # Etiquetas de nodos, por ejemplo: A1, B2, C3, ...
    letras = [f"{letra}{i+1}" for i, letra in enumerate(string.ascii_uppercase[:n])]
    G = nx.Graph()  # Crear grafo no dirigido

    # Añadir nodos al grafo
    for letra in letras:
        G.add_node(letra)

    # Asegurar conectividad mínima: unir cada nodo nuevo con uno anterior
    for i in range(1, n):
        u = letras[i]
        v = random.choice(letras[:i])  # Conectar con un nodo ya agregado
        peso = random.randint(peso_min, peso_max)
        G.add_edge(u, v, weight=peso)

    # Añadir aristas adicionales aleatorias
    extra_aristas = random.randint(n, 2 * n)
    for _ in range(extra_aristas):
        u, v = random.sample(letras, 2)
        if not G.has_edge(u, v):
            peso = random.randint(peso_min, peso_max)
            G.add_edge(u, v, weight=peso)

    return G

# ----------------------------------------
# Bloque: Dijkstra para obtener distancias mínimas y predecesores
# ----------------------------------------
def dijkstra_con_camino(G, origen):
    dist = {n: float('inf') for n in G.nodes}  # Inicializar distancias
    prev = {n: None for n in G.nodes}          # Inicializar predecesores
    dist[origen] = 0
    heap = [(0, origen)]  # Cola de prioridad (distancia, nodo)

    # Algoritmo de Dijkstra
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue  # Ignorar si ya hay una distancia mejor
        for v in G.neighbors(u):
            peso = G[u][v]['weight']
            if dist[u] + peso < dist[v]:
                dist[v] = dist[u] + peso
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))
    return dist, prev

# ----------------------------------------
# Bloque: Reconstrucción del camino mínimo desde el nodo origen
# ----------------------------------------
def reconstruir_camino(prev, destino):
    camino = []  # Lista de aristas (u, v) en orden
    while destino and prev[destino]:
        camino.append((prev[destino], destino))  # Añadir arista del camino
        destino = prev[destino]  # Ir hacia el predecesor
    return camino[::-1]  # Invertir para mostrar desde el origen

# ----------------------------------------
# Bloque: Dibujar el grafo y resaltar el camino mínimo
# ----------------------------------------
def dibujar_grafo(G, camino, origen, destino):
    pos = nx.spring_layout(G, seed=42, k=0.15, iterations=20, scale=2)  # Layout de nodos
    pesos = nx.get_edge_attributes(G, 'weight')  # Obtener pesos de aristas

    # Dibujar nodos y aristas normales
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='lightgray', node_size=400, font_size=8)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=pesos, font_size=7)

    # Dibujar el camino mínimo en rojo
    if camino:
        nx.draw_networkx_edges(G, pos, edgelist=camino, edge_color='red', width=2)

    plt.title(f"Camino mínimo de {origen} a {destino}")
    plt.show()

# ----------------------------------------
# Bloque: Imprimir el camino mínimo y su peso total
# ----------------------------------------
def imprimir_camino(camino, G):
    total = 0
    for u, v in camino:
        peso = G[u][v]['weight']
        print(f"{u} -> {v} (peso: {peso})")
        total += peso
    print(f"Peso total del camino: {total}\n")

# ----------------------------------------
# Bloque principal: Generar grafo, elegir origen y destinos aleatorios
# ----------------------------------------
G = generar_grafo_aleatorio()  # Crear grafo aleatorio
nodos = sorted(G.nodes)  # Ordenar nodos alfabéticamente
origen = nodos[0]  # Tomar el primero como nodo origen
# Elegir 5 nodos distintos al origen como destinos
destinos = random.sample([n for n in nodos if n != origen], 5)

print(f"Nodo origen: {origen}")
print(f"Nodos destino: {', '.join(destinos)}\n")

# ----------------------------------------
# Bloque: Ejecutar Dijkstra y mostrar resultados para cada destino
# ----------------------------------------
for destino in destinos:
    distancias, anteriores = dijkstra_con_camino(G, origen)  # Ejecutar Dijkstra
    camino = reconstruir_camino(anteriores, destino)          # Reconstruir camino
    dibujar_grafo(G, camino, origen, destino)                # Dibujar grafo y camino
    print(f"Camino de {origen} a {destino}:")
    imprimir_camino(camino, G)                                # Imprimir camino y peso
