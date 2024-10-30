from collections import defaultdict
import networkx as nx
import backtrackGUI as bt
import BnBGUI  as bnb
import dpGUI as dp
from scrollCanvas import ScrollCanvas

class prepareGenerator:
    def __init__(self):
        print("terinit")
    
    def set_graph(self, graph):
        self.graph=graph

    def set_nodecost(self, nodecost):
        self.nodecost = nodecost
    
    def set_algochosen(self, algo):
        self.algo = algo
    
    def set_speedchosen(self, speed):
        self.speed = speed
    
    def set_nodeamount(self, node_amount):
        self.node_amount = node_amount
    
    def set_manual_graph(self, g):
        self.manual_graph=g
    
    def set_manual_nodecost(self,g):
        self.manual_nodecost =g

    def set_manual_congestion(self,g):
        self.manual_congestion=g
    
    def set_congestion(self, congestion):
        self.congestion = congestion
    
    def set_root(self,c):
        self.root=c
    

    def running(self):
        g =None
        n = None
        c = None
        if(self.manual_graph==True): g=self.graph
        if(self.manual_nodecost==True): n=self.nodecost
        if(self.manual_congestion==True): 
            c2 = defaultdict(list)
            for i in range(len(self.congestion)):
                for j in range(len(self.congestion[i])):
                    if not self.congestion[i][j] and i!=j: 
                        c2[(i,j)].append((0,0,0))
                        continue
                    elif not self.congestion[i][j] and i==j:
                        continue
                    a,b,percent = self.congestion[i][j]
                    c2[(i,j)].append((a,b,percent))
            c=c2


        if(self.algo=="Brute Force"):
            G =bt.generate_complete_graph(self.node_amount, g, n)
            macet = bt.generate_congestion(self.node_amount, c)
            self.generate_summary(G, macet)
            if(self.speed=="Moderate"): bt.speed=0.6
            elif(self.speed=="Fast"): bt.speed=0.2
            elif(self.speed=="Slow"): bt.speed=1.2
            print(macet)
            sc = ScrollCanvas(self.root,800, 500)
            bt.backtrack(G, self.node_amount,macet, sc)
            return

        if self.algo=="Branch and Bound":
            G =bnb.generate_complete_graph(self.node_amount, g, n)
            macet = bnb.generate_congestion(self.node_amount, c)
            self.generate_summary(G, macet)
            if(self.speed=="Moderate"): bnb.speed=0.6
            elif(self.speed=="Fast"): bnb.speed=0.2
            elif(self.speed=="Slow"): bnb.speed=1.2
            print(macet)
            sc=ScrollCanvas(self.root,800,500)
            bnb.bnb(G, self.node_amount, macet,sc)
            return
        
        if self.algo=="Dynamic Programming":
            G =dp.generate_complete_graph(self.node_amount, g, n)
            macet = dp.generate_congestion(self.node_amount, c)
            self.generate_summary(G, macet)
            if(self.speed=="Moderate"): dp.speed=0.6
            elif(self.speed=="Fast"): dp.speed=0.2
            elif(self.speed=="Slow"): dp.speed=1.2
            print(macet)
            sc = ScrollCanvas(self.root,800,500)
            dp.dynamic_programming(G,self.node_amount,macet, sc)
            return
    

    def generate_summary(self, G, macet):
        summaryCanvas = ScrollCanvas(self.root, 800,140)
        summaryCanvas.add_log("Graph: ")
        for u,v in G.edges():
            summaryCanvas.add_log(f"Weight from {u} to {v}: {G.edges[u, v]['weight']}") 

        summaryCanvas.add_log("\nNode cost:")
        for u in G.nodes():
            summaryCanvas.add_log(f"Node cost {u}: {G.nodes[u]['nodeCost']}")
        
        summaryCanvas.add_log("\nCongestions:")
        print(macet)
        for key,val in macet.items():
            u,v= key
            for lis in val:
                start,end,cost = lis
                summaryCanvas.add_log(f"Congestion in {u} to {v} that causes {cost} times slower: ")
                summaryCanvas.add_log(f"Starts at {start} and ends at {end}")
