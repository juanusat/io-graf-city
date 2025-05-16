# Kruskal

1. Ordenar todas las aristas por peso ascendente.

2. Inicializar un bosque donde cada vértice es su propio componente.

3. Recorrer aristas ordenadas: si al añadir la arista sus extremos están en componentes distintos, unirlos (y añadirla al MST).

4. Repetir hasta tener V−1 aristas.

# Prim

1. Elegir un vértice inicial, marcarlo como “visitado”.

2. Insertar en el heap todas las aristas que salen de él.

3. Mientras el heap no esté vacío y el árbol tenga menos de V−1 aristas:

    - Extraer la arista de menor peso.

    - Si conecta a un vértice no visitado, marcarlo y añadir al MST, y agregar al heap las aristas que salen de éste hacia no visitados.

