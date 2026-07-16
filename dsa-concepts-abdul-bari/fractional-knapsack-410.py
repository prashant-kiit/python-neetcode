# Example
profit = [60, 100, 120]
weights = [10, 20, 30]
capacity = 50

def max_profit(profits, weights, capacity):
    items = [(profits[i]/weights[i], profits[i], weights[i]) for i in range(len(profits))]

    items.sort(reverse=True)

    max_profit_value = 0.0

    for ratio, profit, weight in items:
        if capacity >= weight:
            max_profit_value += profit
            capacity -= weight
        else:
            max_profit_value += ratio * capacity
            break

    return max_profit_value

print(max_profit(profit, weights, capacity))