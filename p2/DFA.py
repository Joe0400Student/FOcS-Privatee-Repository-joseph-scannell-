from typing import Generic, List

T = TypeVar('T')
class DFA:
    
    def __init__(self, Q: list, alpha: list, TF: List[List[int]], SS: int:, AS:List[bool]):
        self.Q, self.alpha, self.TF, self.SS, self.AS = Q, alpha, TF, SS, AS
    
    def __repr__(self, string_to_iterate):
        state = self.SS
        s = [str(Q[state])]
        for c in string_to_iterate:
            state = TF[state][alpha.index(c)]
            s.append(str(Q[state]))
        return '->'.join(s)
    
    def iterate_DFA(self,string_to_iterate):
        state = self.SS
        iterate = [alpha.index(c) for c in string_to_iterate]
        for i in iterate:
            state = TF[state][i]
        return AS[state]
    
    def __invert__(self):
        AS = [not v for v in self.AS]
        return DFA(self.Q,self.alpha,self.TF,self.SS,AS)
    

## DFA worker was orignially gonna be BFS, but hard so no...
class DFAWorker:
    
    def __init__(DFA):
        self.DFA = DFA
        self.state = DFA.SS
        self.previous = []
        self.alpha = DFA.alpha
    
    def __init__(DFA, state, previous=[], characters=[]):
        self.DFA = DFA
        self.state = state
        self.previous = previous
        self.alpha = DFA.alpha
        
    def DFS(self):
        if(self.DFA.AS[self.state]):
            return ''.join(self.characters)
        previous = self.previous + [self.state]
        for c in self.alpha:
            state = self.DFA.TF[self.state][self.alpha.index(c)]
            if(state not in previous):
                ret_val = DFAWorker(self.DFA,state,previous,self.characters + [c]).DFS()
                if(ret_val != False):
                    return ret_val
        return False

