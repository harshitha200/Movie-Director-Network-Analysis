from collections import deque
from heapq import heappush, heappop

def bfs(graph, start_node, search_node=None):
    if search_node and start_node == search_node:
        return 1
    P, visited = dict(), set()
    P[start_node] = -1
    queue = deque([start_node])
    path = list()
    while queue:
        node = queue.popleft()
        path.append(node)
        if node == search_node: 
            return 1
        for other in graph[node]:
            if not other in visited:
                queue.append(other)
                visited.add(other)
                P[other] = node
    if search_node is not None:
        return 0
    return path

def dfs(graph, start_node, visited=None, path=None, search_node=None):
    if path is None:
        path = list()
    if visited is None:
        visited = dict()
    if start_node in visited and visited[start_node]:
        return
    path = [start_node]
    visited[start_node] = True
    if start_node == search_node:
        return 1
    
    for x in graph[start_node]:
        if x in visited and visited[x]:
            continue
        res = dfs(graph, x, visited, path, search_node)
        if search_node is None:
            path.extend(res)
        elif res == 1:
                return 1
    
    if search_node is not None:
        return 0
    return path

def dijkstra(graph, start_node, end_node):
    if start_node == end_node:
        return [[start_node], 0, 0]
    myheap = [(0, start_node)]
    P, co = dict(), dict()
    visited = dict()
    for x in graph:
        visited[x] = False
    P[start_node], co[start_node] = -1, 0
    while myheap:
        truffle = heappop(myheap)
        id = truffle[1]
        cox = truffle[0]
        if visited[id]:
            continue
        for x in graph[id]:
            if visited[x]:
                continue
            if x not in co:
                co[x] = 10**9
            if cox + graph[id][x] < co[x]:
                co[x] = cox + graph[id][x]
                P[x] = id
                heappush(myheap, (co[x], x))
        visited[id] = True
    
    if not visited[end_node]:
        return 0
    path = []
    prev = end_node
    while prev != -1:
        path.append(prev)
        prev = P[prev]
    path = path[::-1]
    return [path, co[end_node], len(path)-1]

def kosaraju(graph):
    Gr = dict()
    for k, v in graph.items():
        for sk, sv in v.items():
            if sk not in Gr:
                Gr[sk] = dict()
            Gr[sk][k] = sv
    
    vis1, vis2 = dict(), dict()
    visiting = list()
    def df1(x, G):
        vis1[x] = True
        for y in G[x]:
            if not vis1[y]:
                df1(y, G)
        visiting.append(x)
    
    def df2(x, G, c):
        vis2[x] = True
        c.append(x)
        for y in G[x]:
            if not vis2[y]:
                df2(y, G, c)
           
           
    for x in graph:
        vis1[x] = False
        vis2[x] = False     
    cx = []
    for x in graph:
        if not vis1[x]:
            df1(x, graph)
    visiting = visiting[::-1]
    for x in visiting:
        if not vis2[x]:
            f = list()
            df2(x, Gr, f)
            cx.append(f)
    return cx
