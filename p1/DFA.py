class DFA:
    
    def __init__(self, accepting):
        self.accepted = accepting
    
    def next(self, item):
        return self.next_table[item]

    def add_next_table(self, table):
        self.next_table = table
    
    def accepting(self) -> bool:
        return self.accepted
