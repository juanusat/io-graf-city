#!/usr/bin/env python3
import argparse
import random
import networkx as nx
import matplotlib.pyplot as plt

def generate_grid_graph(rows, cols, wmin, wmax):
    G = nx.Graph()
    for i in range(rows):
        for j in range(cols):
            u = i * cols + j
            if j < cols - 1:
                v = i * cols + (j + 1)
                w = random.uniform(wmin, wmax)
                G.add_edge(u, v, weight=w)
            if i < rows - 1:
                v = (i + 1) * cols + j
                w = random.uniform(wmin, wmax)
                G.add_edge(u, v, weight=w)
    return G

def save_edge_list(G, path):
    with open(path, 'w') as f:
        for u, v, data in G.edges(data=True):
            f.write(f"{u} {v} {data['weight']:.3f}\n")

def draw_graph(G, path):
    pos = {}
    for u in G.nodes():
        i, j = divmod(u, cols)
        pos[u] = (j, -i)
    plt.figure(figsize=(cols, rows))
    nx.draw(G, pos, with_labels=True, node_size=300, font_size=8, edge_color='gray')
    labels = { (u,v): f"{d['weight']:.1f}" for u,v,d in G.edges(data=True) }
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=6)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(path, dpi=300)
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Genera un grafo en malla con pesos aleatorios.")
    parser.add_argument('-r', type=int, required=True, help="Número de filas")
    parser.add_argument('-c', type=int, required=True, help="Número de columnas")
    parser.add_argument('-f', type=float, required=True, help="Peso mínimo (f)")
    parser.add_argument('-t', type=float, required=True, help="Peso máximo (t)")
    parser.add_argument('-n', '--name', required=True, help="Nombre del test")
    args = parser.parse_args()

    rows = args.r
    cols = args.c
    wmin = args.f
    wmax = args.t
    name = args.name

    G = generate_grid_graph(rows, cols, wmin, wmax)

    txt_path = f"city-test-{name}.txt"
    png_path = f"city-test-{name}.png"

    save_edge_list(G, txt_path)
    print(f"Aristas guardadas en {txt_path}")

    draw_graph(G, png_path)
    print(f"Imagen del grafo guardada en {png_path}")
