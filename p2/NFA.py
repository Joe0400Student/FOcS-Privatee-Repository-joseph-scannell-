import math

union = lambda A,B: list(set(A)|set(B))
def decorate(s,final=False):
    a = "".join(["=" for i in range(50)])
    spaces = " ".join(['' for i in range(100)])
    def wrap(func):
        def _():
            print(f"{a}{s}{a}"[math.floor(len(s)/2):-math.ceil(len(s)/2)-2]+"\\\\")
            try:
                func()
                print(f"||{s} PASSED{''.join([' ' for i in range(100)])}"[:98]+"||")
            except AssertionError as e:
                print(f"||AssertionError: {e}{spaces}"[:98]+"||")
                if(not final):
                    assert False, f"{s}: {e}"
            finally:
                print("\\\\" + "".join(["_" for i in range(100)])[2:])
        return _
    return wrap

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
        if(state != trace[0]):
            return False
        for next_s,c in zip(trace[1:],string):
            if(next_s not in self.transition[state][c]):
                return False
            state = next_s
        return self.accepting[state] == boolean
    def __or__(self,other):
        tf = self.transition | other.transition
        tf[""] = {"":[self.start_s,other.start_s]}
        print(tf[""][""])
        return NFA(
            States=list(set([""])|set(self.states)|set(other.states)),
            Alphabet=self.alpha,
            Transition_function=tf,
            Start_State="",
            Accepting_States={"":False}|self.accepting|other.accepting
        )
    def backtrack(self, string):
        return BackTrack(self,self.start_s,[],string)
    def fork(self):
        return {self.start_s:DFS(self,self.start_s,[self.start_s])}
def DFS(nfa,state,traces):
    current_dict = {}
    for key in nfa.transition[state]:
        for states in nfa.transition[state][key]:
            if(states not in traces):
                val = DFS(nfa,states,traces+[states])
                current_dict[states] = val if val != None else {}
            else:
                current_dict[states]="loopback"
    if(len(current_dict) != 0):
        return current_dict
    return None

# traces are for epsilon in this
def BackTrack(nfa,state,traces,string):
    if(string == ""):
        return nfa.accepting[state]
    char = string[0]
    for states in nfa.transition[state][char]:
        if(BackTrack(nfa,states,[], string[1:])):
            return True
    for states in nfa.transition[state][""]:
        if states not in traces:
            if(BackTrack(nfa,states,traces + [states], string)):
                return True
    return False

FizzBuzz = NFA(
    States=["initial","nmod3=1","nmod5=1","nmod3=2","nmod5=2","nmod3=0","nmod5=3","nmod5=4","nmod5=0"],
    Alphabet=["0"],
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
    Accepting_States={"nmod5=0":True,"nmod3=0":True,"initial":True,"nmod3=1":False,"nmod5=1":False,
                      "nmod3=2":False,"nmod5=2":False,"nmod5=3":False,"nmod5=4":False}
)
"""
    0
    accepting
    nmod3=1,nmod5=1
    00000
    accepting
    nmod3=1,nmod5=1
    nmod3=2,nmod5=2
    nmod3=0,nmod5=3
    nmod3=1,nmod5=4
    nmod3=2,nmod5=0
    fail   ,accepting
"""
cogOrCat = NFA(
    States=["initialc","cOG","cAT","A","T","O","G"],
    Alphabet="abcdefghijklmnopqrstuvwxyz",
    Transition_function={
        "initialc":{"c":["cOG","cAT"]},
        "cOG":{"o":["O"]},
        "cAT":{"a":["A"]},
        "O":{"g":["G"]},
        "A":{"t":["T"]},
        "G":{},
        "T":{}
    },
    Start_State="initialc",
    Accepting_States={"initialc":False,"cOG":False,"cAT":False,"A":False,"T":True,"O":False,"G":True}
)
@decorate("FizzBuzzTest")
def FizzBuzzTest():
    assert FizzBuzz ** ("000",["initial","nmod3=1","nmod3=2","nmod3=0"],True), "Doesnt work"
    assert not FizzBuzz ** ("000",["initial","nmod3=1","nmod5=0"],False),"Doesnt work"
@decorate("ForkTest")
def fork():
    print(FizzBuzz.fork())
    print(cogOrCat.fork())
    assert True, "Didnt throw error"
@decorate("UnionTest")
def union():
    print((FizzBuzz|cogOrCat).fork())

@decorate("BackTrackTest")
def backtrack_test():
    assert FizzBuzz.backtrack("000"), "backtrack returned false"
    assert not FizzBuzz.backtrack("00"), "backtrack returned true"
@decorate("TestSuite",True)
def test_suite():
    FizzBuzzTest()
    fork()
    union()
    backtrack_test()
test_suite()
