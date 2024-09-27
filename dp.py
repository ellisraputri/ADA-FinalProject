import sys
from collections import defaultdict

graph = []
nodeCost = []
macet = defaultdict(list)


def tsp(n, current, mask, dp, link, currTime):
    if mask == (1 << n) - 1:
        return graph[current][0]  
    
    if dp[mask][current] != -1:
        return dp[mask][current]
    
    result = sys.float_info.max
    for i in range(n):
        val = 1 << i
        if mask & val:
            continue

        print(f"current {current}, i {i}")
        travelTime = graph[current][i]
        sub = tsp(n, i, mask | val, dp, link, currTime + travelTime + nodeCost[i]) + travelTime + nodeCost[i]

        arrivalTime = currTime + travelTime
        print(f"current {current}, i {i} = {sub}")


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

        print(f"endcost = {sub}")

        if sub < result:
            result = sub
            link[mask][current] = i  

    dp[mask][current] = result
    print(f"\nresult {result}")
    return result


def getpath(link):
    current = 0
    mask = 0
    path = []
    for _ in range(len(link[0])):
        path.append(current)
        mask |= 1 << current
        current = link[mask][current]
    return path


def main():
    global nodeCost, graph
    n = 4
    nodeCost = [0,5,7,10]
    graph = [
        [0, 8, 12, 15],
    [8, 0, 10, 20],
    [12, 10, 0, 9],
    [15, 20, 9, 0]
    ]
    macet[(0, 1)].append((2, 12, 1.0))
    macet[(1, 3)].append((5, 15, 0.7))


    dp = [[-1] * n for _ in range(1 << n)]
    link = [[0] * n for _ in range(1 << n)]

    res = tsp(n, 0, 1, dp, link, 0)
    print("\nDP Table:")
    for row in dp:
        print(row)
    
    path = getpath(link)
    print(f"result {res}")
    print("Path:", " ".join(map(str, path)))

if __name__ == "__main__":
    main()
