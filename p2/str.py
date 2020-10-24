from char import char
from typing import Iterable, List
from alphabet import alphabet

class string:
    
    def __init__(self):
        self.chars = []
    
    def __repr__(self) -> str:
        return ''.join(map(char.__repr__,self.chars))
    
    def __iter__(self):
        self.pos = 0
        return self
    
    def __next__(self) -> char:
        if(self.pos < len(self.chars)):
            self.pos += 1
            return self.chars[self.pos-1]
        else:
            raise StopIteration
    
    def __add__(self, c):
        self.chars.append(c)
        return self

