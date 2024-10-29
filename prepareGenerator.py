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
    
    def printing(self):
        print("printing:")
        print(f"Graph: {self.graph}")
        print(f"Node cost: {self.nodecost}")
        print(f"Algo: {self.algo}")
        print(f"Speed: {self.speed}")
        print(f"Node amount: {self.node_amount}")
