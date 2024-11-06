from collections import defaultdict
import random
from datetime import datetime 

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

            if (currPos, i) in macet:
                arrivalTime = currTime + travelTime

                for mulaimacet, akhirmacet, tambahanmacet in macet[(currPos, i)]:
                    tamb = 0.0

                    if currTime <= mulaimacet and arrivalTime >= akhirmacet:
                        tamb = (akhirmacet - mulaimacet) * tambahanmacet
                        print("Small case")
                    elif currTime < mulaimacet <= arrivalTime <= akhirmacet:
                        tamb = (arrivalTime - mulaimacet) * tambahanmacet
                        print("Start first")
                    elif mulaimacet < currTime < akhirmacet <= arrivalTime:
                        tamb = (akhirmacet - currTime) * tambahanmacet
                        print("End first")
                    elif currTime >= mulaimacet and arrivalTime <= akhirmacet:
                        tamb = (arrivalTime - currTime) * tambahanmacet
                        print("Large case")

                    nextCost += tamb
                    print(f"Additional time: {tamb}")

            print(f"Adding {nextCost - currTime} to the cost")

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

    n = int(input("Enter node amount: "))
    nodeCost = randomizeNodeCost(n)
    graph = randomizeGraph(n)

    congestion_amount = int(input("Enter congestion amount: "))
    macet = randomizeCongestion(n, congestion_amount)

    visited = [False] * n
    visited[0] = True
    ans = [float('inf')]
    hasil = [0]

    start = datetime.now()
    optimal_path = tsp(0, 1, nodeCost[0], ans)
    end = datetime.now()

    print(f"Minimum cost: {ans[0]}")
    if optimal_path:
        print("Optimal path: ", end="")
        for i in optimal_path:
            print(i, end=" ")
        print()
    
    # display in miliseconds
    ex_time = (end-start).total_seconds() * (10 ** 3) 
    print(f"Execution time = {ex_time:.03f}ms")

if __name__ == "__main__":
    main()
