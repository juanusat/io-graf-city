import heapq  # Importa el módulo heapq para utilizar una cola de prioridad (montículo mínimo)
def kruskal(nodes, edges):  
    # Ordena las aristas por peso ascendente
    sorted_edges = sorted(edges, key=lambda x: x[2])  
    
    # Inicializa el padre de cada nodo como él mismo (estructura disjoint set - unión por conjuntos)
    parent = {n: n for n in nodes}  
    
    # Inicializa el rango (profundidad del árbol de cada conjunto) en 0
    rank = {n: 0 for n in nodes}  

    # Función para encontrar la raíz del conjunto al que pertenece el nodo 'u'
    def find(u):  
        # Si el nodo no es su propio padre, busca recursivamente
        if parent[u] != u:  
            parent[u] = find(parent[u])  # Compresión de caminos
        return parent[u]  # Devuelve el padre raíz

    # Función para unir los conjuntos de 'u' y 'v' si no están ya unidos
    def union(u, v):  
        ru, rv = find(u), find(v)  # Encuentra los representantes de cada conjunto
        if ru == rv:  # Si ya están en el mismo conjunto, no se pueden unir (evitar ciclo)
            return False
        # Unión por rango: el árbol más bajo se une al más alto
        if rank[ru] < rank[rv]:  
            parent[ru] = rv  
        elif rank[ru] > rank[rv]:  
            parent[rv] = ru  
        else:  
            parent[rv] = ru  
            rank[ru] += 1  # Aumenta el rango si ambos tenían el mismo
        return True  # Se realizó la unión correctamente

    mst = []  # Lista para almacenar las aristas del MST
    total_weight = 0.0  # Suma total de pesos de las aristas en el MST

    # Itera sobre las aristas ordenadas por peso
    for u, v, w in sorted_edges:  
        if union(u, v):  # Si unir u y v no forma un ciclo
            mst.append((u, v, w))  # Añade la arista al MST
            total_weight += w  # Suma su peso al total

    return mst, total_weight  # Devuelve el MST y su peso total
def prim(nodes, adj):  
    # Si no hay nodos, devuelve MST vacío
    if not nodes:  
        return [], 0.0  

    start = nodes[0]  # Elige un nodo de inicio arbitrario
    visited = {start}  # Conjunto de nodos visitados (inicialmente solo el nodo de inicio)

    heap = []  # Cola de prioridad para seleccionar la arista de menor peso
    for v, w in adj[start]:  
        heapq.heappush(heap, (w, start, v))  # Añade todas las aristas del nodo inicial al heap

    mst = []  # Lista para almacenar las aristas del MST
    total_weight = 0.0  # Peso total del MST

    # Mientras haya aristas y aún no se hayan visitado todos los nodos
    while heap and len(visited) < len(nodes):  
        w, u, v = heapq.heappop(heap)  # Extrae la arista de menor peso del heap

        if v in visited:  # Si el nodo destino ya fue visitado, se descarta
            continue  

        visited.add(v)  # Marca el nodo como visitado
        mst.append((u, v, w))  # Agrega la arista al MST
        total_weight += w  # Suma su peso al total

        # Agrega las aristas del nuevo nodo a la cola, si el destino no ha sido visitado
        for nbr, w2 in adj[v]:  
            if nbr not in visited:  
                heapq.heappush(heap, (w2, v, nbr))  

    return mst, total_weight  # Devuelve el MST y el peso total
