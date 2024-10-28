class prepareGenerator:
    def __init__(self):
        print("terinit")
    
    def set_graph(self, graph):
        print("executes set graph")
        print(graph)
        self.graph=graph

    def set_nodecost(self, nodecost):
        print("executes set nodecost")
        self.nodecost = nodecost
    
    def printing(self):
        print("printing:")
        print(self.graph)
        print(self.nodecost)
