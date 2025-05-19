1. Algoritmo de Dijkstra (Segundo script)

Objetivo: Encontrar el camino de costo mínimo (menor suma de pesos) desde un nodo origen a todos los demás nodos en un grafo con pesos positivos.

Lógica utilizada:

Se construye un grafo aleatorio no dirigido, donde cada arista tiene un peso aleatorio.

Se implementa una versión clásica del algoritmo de Dijkstra:

Se mantiene una distancia mínima estimada para cada nodo, inicializada como infinito (∞), excepto el nodo de origen (que vale 0).

Se utiliza una cola de prioridad (heap) para seleccionar el nodo con menor distancia no procesado.

Al visitar un nodo, se relajan las aristas hacia sus vecinos: si el nuevo camino es más corto, se actualiza la distancia y el predecesor.


Luego, se reconstruye el camino desde el destino hasta el origen usando los predecesores.

Finalmente, se visualiza el grafo y se imprime el camino mínimo y su peso total.



---

2. Edmonds-Karp (Primer script)

Objetivo: Encontrar el flujo máximo desde una fuente a un sumidero en un grafo dirigido con capacidades en sus aristas.

Lógica utilizada:

Se lee el grafo desde un archivo que contiene:

La fuente y el sumidero.

Aristas con capacidad y flujo usado.


El algoritmo de Edmonds-Karp es una implementación específica de Ford-Fulkerson que utiliza BFS (búsqueda en anchura) para encontrar caminos aumentantes.

En cada iteración:

Se busca un camino desde la fuente al sumidero en el grafo residual (capacidad restante).

Se identifica el cuello de botella (capacidad mínima en el camino).

Se actualiza el grafo residual (resta flujo hacia adelante, suma hacia atrás).

Se acumula el flujo añadido al total.


El proceso se repite hasta que ya no se encuentra un camino aumentante.


Ventaja: Siempre termina en tiempo polinomial. Es más predecible y seguro para grafos grandes.


---

3. Ford-Fulkerson (DFS recursivo) (Primer script)

Objetivo: Igual que Edmonds-Karp: hallar el flujo máximo entre dos nodos.

Lógica utilizada:

También trabaja sobre un grafo dirigido con capacidades.

A diferencia de Edmonds-Karp, utiliza una búsqueda en profundidad (DFS) para encontrar caminos aumentantes.

En cada iteración:

Se ejecuta una DFS recursiva que explora caminos mientras haya capacidad disponible.

Cuando se llega al sumidero, se retrocede actualizando capacidades residuales.

Se repite mientras se puedan encontrar caminos.


Acumula el flujo en cada iteración hasta que no se puede avanzar más.


Ventaja: Puede ser más rápido en práctica para ciertos grafos pequeños.

Desventaja: Puede entrar en bucle infinito o no terminar si los flujos son reales (no enteros) y no se controla el redondeo. Por eso, su versión con BFS (Edmonds-Karp) es preferida para robustez.


---

Comparación rápida:

Algoritmo	Tipo de problema	Estrategia de búsqueda	Garantiza tiempo polinomial

Dijkstra	Camino más corto (pesos)	Greedy (cola de prioridad)	Sí
Ford-Fulkerson (DFS)	Flujo máximo (capacidades)	DFS	No (puede ser exponencial)
Edmonds-Karp	Flujo máximo (capacidades)	BFS	Sí (O(VE²))
