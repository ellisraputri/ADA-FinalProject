import random
import networkx as nx
import matplotlib.pyplot as plt
import sys
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



def plot_graph_step(G, pos, visited_edges, current_node):
    plt.clf()

    # Draw the nodes and the accumulated optimal path edges
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000)
    nx.draw_networkx_nodes(G, pos, nodelist=[current_node], node_color='springgreen', node_size=700)
    nx.draw_networkx_edges(G, pos, edgelist=visited_edges, edge_color='red', width=2)

    # Draw edge weights as labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Display node costs as labels below the nodes
    node_cost_labels = {node: f"{G.nodes[node].get('nodeCost', '')}" for node in G.nodes}
    offset_pos = {node: (x, y - 0.07) for node, (x, y) in pos.items()}
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




def dp_tsp(n, current, mask, dp, link, currTime, G, macet, posGUI, visited_edges):
    if mask == (1 << n) - 1:
        return G[current][0]['weight']

    if dp[mask][current] != -1:
        return dp[mask][current]

    result = sys.float_info.max
    best_next_node = None  # Track the optimal next node

    for i in range(n):
        val = 1 << i
        if mask & val:
            continue

        travelTime = G[current][i]['weight']
        sub = (
            dp_tsp(n, i, mask | val, dp, link, currTime + travelTime + G.nodes[i]['nodeCost'],
                   G, macet, posGUI, visited_edges) + travelTime + G.nodes[i]['nodeCost']
        )

        arrivalTime = currTime + travelTime

        # Handle traffic delays (macet)
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

        # Check if the current path is the best so far
        if sub < result:
            result = sub
            link[mask][current]=i
            best_next_node = i  # Track the optimal next node

    # Add the optimal edge to the visited edges
    if best_next_node is not None:
        visited_edges.append((current, best_next_node))
        plot_graph_step(G, posGUI, visited_edges, current)  # Plot only optimal edges

    dp[mask][current] = result
    return result




def getpath(link):
    current = 0
    mask = 1  # Start from node 0, mask initialized with 1
    path = [0]  # Path starts at node 0

    while True:
        next_node = link[mask][current]
        if next_node == 0:  # If we’re back at the start node, break the loop
            break

        path.append(next_node)
        mask |= (1 << next_node)  # Add the next node to the mask
        current = next_node

    path.append(0)  # Complete the tour by returning to the start
    return path



def dynamic_programming(G, n):
    pos = nx.spring_layout(G) 
    plt.ion()
    macet = defaultdict(list)
    macet[(1, 3)].append((5, 70, 3))
    macet[(3, 1)].append((5, 70, 3))

    dp = [[-1] * n for _ in range(1 << n)]
    link = [[0] * n for _ in range(1 << n)]

    visited_edges = []  # Track visited edges

    res = dp_tsp(n, 0, 1, dp, link, 0, G, macet, pos, visited_edges)

    optimal_path = getpath(link)
    print(f"result {res}")
    print("Path:", " ".join(map(str, optimal_path)))

    plot_final_path(G, pos, optimal_path)  # Final plot

    plt.ioff()  # Turn off interactive mode
    plt.show()




if __name__ == '__main__':
    nodeCost = [0, 15, 10, 20]
    graph = [
        [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
    ]
    G = generate_complete_graph(4, False, graph, nodeCost)
    dynamic_programming(G, 4)
