import networkx as nx  # Para trabajar con grafos dirigidos y atributos
import matplotlib.pyplot as plt  # Para dibujar el grafo

# Nombre del fichero con la definición del modelo de flujo
filename = "modelo-g3.txt"
# Flag para decidir si dibujar o no el grafo
dibujar = True

# ----------------------------------
# Bloque: Lectura de datos de archivo
# ----------------------------------
edges = []      # Lista para almacenar las aristas como tuplas (u, v, capacidad, flujo_usado)
source = None   # Nodo fuente
sink = None     # Nodo sumidero

with open(filename, "r") as f:
    for line in f:
        line = line.strip()  # Quitar espacios y saltos de línea
        if not line or line.startswith("#"):
            continue  # Ignorar líneas vacías o comentarios
        parts = line.split()
        if len(parts) == 2:
            # Línea con sólo fuente y sumidero
            source, sink = map(int, parts)
        elif len(parts) == 4:
            # Línea con arista: u v cap flujo_usado
            u, v, cap, flow_used = map(int, parts)
            edges.append((u, v, cap, flow_used))
        else:
            # Formato inesperado
            raise ValueError(f"Línea con formato inesperado: {line!r}")

# ----------------------------------
# Bloque: Construcción de diccionarios de capacidad y flujo
# ----------------------------------
capacity = {}   # Diccionario para capacidad de cada arista
flow_used = {}  # Diccionario para flujo usado en cada arista

for u, v, cap, f_used in edges:
    capacity[(u, v)] = cap       # Asignar capacidad
    flow_used[(u, v)] = f_used   # Asignar flujo usado

# Mostrar resultados básicos por consola
print(f"Fuente = {source}, Sumidero = {sink}\n")
print("Aristas (u->v : capacidad / flujo_usado):")
for (u, v), cap in capacity.items():
    fu = flow_used.get((u, v), 0)
    print(f"  {u}->{v} : {cap} / {fu}")

# ----------------------------------
# Bloque: Dibujo del grafo con NetworkX y Matplotlib
# ----------------------------------
if dibujar:
    G = nx.DiGraph()  # Grafo dirigido
    for (u, v), cap in capacity.items():
        fu = flow_used.get((u, v), 0)
        # Añadir arista con etiqueta "capacidad/flujo"
        G.add_edge(u, v, label=f"{cap}/{fu}")

    pos = nx.spring_layout(G, seed=355)  # Layout automático con semilla fija
    plt.figure(figsize=(10, 6))
    nx.draw(
        G, pos,
        with_labels=True,        # Mostrar etiquetas de nodos
        node_color='skyblue',    # Color de nodos
        node_size=700,           # Tamaño de nodos
        font_weight='bold',      # Negrita en etiquetas
        arrows=True              # Flechas para grafo dirigido
    )
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    plt.title("Grafo con capacidades / flujo usado")
    plt.axis('off')  # Ocultar ejes
    plt.show()

from collections import deque  # Para Cola en Edmonds–Karp

# ----------------------------------
# Bloque: Implementación de Edmonds–Karp
# ----------------------------------
def edmonds_karp(capacity, s, t):
    residual = dict(capacity)  # Grafo residual inicial
    # Asegurar que exista residual[(u,v)] y residual[(v,u)] para todos los nodos
    nodes = set(u for u, _ in capacity) | set(v for _, v in capacity)
    for u in nodes:
        for v in nodes:
            residual.setdefault((u, v), 0)

    max_flow = 0
    iteration = 0

    while True:
        iteration += 1
        parent = {s: None}        # Para reconstruir el camino
        queue = deque([s])        # Cola BFS
        # BFS para encontrar camino aumentante
        while queue and t not in parent:
            u = queue.popleft()
            for v in nodes:
                if v not in parent and residual[(u, v)] > 0:
                    parent[v] = u
                    queue.append(v)

        if t not in parent:
            break  # No hay más caminos aumentantes

        # Reconstruir camino desde s hasta t
        path = []
        v = t
        while v != s:
            u = parent[v]
            path.append((u, v))
            v = u
        path.reverse()
        path_nodes = [s] + [v for _, v in path]

        # Calcular capacidades residuales en el camino
        capacities = [residual[(u, v)] for u, v in path]
        bottleneck = min(capacities)  # Valor mínimo en el camino

        print(f"Iteración {iteration} = nodos: {tuple(path_nodes)}, "
              f"capacidades: {tuple(capacities)}, mínimo = {bottleneck}")

        # Actualizar grafo residual
        for (u, v) in path:
            residual[(u, v)] -= bottleneck
            residual[(v, u)] += bottleneck

        max_flow += bottleneck

    print(f"Flujo máximo (Edmonds–Karp): {max_flow}")
    return max_flow

max_flow_ek = edmonds_karp(capacity, source, sink)

# ----------------------------------
# Bloque: Implementación de Ford–Fulkerson (con DFS recursivo)
# ----------------------------------
def ford_fulkerson(capacity, s, t):
    residual = dict(capacity)  # Grafo residual inicial
    nodes = set(u for u, _ in capacity) | set(v for _, v in capacity)
    for u in nodes:
        for v in nodes:
            residual.setdefault((u, v), 0)

    max_flow = 0
    iteration = 0

    # DFS recursivo para encontrar un camino aumentante
    def dfs(u, t, visited, flow):
        if u == t:
            return flow
        visited.add(u)
        for v in nodes:
            if (v not in visited) and residual[(u, v)] > 0:
                min_cap = min(flow, residual[(u, v)])
                pushed = dfs(v, t, visited, min_cap)
                if pushed > 0:
                    # Actualizar residual si se pushó flujo
                    residual[(u, v)] -= pushed
                    residual[(v, u)] += pushed
                    return pushed
        return 0

    # Iterar hasta que no queden caminos aumentantes
    while True:
        iteration += 1
        pushed = dfs(s, t, set(), float('inf'))
        if pushed == 0:
            break
        max_flow += pushed
        print(f"Iteración {iteration} (FF rec): flujo añadido = {pushed}")

    print(f"Flujo máximo (Ford–Fulkerson): {max_flow}")
    return max_flow

max_flow_ff = ford_fulkerson(capacity, source, sink)
