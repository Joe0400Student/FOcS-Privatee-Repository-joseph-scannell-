class NFA:
    
    def __init__(self, States, Alphabet, Transition_function, 
                 Start_State, Accepting_States):
        self.states = States
        self.alpha = Alphabet
        self.transition = Transition_function
        self.start_s = Start_State
        self.accepting = accepting_states
    
    def __init__(self,DFA):
        self.states = DFA.Q
        self.alpha = DFA.alpha
        self.transition = {k:{v_k:[v_v] for v_k,v_v in v.items()} for k,v in DFA.TF.items()}
        self.start_s = DFA.SS
        self.accepting = DFA.AS
    
    
    def __pow__(self, data):
        string, trace, boolean = data
        state = self.start_s
        if(state == trace[0]):
        for next_s,c in zip(trace,string):
            if(next_s not in self.transition[state][c]):
                return False
            state = next_s
        return self.accepting[state] == boolean
    
    
