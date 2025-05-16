import argparse
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon

def main(xi, yi, xf, yf):
    place = "Chiclayo, Lambayeque, Peru"
    G = ox.graph_from_place(place, network_type="drive")
    G_proj = ox.project_graph(G)
    nodes_proj = ox.graph_to_gdfs(G_proj, edges=False)
    minx, miny, maxx, maxy = nodes_proj.total_bounds
    width  = maxx - minx
    height = maxy - miny
    print(f"Mapa total proyectado: ancho = {width:.1f} m, alto = {height:.1f} m")
    origin_x = minx + (xi/100.0) * width
    origin_y = miny + (yi/100.0) * height
    crop_w = (xf/100.0) * width
    crop_h = (yf/100.0) * height
    print(f"Área recortada: ancho = {crop_w:.1f} m, alto = {crop_h:.1f} m")

    square = Polygon([
        (origin_x,          origin_y),
        (origin_x + crop_w, origin_y),
        (origin_x + crop_w, origin_y + crop_h),
        (origin_x,          origin_y + crop_h),
    ])
    fig0, ax0 = plt.subplots(figsize=(8, 8))
    ox.plot_graph(G_proj, ax=ax0, node_size=0, edge_color='lightgray',
                  edge_linewidth=0.5, show=False)
    gpd.GeoSeries([square], crs=G_proj.graph['crs']).plot(
        ax=ax0, facecolor='none', edgecolor='red', linewidth=2
    )
    ax0.set_title("Mapa de Chiclayo con área de recorte seleccionada")
    plt.tight_layout()
    plt.show()
    G_sub = ox.truncate.truncate_graph_polygon(G_proj, square)
    print(f"Subgrafo recortado: nodos = {len(G_sub.nodes)}, aristas = {len(G_sub.edges)}")
    G_ud = G_sub.to_undirected()
    mst_k = nx.minimum_spanning_tree(G_ud, weight='length', algorithm='kruskal')
    mst_p = nx.minimum_spanning_tree(G_ud, weight='length', algorithm='prim')
    def print_recorrido(mst, title):
        print(f"\nRecorrido del MST ({title}):")
        for u, v, data in mst.edges(data=True):
            name = data.get('name', 'Sin nombre')
            street = name[0] if isinstance(name, list) else name
            print(f"  Nodo {u} ↔ Nodo {v} : {street}")

    print_recorrido(mst_k, "Kruskal")
    print_recorrido(mst_p, "Prim")
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    ox.plot_graph(G_sub, ax=axs[0,1], node_size=10, edge_color='gray',
                  edge_linewidth=0.7, show=False)
    axs[0,1].set_title("Subgrafo recortado")
    ax = axs[1,0]
    ox.plot_graph(G_sub, ax=ax, node_size=0, edge_color='gray',
                  edge_linewidth=0.7, edge_alpha=0.2, show=False)
    ox.plot_graph(mst_k, ax=ax, node_size=5, edge_color='red',
                  edge_linewidth=1.2, edge_alpha=1.0, show=False)
    ax.set_title("MST con Kruskal")
    ax = axs[1,1]
    ox.plot_graph(G_sub, ax=ax, node_size=0, edge_color='gray',
                  edge_linewidth=0.7, edge_alpha=0.2, show=False)
    ox.plot_graph(mst_p, ax=ax, node_size=5, edge_color='blue',
                  edge_linewidth=1.2, edge_alpha=1.0, show=False)
    ax.set_title("MST con Prim")
    axs[0,0].axis('off')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Recorte porcentual de la red vial y cálculo de MST")
    parser.add_argument("--xi", type=float, default=31,
                        help="Posición inicial X (%) desde el borde izquierdo")
    parser.add_argument("--yi", type=float, default=55,
                        help="Posición inicial Y (%) desde el borde inferior")
    parser.add_argument("--xf", type=float, default=14,
                        help="Ancho del recorte (%) del ancho total")
    parser.add_argument("--yf", type=float, default=20,
                        help="Alto del recorte (%) del alto total")
    args, _ = parser.parse_known_args()
    main(args.xi, args.yi, args.xf, args.yf)