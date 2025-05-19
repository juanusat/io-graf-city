import networkx as nx
import matplotlib.pyplot as plt

filename = "modelo-g3.txt"
dibujar = True

edges = []
source = None
sink = None

with open(filename, "r") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) == 2:
            source, sink = map(int, parts)
        elif len(parts) == 4:
            u, v, cap, flow_used = map(int, parts)
            edges.append((u, v, cap, flow_used))
        else:
            raise ValueError(f"Línea con formato inesperado: {line!r}")

capacity = {}
flow_used = {}

for u, v, cap, f_used in edges:
    capacity[(u, v)] = cap
    flow_used[(u, v)] = f_used

print(f"Fuente = {source}, Sumidero = {sink}\n")
print("Aristas (u->v : capacidad / flujo_usado):")
for (u, v), cap in capacity.items():
    fu = flow_used.get((u, v), 0)
    print(f"  {u}->{v} : {cap} / {fu}")

if dibujar:
    G = nx.DiGraph()
    for (u, v), cap in capacity.items():
        fu = flow_used.get((u, v), 0)
        G.add_edge(u, v, label=f"{cap}/{fu}")

    pos = nx.spring_layout(G, seed=355)
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, font_weight='bold', arrows=True)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    plt.title("Grafo con capacidades / flujo usado")
    plt.axis('off')
    plt.show()


from collections import deque

def edmonds_karp(capacity, s, t):
    residual = dict(capacity)
    nodes = set(u for u, _ in capacity) | set(v for _, v in capacity)
    for u in nodes:
        for v in nodes:
            residual.setdefault((u, v), 0)

    max_flow = 0
    iteration = 0

    while True:
        iteration += 1
        parent = {s: None}
        queue = deque([s])
        while queue and t not in parent:
            u = queue.popleft()
            for v in nodes:
                if v not in parent and residual[(u, v)] > 0:
                    parent[v] = u
                    queue.append(v)

        if t not in parent:
            break

        path = []
        v = t
        while v != s:
            u = parent[v]
            path.append((u, v))
            v = u
        path.reverse()
        path_nodes = [s] + [v for _, v in path]

        capacities = [residual[(u, v)] for u, v in path]
        bottleneck = min(capacities)

        print(f"Iteración {iteration} = nodos: {tuple(path_nodes)}, "
              f"capacidades: {tuple(capacities)}, mínimo = {bottleneck}")

        for (u, v), flow in zip(path, [bottleneck]*len(path)):
            residual[(u, v)] -= flow
            residual[(v, u)] += flow

        max_flow += bottleneck

    print(f"Flujo máximo (Edmonds–Karp): {max_flow}")
    return max_flow

max_flow_ek = edmonds_karp(capacity, source, sink)

def ford_fulkerson(capacity, s, t):
    residual = dict(capacity)
    nodes = set(u for u, _ in capacity) | set(v for _, v in capacity)
    for u in nodes:
        for v in nodes:
            residual.setdefault((u, v), 0)

    max_flow = 0
    iteration = 0

    def dfs(u, t, visited, flow):
        if u == t:
            return flow
        visited.add(u)
        for v in nodes:
            if (v not in visited) and residual[(u, v)] > 0:
                min_cap = min(flow, residual[(u, v)])
                pushed = dfs(v, t, visited, min_cap)
                if pushed > 0:
                    residual[(u, v)] -= pushed
                    residual[(v, u)] += pushed
                    return pushed
        return 0

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
