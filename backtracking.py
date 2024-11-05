from collections import defaultdict
import random 

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
    n = int(input("Enter node amount: "))
    nodeCost = randomizeNodeCost(n)
    graph = randomizeGraph(n)

    congestion_amount = int(input("Enter congestion amount: "))
    macet = randomizeCongestion(n, congestion_amount)

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
