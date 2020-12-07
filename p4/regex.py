from NFA import NFA

class Regex:
    
    def __init__(self,empty,epsilon,char,union,star,circ):
        self.empty, self.epsilon, self.char, self.union, self.star, self.circ = empty, epsilon, char, union, star, circ
    
