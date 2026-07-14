Yes. A graph can be represented as a **matrix**. The two most common matrix representations are:

## 1. Adjacency Matrix (Most Common)

If a graph has **n vertices**, create an **n × n** matrix.

* `matrix[i][j] = 1` if there is an edge from vertex `i` to `j`
* `matrix[i][j] = 0` otherwise

Example graph:

```
A ---- B
|      |
|      |
C ---- D
```

Vertices: A, B, C, D

Adjacency matrix:

|   | A | B | C | D |
| - | - | - | - | - |
| A | 0 | 1 | 1 | 0 |
| B | 1 | 0 | 0 | 1 |
| C | 1 | 0 | 0 | 1 |
| D | 0 | 1 | 1 | 0 |

For a **weighted graph**, store the weight instead of `1`.

Example:

```
A --5-- B
 \2
  \
   C
```

|   | A | B | C |
| - | - | - | - |
| A | 0 | 5 | 2 |
| B | 5 | 0 | 0 |
| C | 2 | 0 | 0 |

---

## 2. Incidence Matrix

Rows represent **vertices** and columns represent **edges**.

Example:

```
A --e1-- B
|
e2
|
C
```

| Vertex | e1 | e2 |
| ------ | -- | -- |
| A      | 1  | 1  |
| B      | 1  | 0  |
| C      | 0  | 1  |

---

## Comparison

| Representation   | Space        | Best For                                         |
| ---------------- | ------------ | ------------------------------------------------ |
| Adjacency Matrix | **O(V²)**    | Dense graphs, fast edge lookup                   |
| Adjacency List   | **O(V + E)** | Sparse graphs (most common in coding interviews) |
| Incidence Matrix | **O(V × E)** | Mathematical graph theory                        |

### Edge lookup complexity

* **Adjacency Matrix:** `O(1)` (just check `matrix[u][v]`)
* **Adjacency List:** `O(degree(u))`
* **Edge List:** `O(E)`

In practice:

* **Competitive programming / LeetCode:** Adjacency List is used most often.
* **Dense graphs or algorithms like Floyd–Warshall:** Adjacency Matrix is preferred.
