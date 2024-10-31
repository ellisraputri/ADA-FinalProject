import random
import networkx as nx
import matplotlib.pyplot as plt
import sys
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



def plot_graph_step(G, pos, visited_edges, current_node):
    plt.clf()

    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000)
    nx.draw_networkx_nodes(G, pos, nodelist=[current_node], node_color='springgreen', node_size=700)
    nx.draw_networkx_edges(G, pos, edgelist=visited_edges, edge_color='red', width=2)

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    node_cost_labels = {node: f"{G.nodes[node].get('nodeCost', '')}" for node in G.nodes}
    offset_pos = {node: (x, y - 0.07) for node, (x, y) in pos.items()}
    nx.draw_networkx_labels(G, offset_pos, labels=node_cost_labels, font_size=8, font_color='black')

    plt.pause(speed)  


def plot_final_path(G, pos, optimal_path):
    plt.clf()

    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000)
    nx.draw_networkx_nodes(G, pos, nodelist=optimal_path, node_color='springgreen', node_size=700)

    optimal_edges = list(zip(optimal_path, optimal_path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=optimal_edges, edge_color='red', width=2)

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    node_cost_labels = {node: f"{G.nodes[node].get('nodeCost', '')}" for node in G.nodes}
    offset_pos = {node: (x, y - 0.07) for node, (x, y) in pos.items()}
    nx.draw_networkx_labels(G, offset_pos, labels=node_cost_labels, font_size=8, font_color='black')

    plt.show()




def dp_tsp(n, current, mask, dp, link, currTime, G, macet, posGUI, visited_edges, sc):
    if mask == (1 << n) - 1:
        return G[current][0]['weight']

    if dp[mask][current] != -1:
        return dp[mask][current]

    result = sys.float_info.max
    best_next_node = None  

    for i in range(n):
        val = 1 << i
        if mask & val:
            continue

        travelTime = G[current][i]['weight']
        sub = (
            dp_tsp(n, i, mask | val, dp, link, currTime + travelTime + G.nodes[i]['nodeCost'],
                   G, macet, posGUI, visited_edges, sc) + travelTime + G.nodes[i]['nodeCost']
        )

        arrivalTime = currTime + travelTime

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
                sc.add_log(f"Additional time: {tamb}")

    
        if sub < result:
            result = sub
            link[mask][current]=i
            best_next_node = i  
        
        sc.add_log(f"Visiting node {i} from {current}. Cost: {sub}")
        
    if best_next_node is not None:
        visited_edges.append((current, best_next_node))
        plot_graph_step(G, posGUI, visited_edges, current)  
    
    if not plt.fignum_exists(1):
        print("Window closed. Exiting...")
        exit()  

    dp[mask][current] = result
    return result




def getpath(link):
    current = 0
    mask = 1  
    path = [0]  

    while True:
        next_node = link[mask][current]
        if next_node == 0:  
            break

        path.append(next_node)
        mask |= (1 << next_node)  
        current = next_node

    path.append(0)  
    return path



def dynamic_programming(G, n, macet, sc):
    pos = nx.spring_layout(G) 
    plt.ion()

    dp = [[-1] * n for _ in range(1 << n)]
    link = [[0] * n for _ in range(1 << n)]

    visited_edges = []  

    res = dp_tsp(n, 0, 1, dp, link, 0, G, macet, pos, visited_edges, sc)

    optimal_path = getpath(link)
    print(f"result {res}")
    sc.add_log(f"\nMinimum cost: {res}")
    print("Path:", " ".join(map(str, optimal_path)))
    x = "Optimal path: " + ' -> '.join(map(str, optimal_path))
    sc.add_log(x)

    plot_final_path(G, pos, optimal_path)  

    plt.ioff()  
    plt.show()




