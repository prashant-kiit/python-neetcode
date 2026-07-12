# The * operator copies references, not the objects themselves.
#         ┌──────► [1]
# lst ────┤
#         ├──────► [1]
#         └──────► [1]

lst = [[0]] * 3
lst[0][0] = 1
print(lst[0] is lst[1])  # True
print(lst[1] is lst[2])  # True
print(lst)   # [[1], [1], [1]]

# Use a list comprehension to create a new inner list each time:
# lst ───► [0]   (independent)
#       ─► [0]   (independent)
#       ─► [0]   (independent)
lst = [[0] for _ in range(3)]
lst[0][0] = 1
print(lst[0] is lst[1])  # False
print(lst)  # [[1], [0], [0]]

