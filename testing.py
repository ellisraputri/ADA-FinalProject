import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

def generate_complete_graph(num_nodes,randomize, graphInput=None, nodeCostInput=None, weight_range=(1, 100)):
    G = nx.complete_graph(num_nodes)

    if(randomize):
        for u, v in G.edges():
            G.edges[u, v]['weight'] = random.randint(*weight_range) 
        for u in G.nodes():
            G.nodes[u]['nodeCost']= random.randint(*weight_range) 
    else:
        for u, v in G.edges():
            G.edges[u, v]['weight'] =graphInput[u][v]
        for u in G.nodes():
            G.nodes[u]['nodeCost'] = nodeCostInput[u]

    return G



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

    plt.pause(0.5)  # Pause to visualize the step


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


def backtrack_tsp(visited, currPos, n, count, currTime, ans, hasil, macet, G, posGUI):
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

            # Check for traffic delays (same logic as before)
            print(f"Visiting node {i} from {currPos}. Cost: {nextCost}")

            # Update the plot immediately after visiting a node
            plot_graph_step(G, hasil, currPos, posGUI)  # Show the current path

            # Recur for the next node
            result = backtrack_tsp(visited, i, n, count + 1, nextCost, ans, hasil, macet, G, posGUI)
            if result:
                optimal_path = result

            visited[i] = False  # Backtrack
            hasil.pop()  # Remove the last node

            # Check if the figure is still open
            if not plt.fignum_exists(1):
                print("Window closed. Exiting...")
                exit()  # Exit if the window is closed

    return optimal_path



def backtrack(G, n):
    pos = nx.spring_layout(G)  # Generate layout only once
    plt.ion()  # Interactive mode to update plots in real-time
    
    macet = defaultdict(list)
    macet[(1,3)].append((5, 70,3))
    macet[(3,1)].append((5,70,3))

    visited = [False] * n
    visited[0] = True
    ans = [float('inf')]
    hasil = [0]

    # Start the TSP solution with backtracking
    optimal_path = backtrack_tsp(visited, 0, n, 0, 0, ans, hasil, macet, G, pos)
    optimal_path.append(0)

    print(f"Minimum cost: {ans[0]}")
    if optimal_path:
        print("Optimal path: ", ' -> '.join(map(str, optimal_path)))
    plot_final_path(G, pos, optimal_path)

    plt.ioff()  # Turn off interactive mode
    plt.show()  # Show the final graph after calculations



if __name__ == '__main__':
    nodeCost = [0, 15, 10, 20]
    graph = [
        [0, 10, 15, 20.0],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
    ]
    G = generate_complete_graph(4, False, graph, nodeCost)
    backtrack(G, 4)
