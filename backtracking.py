import sys
from collections import defaultdict

nodeCost = []
graph = []
hasil = []
hasilakhir = []
macet = defaultdict(list)

def tsp(visited, currPos, n, count, currTime, ans):
    global hasil, hasilakhir

    if count == n and graph[currPos][0]:
        totalCost = currTime + graph[currPos][0]
        if ans[0] > totalCost:
            ans[0] = totalCost
            print(f"ans baru: {ans[0]}")
            print()
            hasilakhir = hasil[:]
        return

    for i in range(n):
        if not visited[i] and graph[currPos][i]:
            visited[i] = True
            hasil.append(i)

            print(f"curpos dan i: {currPos} {i}")
            print(f"waktu skrg: {currTime}")

            travelTime = graph[currPos][i]
            nextCost = currTime + travelTime + nodeCost[i]

            if (currPos, i) in macet:
                arrivalTime = currTime + travelTime

                for mulaimacet, akhirmacet, tambahanmacet in macet[(currPos, i)]:
                    tamb = 0.0

                    # kasus kecil (s mulai akhir e)
                    if currTime <= mulaimacet and arrivalTime >= akhirmacet:
                        tamb = (akhirmacet - mulaimacet) * tambahanmacet
                        print("kasus kecil")
                    # kasus start duluan (s mulai e akhir)
                    elif currTime < mulaimacet and mulaimacet <= arrivalTime and akhirmacet >= arrivalTime:
                        tamb = (arrivalTime - mulaimacet) * tambahanmacet
                        print("kasus start dulu")
                    # kasus akhir duluan (mulai s akhir e)
                    elif mulaimacet < currTime and akhirmacet > currTime and akhirmacet <= arrivalTime:
                        tamb = (akhirmacet - currTime) * tambahanmacet
                        print("kasus end dulu")
                    # kasus gede (mulai s e akhir)
                    elif currTime >= mulaimacet and arrivalTime <= akhirmacet:
                        tamb = (arrivalTime - currTime) * tambahanmacet
                        print("kasus gede")

                    nextCost += tamb
                    print(f"tambahan = {tamb}")

            print(f"masukkin {nextCost - currTime}")

            tsp(visited, i, n, count + 1, nextCost, ans)

            visited[i] = False
            hasil.pop()
            print(f"keluarin {currTime}")

def main():
    global nodeCost, graph, macet, hasil

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

    visited = [False] * n
    visited[0] = True
    ans = [float('inf')]
    hasil.append(0)

    tsp(visited, 0, n, 1, nodeCost[0], ans)

    print(f"Minimum cost: {ans[0]}")

    print("Optimal path: ", end="")
    for i in hasilakhir:
        print(i, end=" ")
    print()

if __name__ == "__main__":
    main()
