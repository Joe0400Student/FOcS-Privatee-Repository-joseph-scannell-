from char import char

class alphabet:
    
    def __init__(self, l=[]):
        self.chars = l
    
    def __len__(self):
        return len(self.chars)

    def __repr__(self) -> str:
        return "contains " + ','.join(map(char.__repr__,self.chars))
    
    def __iter__(self):
        self.pos = 0
        return self
    
    def __next__(self) -> char:
        if(self.pos < len(self.chars)):
            self.pos += 1
            return self.chars[self.pos-1]
        else:
            raise StopIteration
    
