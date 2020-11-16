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
        self.transition = {k:[v] for k,v in DFA.TF.items()}
        self.start_s = DFA.SS
        self.accepting = DFA.AS
    
