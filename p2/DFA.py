from typing import Generic, List

cart_prod = lambda A,B: [(a,b) for a in A for b in B]

union = lambda A,B: list(set(A) | set(B))

T = TypeVar('T')
class DFA:
    
    def __init__(self, Q: list, alpha: list, TF: list, SS: int:, AS:List[bool]):
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
        for c in string_to_iterate:
            state = TF[state](c)
        return AS[state]
    
    def __invert__(self):
        AS = [not v for v in self.AS]
        return DFA(self.Q,self.alpha,self.TF,self.SS,AS)
    
    def __or__(self, other):
        Q = cart_prod(self.Q,other.Q)
        alpha = union(self.alpha,other.alpha)
        TF = [(lambda a : self.TF[R1](a)*len(other.Q)+other.TF[R2](a)) for R1,R2 in Q]
        SS = Q.index((self.SS,other.SS))
        AS = [self.TF[q[0]] or other.TF[q[1]] for q in Q]
        return DFA(Q,alpha,TF,SS,AS)
    
    def __and__(self,other):
        return ~((~self)|(~other))
    
    
## DFA worker was orignially gonna be BFS, but hard so no...

def DFS(dfa,State=None,previous_states=[],visited_chars=[]):
    if(State == None):
        State = dfa.SS
    if(dfa.AS[State]):
        return ''.join(visited_chars)
    previous_states.append(State)
    for c in dfa.alpha:
        if dfa.TF[State](c) not in previous_states:
            v = DFS(dfa,dfa.TF[State](c),previous_states,visited_chars += [c])
            if v != False:
                return v
    return False

