def kruskal(nodes, edges):
    sorted_edges = sorted(edges, key=lambda x: x[2])
    parent = {n: n for n in nodes}
    rank = {n: 0 for n in nodes}

    def find(u):
        if parent[u] != u:
            parent[u] = find(parent[u])
        return parent[u]

    def union(u, v):
        ru, rv = find(u), find(v)
        if ru == rv:
            return False
        if rank[ru] < rank[rv]:
            parent[ru] = rv
        elif rank[ru] > rank[rv]:
            parent[rv] = ru
        else:
            parent[rv] = ru
            rank[ru] += 1
        return True

    mst = []
    total_weight = 0.0
    for u, v, w in sorted_edges:
        if union(u, v):
            mst.append((u, v, w))
            total_weight += w
    return mst, total_weight


def prim(nodes, adj):
    if not nodes:
        return [], 0.0
    start = nodes[0]
    visited = {start}
    heap = []
    for v, w in adj[start]:
        heapq.heappush(heap, (w, start, v))
    mst = []
    total_weight = 0.0
    while heap and len(visited) < len(nodes):
        w, u, v = heapq.heappop(heap)
        if v in visited:
            continue
        visited.add(v)
        mst.append((u, v, w))
        total_weight += w
        for nbr, w2 in adj[v]:
            if nbr not in visited:
                heapq.heappush(heap, (w2, v, nbr))
    return mst, total_weight
