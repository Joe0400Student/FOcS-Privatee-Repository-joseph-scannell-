class char:
    
    def __init__(self, repr: str):
        self.repr = repr
    
    def __repr__(self) -> str:
        return self.repr
    
    def __eq__(self, other) -> bool:
        return self.__repr__() == other.__repr__()
    
    def __hash__(self):
        return hash(repr)

