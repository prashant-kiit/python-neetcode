def greedy_solution(arr):
    optimal_solution = []
    for a in arr:
        x = select_such_that_x_is_optimal(arr)
        if is_x_solution(x) and is_x_feasible_solution(x):
            optimal_solution.append(x)
    return optimal_solution
