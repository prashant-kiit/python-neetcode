import heapq


def prim_mst(graph, start=0):
    visited = {start}
    mst = []
    min_heap = []

    # Push all edges from the starting vertex
    for neighbor, weight in graph[start]:
        heapq.heappush(min_heap, (weight, start, neighbor))

    # Continue until MST has V-1 edges
    while min_heap and len(mst) < len(graph) - 1:
        weight, source, destination = heapq.heappop(min_heap)

        # Skip if destination is already part of the MST
        if destination in visited:
            continue

        # Add edge to MST
        mst.append((source, destination, weight))
        visited.add(destination)

        # Push all outgoing edges from the newly visited vertex
        for neighbor, edge_weight in graph[destination]:
            if neighbor not in visited:
                heapq.heappush(
                    min_heap,
                    (edge_weight, destination, neighbor)
                )

    return mst


# Example Graph (Adjacency List)
graph = {
    0: [(1, 4), (2, 3)],
    1: [(0, 4), (2, 1), (3, 2)],
    2: [(0, 3), (1, 1), (3, 4)],
    3: [(1, 2), (2, 4)]
}

mst = prim_mst(graph)

print("Edges in MST:")
total_weight = 0
for source, destination, weight in mst:
    print(f"{source} --({weight})--> {destination}")
    total_weight += weight

print(f"\nTotal Weight = {total_weight}")