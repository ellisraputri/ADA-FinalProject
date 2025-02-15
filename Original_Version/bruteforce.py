from collections import defaultdict
import random

n = 0
nodeCost = []
graph = []
macet = defaultdict(list)
hasil = []
visited = []

def tsp(currPos, count, currTime, ans):
    global n, macet, nodeCost, graph, hasil, visited

    if count == n and graph[currPos][0]:
        totalCost = currTime + graph[currPos][0]
        if ans[0] > totalCost:
            ans[0] = totalCost
            print(f"New ans: {ans[0]}\n")
            return hasil[:]  
        return None

    optimal_path = None

    for i in range(n):
        if not visited[i] and graph[currPos][i]:
            visited[i] = True
            hasil.append(i)

            print(f"Current position: {currPos}, Next: {i}")
            print(f"Current time: {currTime}")

            travelTime = graph[currPos][i]
            nextCost = currTime + travelTime + nodeCost[i]

            result = tsp(i, count + 1, nextCost, ans)
            if result:
                optimal_path = result

            visited[i] = False
            hasil.pop()
            print(f"Backtracking to time {currTime}")

    return optimal_path

def randomizeGraph(n):
    weight_range = (1, 100)
    graph = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            graph[i][j] = random.randint(*weight_range)
            graph[j][i] = graph[i][j]
    return graph

def randomizeNodeCost(n):
    weight_range = (1, 100)
    return [random.randint(*weight_range) for _ in range(n)]

def randomizeCongestion(n, congestion_amount):
    macet = defaultdict(list)
    weight_range = (1, n * 100)

    for _ in range(congestion_amount):
        i, j = 0, 0
        while i == j:
            i = random.randint(0, n - 1)
            j = random.randint(0, n - 1)

        a = random.randint(*weight_range)
        b = random.randint(a, weight_range[1])
        percent = round(random.uniform(0.1, 1.0), 2)
        macet[(i, j)].append((a, b, percent))
    return macet


def main():
    global n, nodeCost, graph, macet, hasil, visited

    n = 4
    nodeCost = [0, 15, 10, 20]
    graph = [[0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]]

    # congestion_amount = int(input("Enter congestion amount: "))

    macet = defaultdict(list)
    macet[(1,3)].append((5, 70, 3));  # City 0 to 2 is heavily congested
    macet[(3,1)].append((5, 70, 3));  # City 2 to 3 also congested


    visited = [False] * n
    visited[0] = True
    ans = [float('inf')]
    hasil = [0]
    
    optimal_path = tsp(0, 1, nodeCost[0], ans)

    print(f"Minimum cost: {ans[0]}")
    if optimal_path:
        print("Optimal path: ", end="")
        for i in optimal_path:
            print(i, end=" ")
        print()

if __name__ == "__main__":
    main()
