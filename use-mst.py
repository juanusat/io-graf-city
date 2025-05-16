import argparse
import matplotlib.pyplot as plt
import networkx as nx
from mst_algorithms import kruskal, prim


def read_graph(filename):
    edges = []
    nodes = set()
    with open(filename) as f:
        for line in f:
            parts = line.strip().split()
            if not parts or parts[0].startswith('#'):
                continue
            u, v, w = parts[0], parts[1], float(parts[2])
            nodes.update([u, v])
            edges.append((u, v, w))
    adj = {n: [] for n in nodes}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return list(nodes), edges, adj


def draw_graph_with_mst(nodes, edges, mst_edges, image_file, rows=None, cols=None):
    G = nx.Graph()
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    if rows and cols:
        pos = {n: (int(n) % cols, - (int(n) // cols)) for n in nodes}
    else:
        pos = nx.spring_layout(G)

    plt.figure(figsize=(8, 8))
    nx.draw(G, pos, with_labels=True, node_size=200, node_color='lightgrey', edge_color='lightgrey')

    mst_graph = nx.Graph()
    for u, v, w in mst_edges:
        mst_graph.add_edge(u, v, weight=w)

    nx.draw_networkx_nodes(mst_graph, pos, node_size=200, node_color='red')
    nx.draw_networkx_edges(mst_graph, pos, width=2.0, edge_color='red')

    edge_labels = { (u, v): f"{w:.1f}" for u, v, w in mst_edges }
    nx.draw_networkx_edge_labels(mst_graph, pos, edge_labels=edge_labels, font_color='red', font_size=6)

    plt.title("Árbol de Expansión Mínima en malla")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(image_file, dpi=300)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Compute and draw MST on grid-like or general graph.")
    parser.add_argument('-f', '--file', required=True, help="Graph file (edge list: u v w)")
    parser.add_argument('-a', '--algorithm', choices=['kruskal', 'prim'], required=True,
                        help="Algorithm to use: kruskal or prim")
    parser.add_argument('-i', '--image', help="Output image file to save MST visualization")
    parser.add_argument('-r', '--rows', type=int, help="(Optional) Número de filas para layout en malla")
    parser.add_argument('-c', '--cols', type=int, help="(Optional) Número de columnas para layout en malla")
    args = parser.parse_args()

    nodes, edges, adj = read_graph(args.file)
    if args.algorithm == 'kruskal':
        mst, total = kruskal(nodes, edges)
    else:
        mst, total = prim(nodes, adj)

    print(f"MST using {args.algorithm}:")
    for u, v, w in mst:
        print(f"{u} - {v}: {w}")
    print(f"Total weight: {total}")

    if args.image:
        draw_graph_with_mst(nodes, edges, mst, args.image, rows=args.rows, cols=args.cols)
        print(f"MST image saved to {args.image}")

if __name__ == '__main__':
    main()
