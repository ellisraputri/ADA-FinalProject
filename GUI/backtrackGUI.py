import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

speed=0.5

def generate_complete_graph(num_nodes, graphInput=None, nodeCostInput=None, weight_range=(1, 100)):
    G = nx.complete_graph(num_nodes)

    if(graphInput==None):
        for u, v in G.edges():
            G.edges[u, v]['weight'] = random.randint(*weight_range) 
    else:
        for u, v in G.edges():
            G.edges[u, v]['weight'] =graphInput[u][v]
    
    if(nodeCostInput==None):
        for u in G.nodes():
            if u == 0:
                G.nodes[u]['nodeCost'] = 0
            elif 'nodeCost' not in G.nodes[u]:  
                G.nodes[u]['nodeCost'] = random.randint(*weight_range)
 
    else:
        for u in G.nodes():
            G.nodes[u]['nodeCost'] = nodeCostInput[u]

    return G


def generate_congestion(num_nodes, congestion_input=None):
    macet = defaultdict(list)
    weight_range=(1, num_nodes*100)

    if not congestion_input: 
        num_pairs = random.randint(1, num_nodes * (num_nodes - 1))  

        for _ in range(num_pairs):
            i = random.randint(0, num_nodes - 1)
            j = random.randint(0, num_nodes - 1)

            if i != j:  
                a = random.randint(*weight_range)  
                b = random.randint(a, weight_range[1])  
                percent = round(random.uniform(0.1, 1.0), 2)  

                macet[(i, j)].append((a, b, percent))
    else:
        macet = congestion_input  

    return macet



def plot_graph_step(G, tour, current_node, pos):
    plt.clf()

    # Draw only the nodes initially
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000)
    nx.draw_networkx_nodes(G, pos, nodelist=[current_node], node_color='springgreen', node_size=700)

    # If there is a path, show all edges drawn so far
    if len(tour) > 1:
        path_edges = list(zip(tour, tour[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

    # Draw edge weights as labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Display node costs as labels below the nodes
    node_cost_labels = {node: f"{G.nodes[node].get('nodeCost', '')}" for node in G.nodes}
    offset_pos = {node: (x, y - 0.07) for node, (x, y) in pos.items()}  # Adjust position
    nx.draw_networkx_labels(G, offset_pos, labels=node_cost_labels, font_size=8, font_color='black')

    plt.pause(speed)  # Pause to visualize the step


def plot_final_path(G, pos, optimal_path):
    plt.clf()

    # Draw the graph with nodes
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000)

    # Highlight the nodes on the optimal path
    nx.draw_networkx_nodes(G, pos, nodelist=optimal_path, node_color='springgreen', node_size=700)

    # Create edges from the optimal path
    optimal_edges = list(zip(optimal_path, optimal_path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=optimal_edges, edge_color='red', width=2)

    # Draw edge weights as labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Display node costs as labels below the nodes
    node_cost_labels = {node: f"{G.nodes[node].get('nodeCost', '')}" for node in G.nodes}
    offset_pos = {node: (x, y - 0.07) for node, (x, y) in pos.items()}
    nx.draw_networkx_labels(G, offset_pos, labels=node_cost_labels, font_size=8, font_color='black')

    plt.show()


def backtrack_tsp(visited, currPos, n, count, currTime, ans, hasil, macet, G, posGUI, sc):
    # Base case: If all nodes are visited and we are back to the start (node 0)
    if count == n - 1 and G.has_edge(currPos, 0):
        totalCost = currTime + G[currPos][0]['weight']
        if ans[0] > totalCost:
            ans[0] = totalCost
            return hasil[:]  # Return a copy of the optimal path
        return None

    optimal_path = None

    for i in range(n):
        if not visited[i] and G.has_edge(currPos, i):
            visited[i] = True
            hasil.append(i)

            travelTime = G[currPos][i]['weight']
            nextCost = currTime + travelTime + G.nodes[i]['nodeCost']

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
                    sc.add_log(f"Additional time: {tamb}")

            # Check for traffic delays (same logic as before)
            print(f"Visiting node {i} from {currPos}. Cost: {nextCost}")
            sc.add_log(f"Visiting node {i} from {currPos}. Cost: {nextCost}")

            # Update the plot immediately after visiting a node
            plot_graph_step(G, hasil, currPos, posGUI)  # Show the current path

            # Recur for the next node
            result = backtrack_tsp(visited, i, n, count + 1, nextCost, ans, hasil, macet, G, posGUI,sc)
            if result:
                optimal_path = result

            visited[i] = False  # Backtrack
            hasil.pop()  # Remove the last node

            # Check if the figure is still open
            if not plt.fignum_exists(1):
                print("Window closed. Exiting...")
                exit()  # Exit if the window is closed

    return optimal_path



def backtrack(G, n, macet, sc):
    pos = nx.spring_layout(G)  # Generate layout only once
    plt.ion()  # Interactive mode to update plots in real-time

    visited = [False] * n
    visited[0] = True
    ans = [float('inf')]
    hasil = [0]

    # Start the TSP solution with backtracking
    optimal_path = backtrack_tsp(visited, 0, n, 0, 0, ans, hasil, macet, G, pos, sc)
    optimal_path.append(0)

    print(f"Minimum cost: {ans[0]}")
    sc.add_log(f"\nMinimum cost: {ans[0]}")
    if optimal_path:
        x = "Optimal path: " + ' -> '.join(map(str, optimal_path))
        print(x)
        sc.add_log(x)
    plot_final_path(G, pos, optimal_path)

    plt.ioff()  # Turn off interactive mode
    plt.show()  # Show the final graph after calculations



