from DFA import DFA


class DFAContainer:
    
    def __init__(self,DFA_nodes):
        self.DFA_nodes = DFA_nodes
        
    def __invert__(self):
        for node in self.DFA_nodes:
            node = ~node
        return self



