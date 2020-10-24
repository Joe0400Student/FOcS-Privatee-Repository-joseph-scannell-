class DFA:
    
    def __init__(self, accepting, name=""):
        self.accepted = accepting
        self.name = name
    
    def next(self, item):
        return self.next_table[item]

    def add_next_table(self, table):
        self.next_table = table
    
    def accepting(self):
        return self.accepted

    def __repr__(self):
        return self.name
    
    def geT_configurations(DFA_node, choices):
        positions = []
        for c in choices:
            positions.append(str(DFA_node))
            DFA_node = DFA_node.next(c)
        
        return '->'.join(positions + [str(DFA_node)])

    def __invert__(self):
        self.accepted = not self.accepted
        return self
