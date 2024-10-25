from collections import defaultdict

def tsp(visited, currPos, n, count, currTime, ans, hasil, macet, nodeCost, graph):
    if count == n and graph[currPos][0]:
        totalCost = currTime + graph[currPos][0]
        if ans[0] > totalCost:
            ans[0] = totalCost
            print(f"New ans: {ans[0]}\n")
            return hasil[:]  # Return the current optimal path
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

            # Check if there's a traffic delay on this route
            if (currPos, i) in macet:
                arrivalTime = currTime + travelTime

                for mulaimacet, akhirmacet, tambahanmacet in macet[(currPos, i)]:
                    tamb = 0.0

                    # Handle different traffic scenarios
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

            # Recur with the updated state
            result = tsp(visited, i, n, count + 1, nextCost, ans, hasil, macet, nodeCost, graph)
            if result:
                optimal_path = result

            visited[i] = False
            hasil.pop()
            print(f"Backtracking to time {currTime}")

    return optimal_path

def main():
    n = 4
    nodeCost = [0, 15, 10, 20]
    graph = [
        [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
    ]

    # Traffic conditions (start, end, additional cost per time unit)
    macet = defaultdict(list)
    macet[(0, 2)].append((5,30,1))
    macet[(2, 3)].append((10,50,0.8))

    visited = [False] * n
    visited[0] = True
    ans = [float('inf')]
    hasil = [0]

    # Run the TSP and get the optimal path
    optimal_path = tsp(visited, 0, n, 1, nodeCost[0], ans, hasil, macet, nodeCost, graph)

    print(f"Minimum cost: {ans[0]}")

    if optimal_path:
        print("Optimal path: ", end="")
        for i in optimal_path:
            print(i, end=" ")
        print()

if __name__ == "__main__":
    main()
