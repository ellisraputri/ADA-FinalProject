import random
from collections import defaultdict
from math import inf
from datetime import datetime
from time import perf_counter

#time dependent tsp branch and bound

res = inf
N = 0
path = [-1] * (N + 1)
visited = [False] * N
nodeCost = []
macet = defaultdict(list)
graph = []

def firstMin(i):
    minimum = inf
    for k in range(N):
        if graph[i][k] < minimum and i != k:
            minimum = graph[i][k]
    return minimum

def secondMin(i):
    first, second = inf, inf
    for k in range(N):
        if i == k:
            continue
        if graph[i][k] <= first:
            second = first
            first = graph[i][k]
        elif graph[i][k] <= second and graph[i][k] != first:
            second = graph[i][k]
    return second

def copyToFinal(curr_path):
    for i in range(N):
        path[i] = curr_path[i]
    path[N] = curr_path[0]

def TSPrec(curr_bound, curr_weight, lvl, curr_path):
    global res
    if lvl == N:
        if graph[curr_path[lvl - 1]][curr_path[0]] != 0:
            curr_res = curr_weight + graph[curr_path[lvl - 1]][curr_path[0]]
            if curr_res < res:
                copyToFinal(curr_path)
                res = curr_res
        return

    for i in range(N):
        if graph[curr_path[lvl - 1]][i] != 0 and not visited[i]:
            temp_bound = curr_bound
            temp_weight = curr_weight
            nextCost = 0.0

            if (curr_path[lvl - 1], i) in macet:
                travelTime = graph[curr_path[lvl - 1]][i]
                end_time = curr_weight + travelTime

                for mulaimacet, akhirmacet, tambahanmacet in macet[(curr_path[lvl - 1], i)]:
                    tamb = 0.0
                    if curr_weight <= mulaimacet and end_time >= akhirmacet:
                        tamb = (akhirmacet - mulaimacet) * tambahanmacet
                    elif curr_weight < mulaimacet and mulaimacet <= end_time and akhirmacet >= end_time:
                        tamb = (end_time - mulaimacet) * tambahanmacet
                    elif mulaimacet < curr_weight and akhirmacet > curr_weight and akhirmacet <= end_time:
                        tamb = (akhirmacet - curr_weight) * tambahanmacet
                    elif curr_weight >= mulaimacet and end_time <= akhirmacet:
                        tamb = (end_time - curr_weight) * tambahanmacet

                    nextCost += tamb

            curr_weight += graph[curr_path[lvl - 1]][i] + nextCost

            if lvl == 1:
                curr_bound -= (firstMin(curr_path[lvl - 1]) + firstMin(i)) / 2
            else:
                curr_bound -= (secondMin(curr_path[lvl - 1]) + firstMin(i)) / 2

            if curr_bound + curr_weight < res:
                curr_path[lvl] = i
                visited[i] = True
                curr_weight += nodeCost[i]
                TSPrec(curr_bound, curr_weight, lvl + 1, curr_path)

            curr_weight = temp_weight
            curr_bound = temp_bound
            visited[i] = False

def TSP():
    curr_path = [-1] * (N + 1)
    curr_bound = 0

    for i in range(N):
        curr_bound += (firstMin(i) + secondMin(i))

    curr_bound = (curr_bound // 2) if curr_bound % 2 == 0 else (curr_bound // 2 + 1)

    visited[0] = True
    curr_path[0] = 0
    TSPrec(curr_bound, 0, 1, curr_path)

def randomizeGraph():
    global graph
    weight_range=(1,100)
    graph = [[0]*(N)] *(N)
    for i in range(N):
        for j in range(i+1, N):
            graph[i][j] = random.randint(*weight_range) 
            graph[j][i] = random.randint(*weight_range)

def randomizeNodeCost():
    weight_range=(1,100)
    nodecost = [0] *(N)
    for i in range(N):
        nodecost[i] =random.randint(*weight_range)
    return nodecost

def randomizeCongestion(congestion_amount):
    macet = defaultdict(list)
    weight_range=(1, N*100)

    for _ in range(congestion_amount):
        i=0
        j=0
        while(i==j):
            i = random.randint(0, N - 1)
            j = random.randint(0, N - 1)

        a = random.randint(*weight_range)  
        b = random.randint(a, weight_range[1])  
        percent = round(random.uniform(0.1, 1.0), 2)  
        macet[(i, j)].append((a, b, percent))
    return macet



def main():
    global res, N, macet, nodeCost, path, visited, graph

    N = int(input("Enter node amount: "))
    nodeCost = randomizeNodeCost()
    randomizeGraph()

    congestion_amount = int(input("Enter congestion amount: "))
    macet = randomizeCongestion(congestion_amount)

    path = [-1] * (N + 1)
    visited = [False] * N

    start = perf_counter()
    TSP() 
    end = perf_counter()

    print(f"Minimum cost: {res}")
    print(f"Path: {'-'.join(map(str, path))}")

    ex_time = (end - start) * 1000  
    print(f"Execution time = {ex_time:.03f} ms")

    
if __name__ == "__main__":
    main()
