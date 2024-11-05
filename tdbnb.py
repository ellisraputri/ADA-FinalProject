import random
from collections import defaultdict
from math import inf

#time dependent tsp branch and bound :D

res = inf
N = 0
path = [-1] * (N + 1)
visited = [False] * N
nodeCost = []
macet = defaultdict(list)

def firstMin(adj, i):
    minimum = inf
    for k in range(N):
        if adj[i][k] < minimum and i != k:
            minimum = adj[i][k]
    return minimum

def secondMin(adj, i):
    first, second = inf, inf
    for k in range(N):
        if i == k:
            continue
        if adj[i][k] <= first:
            second = first
            first = adj[i][k]
        elif adj[i][k] <= second and adj[i][k] != first:
            second = adj[i][k]
    return second

def copyToFinal(curr_path):
    for i in range(N):
        path[i] = curr_path[i]
    path[N] = curr_path[0]

def TSPrec(adj, curr_bound, curr_weight, lvl, curr_path):
    global res
    if lvl == N:
        if adj[curr_path[lvl - 1]][curr_path[0]] != 0:
            curr_res = curr_weight + adj[curr_path[lvl - 1]][curr_path[0]]
            if curr_res < res:
                copyToFinal(curr_path)
                res = curr_res
        return

    for i in range(N):
        if adj[curr_path[lvl - 1]][i] != 0 and not visited[i]:
            temp_bound = curr_bound
            temp_weight = curr_weight
            nextCost = 0.0

            if (curr_path[lvl - 1], i) in macet:
                travelTime = adj[curr_path[lvl - 1]][i]
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

            curr_weight += adj[curr_path[lvl - 1]][i] + nextCost

            if lvl == 1:
                curr_bound -= (firstMin(adj, curr_path[lvl - 1]) + firstMin(adj, i)) / 2
            else:
                curr_bound -= (secondMin(adj, curr_path[lvl - 1]) + firstMin(adj, i)) / 2

            if curr_bound + curr_weight < res:
                curr_path[lvl] = i
                visited[i] = True
                curr_weight += nodeCost[i]
                TSPrec(adj, curr_bound, curr_weight, lvl + 1, curr_path)

            curr_weight = temp_weight
            curr_bound = temp_bound
            visited[i] = False

def TSP(adj):
    curr_path = [-1] * (N + 1)
    curr_bound = 0

    for i in range(N):
        curr_bound += (firstMin(adj, i) + secondMin(adj, i))

    curr_bound = (curr_bound // 2) if curr_bound % 2 == 0 else (curr_bound // 2 + 1)

    visited[0] = True
    curr_path[0] = 0
    TSPrec(adj, curr_bound, 0, 1, curr_path)


def randomizeGraph(n):
    weight_range=(1,100)
    graph = [[0]*(n)] *(n)
    for i in range(n):
        for j in range(i+1, n):
            graph[i][j] = random.randint(*weight_range) 
            graph[j][i] = random.randint(*weight_range)
    return graph

def randomizeNodeCost(n):
    weight_range=(1,100)
    nodecost = [0] *(n)
    for i in range(n):
        nodecost[i] =random.randint(*weight_range)
    return nodecost

def randomizeCongestion(n, congestion_amount):
    macet = defaultdict(list)
    weight_range=(1, n*100)

    for _ in range(congestion_amount):
        i=0
        j=0
        while(i==j):
            i = random.randint(0, n - 1)
            j = random.randint(0, n - 1)

        a = random.randint(*weight_range)  
        b = random.randint(a, weight_range[1])  
        percent = round(random.uniform(0.1, 1.0), 2)  
        macet[(i, j)].append((a, b, percent))
    return macet



def main():
    global res, N, macet, nodeCost, path, visited

    N = int(input("Enter node amount: "))
    nodeCost = randomizeNodeCost(N)
    adj = randomizeGraph(N)

    congestion_amount = int(input("Enter congestion amount: "))
    macet = randomizeCongestion(N, congestion_amount)

    path = [-1] * (N + 1)
    visited = [False] * N


    TSP(adj)

    print(f"Minimum cost: {res}")
    print(f"Path: {'-'.join(map(str, path))}")

if __name__ == "__main__":
    main()
