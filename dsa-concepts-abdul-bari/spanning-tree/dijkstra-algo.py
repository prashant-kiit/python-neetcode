import heapq


def dijkstra(graph, start):
    distances = {node: float("inf") for node in graph}
    distances[start] = 0

    pq = [(0, start)]  # (distance, node)

    while pq:
        current_dist, current = heapq.heappop(pq)

        if current_dist > distances[current]:
            continue

        for neighbor, weight in graph[current]:
            new_dist = current_dist + weight

            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))

    return distances

graph = {
    1: [(2, 1), (4, 10)],
    2: [(1, 1), (3, 11)],
    3: [(2, 11), (4, 1)],
    4: [(1, 10), (3, 1)]
}

print(dijkstra(graph, 1))