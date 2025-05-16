def main(xi, yi, xf, yf):
    # Define el lugar de interés
    place = "Chiclayo, Lambayeque, Peru"

    # Obtiene el grafo de la red vial de la ciudad usando OpenStreetMap (tipo 'drive' = solo calles para vehículos)
    G = ox.graph_from_place(place, network_type="drive")

    # Proyecta el grafo a un sistema de coordenadas métrico (para trabajar en metros)
    G_proj = ox.project_graph(G)

    # Convierte los nodos del grafo proyectado a un GeoDataFrame (sin incluir las aristas)
    nodes_proj = ox.graph_to_gdfs(G_proj, edges=False)

    # Obtiene los límites extremos del grafo proyectado: (min x, min y, max x, max y)
    minx, miny, maxx, maxy = nodes_proj.total_bounds

    # Calcula el ancho y alto total del grafo en metros
    width  = maxx - minx
    height = maxy - miny

    # Imprime el tamaño total del mapa proyectado
    print(f"Mapa total proyectado: ancho = {width:.1f} m, alto = {height:.1f} m")

    # Calcula el punto de origen del área a recortar (en porcentaje del total)
    origin_x = minx + (xi/100.0) * width
    origin_y = miny + (yi/100.0) * height

    # Calcula el tamaño (ancho y alto) del recorte en metros, basado en porcentajes
    crop_w = (xf/100.0) * width
    crop_h = (yf/100.0) * height

    # Imprime las dimensiones del área recortada
    print(f"Área recortada: ancho = {crop_w:.1f} m, alto = {crop_h:.1f} m")

    # Define un polígono rectangular (área de recorte) con coordenadas en el sistema proyectado
    square = Polygon([
        (origin_x,          origin_y),
        (origin_x + crop_w, origin_y),
        (origin_x + crop_w, origin_y + crop_h),
        (origin_x,          origin_y + crop_h),
    ])

    # Dibuja el mapa completo con la zona de recorte resaltada
    fig0, ax0 = plt.subplots(figsize=(8, 8))
    ox.plot_graph(G_proj, ax=ax0, node_size=0, edge_color='lightgray',
                  edge_linewidth=0.5, show=False)
    gpd.GeoSeries([square], crs=G_proj.graph['crs']).plot(
        ax=ax0, facecolor='none', edgecolor='red', linewidth=2
    )
    ax0.set_title("Mapa de Chiclayo con área de recorte seleccionada")
    plt.tight_layout()
    plt.show()

    # Recorta el grafo original al área definida por el polígono 'square'
    G_sub = ox.truncate.truncate_graph_polygon(G_proj, square)

    # Muestra el número de nodos y aristas del subgrafo recortado
    print(f"Subgrafo recortado: nodos = {len(G_sub.nodes)}, aristas = {len(G_sub.edges)}")

    # Convierte el grafo dirigido a no dirigido para calcular árboles generadores
    G_ud = G_sub.to_undirected()

    # Calcula el Árbol de Expansión Mínima (MST) usando el algoritmo de Kruskal
    mst_k = nx.minimum_spanning_tree(G_ud, weight='length', algorithm='kruskal')

    # Calcula el MST usando el algoritmo de Prim
    mst_p = nx.minimum_spanning_tree(G_ud, weight='length', algorithm='prim')

    # Función auxiliar para imprimir los recorridos del MST
    def print_recorrido(mst, title):
        print(f"\nRecorrido del MST ({title}):")
        for u, v, data in mst.edges(data=True):
            # Intenta obtener el nombre de la calle, si está disponible
            name = data.get('name', 'Sin nombre')
            street = name[0] if isinstance(name, list) else name
            print(f"  Nodo {u} ↔ Nodo {v} : {street}")

    # Imprime el recorrido del árbol generado por Kruskal
    print_recorrido(mst_k, "Kruskal")

    # Imprime el recorrido del árbol generado por Prim
    print_recorrido(mst_p, "Prim")

    # Dibuja diferentes visualizaciones en una sola figura (2x2 subplots)
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))

    # Dibuja el subgrafo recortado
    ox.plot_graph(G_sub, ax=axs[0,1], node_size=10, edge_color='gray',
                  edge_linewidth=0.7, show=False)
    axs[0,1].set_title("Subgrafo recortado")

    # Dibuja el MST de Kruskal sobre el subgrafo
    ax = axs[1,0]
    ox.plot_graph(G_sub, ax=ax, node_size=0, edge_color='gray',
                  edge_linewidth=0.7, edge_alpha=0.2, show=False)
    ox.plot_graph(mst_k, ax=ax, node_size=5, edge_color='red',
                  edge_linewidth=1.2, edge_alpha=1.0, show=False)
    ax.set_title("MST con Kruskal")

    # Dibuja el MST de Prim sobre el subgrafo
    ax = axs[1,1]
    ox.plot_graph(G_sub, ax=ax, node_size=0, edge_color='gray',
                  edge_linewidth=0.7, edge_alpha=0.2, show=False)
    ox.plot_graph(mst_p, ax=ax, node_size=5, edge_color='blue',
                  edge_linewidth=1.2, edge_alpha=1.0, show=False)
    ax.set_title("MST con Prim")

    # Desactiva el subplot superior izquierdo (no se usa)
    axs[0,0].axis('off')

    # Muestra la figura con los cuatro gráficos
    plt.tight_layout()
    plt.show()