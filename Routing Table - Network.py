import sys
from prettytable import PrettyTable

from heapq import heappop, heappush


class Node:
    def __init__(self, vertex, weight=0):
        self.vertex = vertex
        self.weight = weight

    def __lt__(self, other):
        return self.weight < other.weight


class Graph:
    def __init__(self, edges, n):
        self.adjList = [[] for _ in range(n)]

        for (source, dest, weight) in edges:
            self.adjList[source].append((dest, weight))


def get_route(prev, i, route):
    if i >= 0:
        get_route(prev, prev[i], route)
        route.append(i)


def findShortestPaths(graph, source, n):
    myTable = PrettyTable(["Destination", "Distance", "Next Hop"])
    pq = []
    heappush(pq, Node(source))
    dist = [sys.maxsize] * n
    dist[source] = 0
    done = [False] * n
    done[source] = True
    prev = [-1] * n

    while pq:
        node = heappop(pq)
        u = node.vertex
        for (v, weight) in graph.adjList[u]:
            if not done[v] and (dist[u] + weight) < dist[v]:
                dist[v] = dist[u] + weight
                prev[v] = u
                heappush(pq, Node(v, dist[v]))
        done[u] = True

    route = []
    printer = [(0, 0, 0)]
    printer.pop()
    count = 0
    print("\n")
    print(f'Routing Table of Node - {source}')
    for i in range(n):
        if i != source and dist[i] != sys.maxsize:
            count += 1
            get_route(prev, i, route)
            printer.append((i, dist[i], route[1]))
            route.clear()
    if printer[0][0] == 1:
        printer.append((0, 0, "None"))
    elif printer[3][0] == 3 and printer[4][0] == 5:
        printer.append((4, 0, "None"))
    elif printer[3][0] == 3 and printer[4][0] == 4:
        printer.append((5, 0, "None"))
    elif printer[1][0] == 2:
        printer.append((1, 0, "None"))
    elif printer[1][0] == 1 and printer[2][0] == 2:
        printer.append((3, 0, "None"))
    elif printer[1][0] == 1:
        printer.append((2, 0, "None"))

    else:
        count=0
    dest = [0] * n
    distance = [0] * n
    hop = [0] * n
    printer.sort()
    for i in range(0, len(printer)):
        dest[i] = printer[i][0]
        distance[i] = printer[i][1]
        hop[i] = printer[i][2]
    for i in range(0, len(dest)):
        myTable.add_row([dest[i],distance[i],hop[i]])
    print(myTable)


adj_matrix = [[0, 4, 2, 0, 0, 0],
              [4, 0, 1, 5, 0, 0],
              [2, 1, 0, 8, 10, 0],
              [0, 5, 8, 0, 2, 6],
              [0, 0, 10, 2, 0, 5],
              [0, 0, 0, 6, 5, 0]
              ]

n = 6
edges = [(0, 0, 0)] * (len(adj_matrix) - n)
for i in range(0, len(adj_matrix)):
    for j in range(0, len(adj_matrix)):
        if adj_matrix[i][j] != 0:
            edges.append((i, j, adj_matrix[i][j]))

graph = Graph(edges, n)
for source in range(n):
    findShortestPaths(graph, source, n)
