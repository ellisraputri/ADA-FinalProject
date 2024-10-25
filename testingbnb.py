import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from math import inf

def generate_complete_graph(num_nodes, randomize, graphInput=None, nodeCostInput=None, weight_range=(1, 100)):
    G = nx.complete_graph(num_nodes)

    if randomize:
        for u, v in G.edges():
            G.edges[u, v]['weight'] = random.randint(*weight_range)
        for u in G.nodes():
            G.nodes[u]['nodeCost'] = random.randint(*weight_range)
    else:
        for u, v in G.edges():
            G.edges[u, v]['weight'] = graphInput[u][v]
        for u in G.nodes():
            G.nodes[u]['nodeCost'] = nodeCostInput[u]

    return G

def plot_graph_step(G, tour, current_node, pos):
    plt.clf()

    # Draw only the nodes initially
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000)
    nx.draw_networkx_nodes(G, pos, nodelist=[current_node], node_color='springgreen', node_size=700)

    if len(tour) > 1 :
        path_edges = [(tour[i], tour[i + 1]) for i in range(len(tour) - 1) if tour[i] != -1 and tour[i + 1] != -1]
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
    if -1 not in optimal_path:
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

def firstMin(G, i, N):
    minimum = inf
    for k in range(N):
        if k!=i:
            if G[i][k]['weight'] < minimum and i != k:
                minimum = G[i][k]['weight']
    return minimum

def secondMin(G, i, N):
    first, second = inf, inf
    for k in range(N):
        if i == k:
            continue
        if G[i][k]['weight'] <= first:
            second = first
            first = G[i][k]['weight']
        elif G[i][k]['weight'] <= second and G[i][k]['weight'] != first:
            second = G[i][k]['weight']
    return second

def copyToFinal(curr_path, N, path):
    for i in range(N):
        path[i] = curr_path[i]
    path[N] = curr_path[0]


def BNBrec(G, curr_bound, curr_weight, lvl, curr_path, N, visited, macet, res, path, posGUI):
    if lvl == N:
        if G[curr_path[lvl - 1]][curr_path[0]]['weight'] != 0:
            curr_res = curr_weight + G[curr_path[lvl - 1]][curr_path[0]]['weight']
            if curr_res < res[0]:  # Update the result
                copyToFinal(curr_path, N, path)
                res[0] = curr_res
        return

    for i in range(N):
        if curr_path[lvl - 1] in G and i in G and not visited[i]:
            temp_bound = curr_bound
            temp_weight = curr_weight
            nextCost = 0.0

            if (curr_path[lvl - 1], i) in macet:
                travelTime = G[curr_path[lvl - 1]][i]['weight']
                end_time = curr_weight + travelTime

                for mulaimacet, akhirmacet, tambahanmacet in macet[(curr_path[lvl - 1], i)]:
                    tamb = 0.0
                    if curr_weight <= mulaimacet and end_time >= akhirmacet:
                        tamb = (akhirmacet - mulaimacet) * tambahanmacet
                    elif curr_weight < mulaimacet <= end_time and akhirmacet >= end_time:
                        tamb = (end_time - mulaimacet) * tambahanmacet
                    elif mulaimacet < curr_weight < akhirmacet <= end_time:
                        tamb = (akhirmacet - curr_weight) * tambahanmacet
                    elif curr_weight >= mulaimacet and end_time <= akhirmacet:
                        tamb = (end_time - curr_weight) * tambahanmacet

                    nextCost += tamb

            curr_weight += G[curr_path[lvl - 1]][i]['weight'] + nextCost

            if lvl == 1:
                curr_bound -= (firstMin(G, curr_path[lvl - 1], N) + firstMin(G, i, N)) / 2
            else:
                curr_bound -= (secondMin(G, curr_path[lvl - 1], N) + firstMin(G, i, N)) / 2

            if curr_bound + curr_weight < res[0]:  # Use res[0]
                curr_path[lvl] = i
                visited[i] = True
                curr_weight += nodeCost[i]
                plot_graph_step(G, curr_path, i, posGUI)
                BNBrec(G, curr_bound, curr_weight, lvl + 1, curr_path, N, visited, macet, res, path, posGUI)

            curr_weight = temp_weight
            curr_bound = temp_bound
            visited[i] = False



def bnb(G, N):
    pos = nx.spring_layout(G)  # Generate layout only once
    plt.ion()  # Interactive mode to update plots in real-time

    curr_path = [-1] * (N + 1)
    curr_bound = 0

    macet = defaultdict(list)
    macet[(0, 1)].append((2, 5, 1.0))
    macet[(0, 1)].append((7, 12, 0.5))

    path = [-1] * (N + 1)

    for i in range(N):
        curr_bound += (firstMin(G, i, N) + secondMin(G, i, N))

    curr_bound = (curr_bound + 1) // 2  # Ensure proper rounding

    visited = [False] * N
    visited[0] = True
    curr_path[0] = 0
    res = [inf]  # Use a list to store the result

    BNBrec(G, curr_bound, 0, 1, curr_path, N, visited, macet, res, path, pos)

    if res[0] == inf:
        print("No valid path found.")
    else:
        print(f"Minimum cost: {res[0]}")
        print("Optimal path: ", ' -> '.join(map(str, path)))

    plot_final_path(G, pos, path)
    plt.ioff()  # Turn off interactive mode
    plt.show()  # Show the final graph after calculations



if __name__ == '__main__':
    nodeCost = [0, 5, 6]
    graph = [
        [0, 10, 15],
        [10, 0, 20],
        [15, 20, 0]
    ]

    G = generate_complete_graph(3, False, graph, nodeCost)
    bnb(G, 3)
