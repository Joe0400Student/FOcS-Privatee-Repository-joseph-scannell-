from typing import List
import string

cart_prod = lambda A,B: [(a,b) for a in A for b in B]

union = lambda A,B: list(set(A) | set(B))

class DFA:
    
    def __init__(self, Q: list, alpha: list, TF: list, SS: int, AS:List[bool]):
        self.Q, self.alpha, self.TF, self.SS, self.AS = Q, alpha, TF, SS, AS
    
    def __repr__(self, string_to_iterate):
        state = self.SS
        s = [str(self.Q[state])]
        for c in string_to_iterate:
            state = self.TF[state](c)
            s.append(str(self.Q[state]))
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
        TF = [
                (lambda a : 
                    self.TF[ self.Q.index(R1) ](a) * len(other.Q) + 
                    other.TF[ other.Q.index(R2) ](a)
                )
                for R1,R2 in Q
            ]
        SS = self.SS*len(other.Q) + other.SS
        AS = [self.AS[self.Q.index(a[0])] or other.AS[other.Q.index(a[1])] for a in Q]
        return DFA(Q,alpha,TF,SS,AS)
    
    def __and__(self,other):
        return ~((~self)|(~other))
    
    def __le__(self,other):
        return DFS(self & ~other) == False
    
    def __eq__(self,other):
        return self <= other and other <= self


## DFA worker was orignially gonna be BFS, but hard so no...

def DFS(dfa,State=None,previous_states=[],visited_chars=[]):
    if(State == None):
        State = dfa.SS
    if(dfa.AS[State]):
        return f"\"{''.join(visited_chars)}\""
    previous_states.append(State)
    for c in dfa.alpha:
        if dfa.TF[State](c) not in previous_states:
            v = DFS(dfa,dfa.TF[State](c),previous_states,visited_chars + [c])
            if v != False:
                return v
    return False

odd = DFA(
    ["0","1"],
    ['0','1'],
    [
        (lambda a: 1 if a == '1' else 0),
        (lambda a: 1 if a == '0' else 0)
    ],
    0,
    [True,False]
)
dog = DFA(
    ["q_None","q_D","q_O","q_G"],
    string.ascii_lowercase,
    [
        (lambda a: 1 if a == 'd' else 0),
        (lambda a: 1 if a == 'd' else 2 if a == 'o' else 0),
        (lambda a: 1 if a == 'd' else 3 if a == 'g' else 0),
        (lambda a: 3)
    ],
    0,
    [False,False,False,True]
)
even = ~odd
not_dog = ~dog
cat = DFA(
    ["q_None","q_C","q_A","q_T"],
    string.ascii_lowercase,
    [
        (lambda a: 1 if a == 'c' else 0),
        (lambda a: 1 if a == 'c' else 2 if a == 'a' else 0),
        (lambda a: 1 if a == 'c' else 3 if a == 't' else 0),
        (lambda a: 3)
    ],
    0,
    [False,False,False,True]
)
not_cat = ~cat
cat_or_dog = cat | dog
not_cat_and_not_dog = ~cat & ~dog




print(DFS(dog))

print(DFS(odd))
print(DFS(~odd))
print(DFS(odd | odd))
print(DFS(odd | ~odd))
print(DFS(odd & odd))
print(f"DFS(odd & ~odd):{DFS(odd & ~odd)}")
print(f"odd <= odd:{odd <= odd}")
print(f"emtpy <= ~emtpy:{odd <= ~odd}")
print(f"odd == odd:{odd == odd}")
print(f"odd == ~odd:{odd == ~odd}")

print(odd.__repr__("01"))
