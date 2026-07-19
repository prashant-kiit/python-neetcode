class DisJointSet():
    def __init__(self, n):
        self.vertice_root_map = list(range(n))
    
    def get_vertice_root_map(self):
        return self.vertice_root_map
    
    def find_root_and_depth(self, vertice):
        root = self.vertice_root_map[vertice]
        depth = 0
        if root != vertice:
            root, depth = self.find_root_and_depth(self.vertice_root_map[vertice])
        depth += 1 
        return root, depth 

    def is_diff_subset(self, vertice_1, vertice_2):
        root_1, depth_1 = self.find_root_and_depth(vertice_1)
        root_2, depth_2 = self.find_root_and_depth(vertice_2)

        if root_1 == root_2:
            return False

        if depth_2 >= depth_1:
            self.vertice_root_map[root_1] = root_2
        else:
            self.vertice_root_map[root_2] = root_1

        return True

def kruskal(n, edges):
    edges.sort(key=lambda x: x[2])
    print(edges)
    disjointset = DisJointSet(n)
    print(disjointset.get_vertice_root_map())
    mst = []
    total_cost = 0

    for vertice_1, vertice_2, cost in edges:
        if disjointset.is_diff_subset(vertice_1, vertice_2):
            mst.append((vertice_1, vertice_2))
            total_cost += cost

    return mst, total_cost

n = 4
edges = [
    (0, 1, 10),
    (0, 2, 6),
    (0, 3, 5),
    (1, 3, 15),
    (2, 3, 4)
]

mst, total_cost = kruskal(n, edges)

print("MST:", mst)
print("Total Cost:", total_cost)