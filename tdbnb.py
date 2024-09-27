import sys
from collections import defaultdict
from math import inf

#time dependent tsp branch and bound :D

res = inf
N = 4
path = [-1] * (N + 1)
visited = [False] * N
nodeCost = [0, 15, 10, 20]
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

def main():
    global res

    adj = [[0, 10, 15, 20],
[10, 0, 35, 25],
[15, 35, 0, 30],
[20, 25, 30, 0]]

    # macet[(0,2)].append((5, 30, 1.0))
    # macet[(2,3)].append((10, 50, 0.8))
    # macet[(2,3)].append((5, 20, 0.5))
    # macet[(3,4)].append((12, 30, 0.6))

    TSP(adj)

    print(f"Minimum cost: {res}")
    print(f"Path: {'-'.join(map(str, path))}")

if __name__ == "__main__":
    main()
