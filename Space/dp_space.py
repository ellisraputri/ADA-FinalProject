import tracemalloc as tm
import sys
from collections import defaultdict
import random

n = 0
result = sys.float_info.max
mask = 0
graph = []
nodeCost = []
macet = defaultdict(list)


def tsp(current, dp, link, currTime):
    global result, mask, n
    
    if mask == (1 << n) - 1:
        return graph[current][0]  
    
    if dp[mask][current] != -1:
        return dp[mask][current]
    
    local_result = sys.float_info.max
    for i in range(n):
        val = 1 << i
        if mask & val:
            continue

        # print(f"current {current}, i {i}")
        travelTime = graph[current][i]
        
        prev_mask = mask
        mask |= val
        sub = tsp(i, dp, link, currTime + travelTime + nodeCost[i]) + travelTime + nodeCost[i]
        mask = prev_mask

        arrivalTime = currTime + travelTime
        # print(f"current {current}, i {i} = {sub}")

        if (current, i) in macet:
            for mulaimacet, akhirmacet, tambahanmacet in macet[(current, i)]:
                tamb = 0.0
                if currTime <= mulaimacet and arrivalTime >= akhirmacet:
                    tamb = (akhirmacet - mulaimacet) * tambahanmacet
                elif currTime < mulaimacet <= arrivalTime and akhirmacet >= arrivalTime:
                    tamb = (arrivalTime - mulaimacet) * tambahanmacet
                elif mulaimacet < currTime and akhirmacet > currTime and akhirmacet <= arrivalTime:
                    tamb = (akhirmacet - currTime) * tambahanmacet
                elif currTime >= mulaimacet and arrivalTime <= akhirmacet:
                    tamb = (arrivalTime - currTime) * tambahanmacet

                sub += tamb
                # print("kena macet")

        # print(f"endcost = {sub}")

        if sub < local_result:
            local_result = sub
            link[mask][current] = i  

    dp[mask][current] = local_result
    # print(f"\nresult {local_result}")
    return local_result


def getpath(link):
    global mask
    current = 0
    mask = 0
    path = []
    for _ in range(len(link[0])):
        path.append(current)
        mask |= 1 << current
        current = link[mask][current]
    return path


def randomizeGraph(n):
    weight_range = (1, 100)
    graph = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            graph[i][j] = random.randint(*weight_range)
            graph[j][i] = random.randint(*weight_range)
    return graph


def randomizeNodeCost(n):
    weight_range = (1, 100)
    nodecost = [0] * n
    for i in range(n):
        nodecost[i] = random.randint(*weight_range)
    return nodecost


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

def analyze_this_code(dp, link):
    result = tsp(0, dp, link, 0)

    # take a snapshot
    snapshot = tm.take_snapshot()
    for stat in snapshot.statistics("lineno"):
        print(stat)

    # displaying the memory in bytes (current and peak)
    print(tm.get_traced_memory())
    return result

def main():
    global n, result, graph, nodeCost, macet, mask
    
    n = int(input("Enter node amount: "))
    nodeCost = randomizeNodeCost(n)
    graph = randomizeGraph(n)

    congestion_amount = int(input("Enter congestion amount: "))
    macet = randomizeCongestion(n, congestion_amount)

    dp = [[-1] * n for _ in range(1 << n)]
    link = [[0] * n for _ in range(1 << n)]
    mask = 1  

    tm.start()
    result = analyze_this_code(dp, link)
    tm.stop()
    
    # print("\nDP Table:")
    # for row in dp:
    #     print(row)
    
    path = getpath(link)
    print(f"Minimum cost: {result}")
    print("Path:", " ".join(map(str, path)))


if __name__ == "__main__":
    main()
