from typing import List
import string

cart_prod = lambda A,B: [(a,b) for a in A for b in B]

union = lambda A,B: list(set(A) | set(B))



class DFA:
    
    def __init__(self, Q, alpha, TF, SS, AS):
        self.Q, self.alpha, self.TF, self.SS, self.AS = Q, alpha, TF, SS, AS
    
    def __repr__(self, string_to_iterate):
        state = self.SS
        s = state
#        print(state)
        for c in string_to_iterate:
            s += (state := self.TF[state][c])
        return '->'.join(s)
    
    def iterate_DFA(self,string_to_iterate):
        state = self.SS
        for c in string_to_iterate:
            state = self.TF[state][c]
        return self.AS[state]
    
    def __invert__(self):
        AS = {a:not self.AS[a] for a in self.Q}
        return DFA(self.Q,self.alpha,self.TF,self.SS,AS)
    
    def __or__(self, other):
        Q = cart_prod(self.Q,other.Q)
        alpha = union(self.alpha,other.alpha)
        TF = {(a,b) : { A: (self.TF[a][A],other.TF[b][A]) for A in alpha } for a,b in Q}
        SS = (self.SS,other.SS)
        AS = {(a,b):self.AS[a] or other.AS[b] for a,b in Q}
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
        if(dfa.TF[State][c] not in previous_states):
            val = DFS(dfa,dfa.TF[State][c],previous_states,visited_chars + [c])
            if(False != val):
                return val
    return False

odd = DFA(
    ["d0","d1"],
    ['0','1'],
    {
        "d0":{"0":"d0","1":"d1"},
        "d1":{"0":"d1","1":"d0"}
    },
    "d0",
    {"d0":False,"d1":True}
)
dog = DFA(
    ["q_None","q_D","q_O","q_G"],
    string.ascii_lowercase,
    {
        "q_None":{a:"q_D" if a == "d" else "q_None" for a in string.ascii_lowercase},
        "q_D":{a:"q_D" if a == "d" else "q_O" if a == "o" else "q_None" for a in string.ascii_lowercase},
        "q_O":{a:"q_D" if a == "d" else "q_G" if a == "g" else "q_None" for a in string.ascii_lowercase},
        "q_G":{a:"q_G" for a in string.ascii_lowercase}
    },
    "q_None",
    {"q_None":False,"q_D":False,"q_O":False,"q_G":True}
)
even = ~odd
not_dog = ~dog
cat = DFA(
    ["q_None","q_C","q_A","q_T"],
    string.ascii_lowercase,
    {
        "q_None":{a:"q_C" if a == "c" else "q_None" for a in string.ascii_lowercase},
        "q_C":{a:"q_C" if a == "c" else "q_A" if a == "a" else "q_None" for a in string.ascii_lowercase},
        "q_A":{a:"q_C" if a == "c" else "q_T" if a == "t" else "q_None" for a in string.ascii_lowercase},
        "q_T":{a:"q_T" for a in string.ascii_lowercase}
    },
    "q_None",
    {"q_None":False,"q_C":False,"q_A":False,"q_T":True}
)
not_cat = ~cat
cat_or_dog = cat | dog
not_cat_and_not_dog = ~cat & ~dog

print(cat_or_dog.iterate_DFA("ddd"))
print(cat_or_dog.__repr__("ddd"))


print(f"DFS(dog):{DFS(dog)}")

print(f"DFS(odd):{DFS(odd)}")
print(f"DFS(~odd):{DFS(~odd)}")
print(f"DFS(odd | odd):{DFS(odd | odd)}")
print(f"DFS(odd | ~odd):{DFS(odd | ~odd)}")
print(f"DFS(odd & odd):{DFS(odd & odd)}")
print(f"DFS(odd & ~odd):{DFS(odd & ~odd)}")
print(f"odd <= odd:{odd <= odd}")
print(f"emtpy <= ~emtpy:{odd <= ~odd}")
print(f"odd == odd:{odd == odd}")
print(f"odd == ~odd:{odd == ~odd}")

print(odd.__repr__("01"))
