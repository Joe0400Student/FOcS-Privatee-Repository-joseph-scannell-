class NFA:

    def __init__(self, States=None, Alphabet=None, Transition_function=None, Start_State=None, Accepting_States=None,DFA=None):
        if(DFA != None):
            States, Alphabet, Transition_function, Start_State, Accepting_States = DFA.Q, DFA.alpha, {k: {v_k:[v_v] for v_k,v_v in v.items()} for k,v in DFA.TF.items()}, DFA.SS, DFA.AS
            for k,v in Transition_function.items():
                v[""] = []
        self.states = States
        self.alpha = Alphabet
        self.transition = Transition_function
        self.start_s = Start_State
        self.accepting = Accepting_States
    def __pow__(self, data):
        string, trace, boolean = data
        state = self.start_s
        if(state == trace[0]):
            for next_s,c in zip(trace,string):
                if(next_s not in self.transition[state][c]):
                    return False
                state = next_s
        return self.accepting[state] == boolean

FizzBuzz = NFA(
    States=["initial","nmod3=1","nmod5=1","nmod3=2","nmod5=2","nmod3=0","nmod5=3","nmod5=4","nmod5=0"],
    Alphabet="0",
    Transition_function={
        "initial":{"":[],"0":["nmod3=1","nmod5=1"]},
        "nmod3=1":{"":[],"0":["nmod3=2"]},
        "nmod3=2":{"":[],"0":["nmod3=0"]},
        "nmod3=0":{"":[],"0":["nmod3=1"]},
        "nmod5=1":{"":[],"0":["nmod5=2"]},
        "nmod5=2":{"":[],"0":["nmod5=3"]},
        "nmod5=3":{"":[],"0":["nmod5=4"]},
        "nmod5=4":{"":[],"0":["nmod5=0"]},
        "nmod5=0":{"":[],"0":["nmod5=1"]}
    },
    Start_State="initial",
    Accepting_States=["nmod5=0","nmod3=0","initial"]
)

FizzBuzz ** (a,b,c,d)
class Tree:
    
    def __init__(self, val=None ,sub_elements = []):
        self.sub_elements, self.val = sub_elements, val
    
    def __repr__(self):
        return f"{self.val}:branch({self.sub_elements})"
    
    def __getitem__(self,index):
        return self.sub_elements[index]
    
    def insert(self,item):
        self.sub_elements.append(item)
    
    def __setitem__(self,index,value):
        self.sub_elements[index] = value
    
class Trace:
    
    def __init__(self, state, accepting):
        self.state, self.accepting = state, accepting
    
    def __repr__(self):
        return f"{self.state}|{self.accepting}"

