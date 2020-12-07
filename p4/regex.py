from NFA import NFA

class Regex:
    
    def __init__(self,empty=None,epsilon=None,char=None,union=None,star=None,circ=None):
        if(empty != None):
            self.empty = empty
            self.type = 0
        elif(epsilon != None):
            self.epsilon = epsilon
            self.type = 1
        elif(char != None):
            self.char = char
            self.type = 2
        elif(union != None):
            self.union = union
            self.type = 3
        elif(star != None):
            self.star = star
            self.type = 4
        elif(circ != None):
            self.circ = crc
            self.type = 5
    
    
    def __repr__(self):
        if(self.type == 0):
            return "∅"
        elif(self.type == 1):
            return "ϵ"
        elif(self.type == 2):
            return self.char
        elif(self.type == 3):
            return f"({self.char[0].__repr__()}) | ({self.char[1].__repr__()})"
        elif(self.type == 4):
            return f"({self.star.__repr__()})*"
        elif(self.type == 5):
            return f"({self.circ[0].__repr__()})⚬({self.cric[1].__repr__()})"
    
    

