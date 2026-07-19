class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    """
    find(x) finds the parent of vertice x in the subset in which it belongs
    """
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    """
    union(x, y) checks if vertices x and y belong to diff subset or not ie. is_diff_subset(x, y)
    """
    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)

        if rootX == rootY:
            # vertices x and y belong to same subset
            return False

        # vertices x and y do not belong to same subset
        # so, union them to belong to same subset
        # thus assign them a root parent that represents that subset and adjust the rank(depth) of that subset
        if self.rank[rootX] < self.rank[rootY]:
            self.parent[rootX] = rootY
        elif self.rank[rootX] > self.rank[rootY]:
            self.parent[rootY] = rootX
        else:
            self.parent[rootY] = rootX
            self.rank[rootX] += 1

        return True


def kruskal(n, edges):
    """
    n: number of vertices (0 to n-1)
    edges: [(u, v, weight), ...]
    """
    edges.sort(key=lambda x: x[2])
    ds = DisjointSet(n)
    mst = []
    total_cost = 0
    print(edges)

    # n = 4
    # edges = [(2, 3, 4), (0, 3, 5), (0, 2, 6), (0, 1, 10), (1, 3, 15)]
    # ds_parent = [2, 2, 2, 2]
    # ds_rank = [0, 0, 1, 0]
    # mst = [(2, 3, 4), (0, 3, 5), (0, 1, 10)]
    # total_cost = 19

    for u, v, w in edges:
        if ds.union(u, v):
            mst.append((u, v, w))
            total_cost += w

    return mst, total_cost


# Example
n = 4
edges = [
    (0, 1, 10),
    (0, 2, 6),
    (0, 3, 5),
    (1, 3, 15),
    (2, 3, 4)
]

mst, cost = kruskal(n, edges)

print("MST:", mst)
print("Total Cost:", cost)