import math
from DFA import DFA
from random import choices
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

class Tree(dict):
    pass


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
        name = ''.join(choices("abcdefghijklmnopqrstuvwxyz",k=20))
        tf[name] = {"":[self.start_s,other.start_s]}
        return NFA(
            States=list(set([name])|set(self.states)|set(other.states)),
            Alphabet=self.alpha,
            Transition_function=tf,
            Start_State=name,
            Accepting_States={name:False}|self.accepting|other.accepting
        )
    def __add__(self,other):
        tf = self.transition | other.transition
        for each in self.accepting:
            if(self.accepting[each]):
                self.transition[each][""] = [other.start_s]
        temp_accepting = other.accepting
        for k in self.accepting:
            temp_accepting[k] = False
        return NFA(
            States=self.states+other.states,
            Alphabet=self.alpha,
            Transition_function=tf,
            Start_State=self.start_s,
            Accepting_States=temp_accepting
        )
    def backtrack(self, string):
        return BackTrack(self,self.start_s,[],string)
    def tree(self):
        return {(self.start_s,self.accepting[self.start_s]):DFS(self,self.start_s,[self.start_s])}
    def fork(self,string):
        if((v := fork_string(self,self.start_s,[],string)) != None):
            return {(self.start_s,self.accepting[self.start_s]):v}
        return None
    def __repr__(self):
        return f"{self.transition}"
    def kleene_star(self):
        tf = self.transition
        name = ''.join(choices("abcdefghijklmnopqrstuvwxyz",k=20))
        tf[name] = {"":[self.start_s]}
        for each in self.accepting:
            if(self.accepting[each]):
                if("" in tf[each]):
                    tf[each][""] = tf[each][""] + [name]
                else:
                    tf[each][""] = [name]
        accepting = self.accepting
        accepting[name] = True
        return NFA(
            States=self.states,
            Alphabet=self.alpha,
            Start_State=name,
            Transition_function=tf,
            Accepting_States=accepting
        )

    def closure(self,state):
        return closure(state,self.transition,[])

    def any_accept(self,states):
        for state in states:
            if(self.accepting[state]):
                return True
        return False
    def compile(self) -> DFA:
        ss = self.closure(self.start_s)
        
        jobs = [ss]
        table = {ss:{}}
        
        for job in jobs:
            for c in self.alpha:
                #print(f"{c}")
                new_state = ()
                for state in job:
                    if(c in self.transition[state]):
                        for tmp_state in self.transition[state][c]:
                            new_state += self.closure(tmp_state)
                new_state = tuple(sorted(no_duplicates(new_state)))
                if(new_state == ()):
                    table[job][c] = None
                else:
                    table[job][c] = new_state
                    if(new_state not in jobs):
                        jobs.append(new_state)
                        table[new_state] = {}
        looping_state = ("looping",) + (''.join(choices("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",k=40)),)
        accepting = {looping_state:False}
        for state in table:
            accepting[state] = any(map(lambda c: self.accepting[c],state))
        table[looping_state] = {c: looping_state for c in self.alpha}
        for value in table:
            for c in table[value]:
                if(table[value][c] == None):
                    table[value][c] = looping_state
        return DFA([*table],self.alpha,table,ss,accepting)
"""    
    def compile(self) -> DFA:
        table = {}
        start_state = tuple(sorted(self.closure(self.start_s)))
        #print(len(start_state))
        table = {state:{character:None for character in self.alpha}
            for state in map(
                lambda a: tuple(sorted(self.closure(a))) 
                if type(a) != type((0,0)) else a,self.states)
        }
        table[start_state] = {a: None for a in self.alpha}
        jobs = no_duplicates([states for states in table])
#        print(len(jobs))
        #input()
        i = 0
        for job in jobs:
#            print(f"{i}:{len(jobs)}")
            #print(job)
#            print(jobs.index(job))
            table[job] = process_job(self,job, self.transition)
            for newly_generated in table[job].values():
                if(newly_generated not in jobs and newly_generated != None):
                    #print(type(newly_generated[0]))
                    #input()
                    #print(type(jobs[0][0]))
                    jobs.append(newly_generated)
                    table[newly_generated] = {c:None for c in self.alpha}
            i += 1
        #print("outside")
        new_state = (''.join(choices("abcdefghijklmnopqrstuvwxyz1234567890_-\\",k=40)),)
        table[new_state] = {a:new_state for a in self.alpha}
        for key in table:
            for char in table[key]:
                if(table[key][char] == None):
                    table[key][char] = new_state
        accepting = {}
        accepting[new_state] = False
        for state in jobs:
            accepting[state] = any(map(lambda a: self.accepting[a], state))
        jobs.append(new_state)
        return DFA(jobs,self.alpha,table,start_state,accepting)
def process_job(nfa: NFA, state, transition_table: dict):
    current_working_dict = {c:None for c in nfa.alpha}
    for sub_jobs in state:
        #print(sub_jobs)
#        print(len(sub_jobs))
        single_dict = get_single_state_dict(nfa,sub_jobs,transition_table)
        for c in nfa.alpha:
            if(current_working_dict[c] == None):
                if(single_dict[c] != ()):
                    current_working_dict[c] = single_dict[c]
            else:
                #print(current_working_dict[c])
                #print(current_working_dict[c] + single_dict[c])
                current_working_dict[c] = tuple(sorted(no_duplicates(current_working_dict[c] + single_dict[c])))
    return current_working_dict

def get_single_state_dict(nfa: NFA, state, dictionary: dict) -> dict:
    tmp = {}
    for c in nfa.alpha:
        if(c in dictionary[state]):
            temp = dictionary[state][c]
            tmp[c] = tuple(no_duplicates([v for t in temp for v in nfa.closure(t)]))
            #input()
            #tmp[c] = tuple([v for v in map(lambda a: sorted(no_duplicates(nfa.closure(a))), dictionary[state][c])])
        else:
            tmp[c] = ()
    #print(tmp[nfa.alpha[0]])
    return tmp
"""
def no_duplicates(values):
    return [v for v in {value:0 for value in values}]

def closure(state,transfer_function,been_to):
    if("" not in transfer_function[state]):
        return (state,)
    tmp = (state,)
    for states in transfer_function[state][""]:
        if(states not in been_to + list(tmp)):
            tmp += closure(states, transfer_function, been_to + list(tmp))
    return tuple(sorted(no_duplicates(tmp)))

    return tmp
def close_all(nfa, states):
    tmp = []
    for each in states:
        tmp = list(set(nfa.closure(each)) | set(tmp))
    return tmp

def generate_union_dict(dicts, alphabet):
    tmp = {}
    for char in alphabet:
        char_set = []
        for dictionary in dicts:
            if char in dictionary:
                char_set = list(set(char_set)|set(dictionary[char]))
        tmp[char] = tuple(char_set)
    return tmp
def get_all_tuples(dictionary):
    return [dictionary[k] for k in dictionary for char in dictionary[k]]


def compile(nfa: NFA) -> DFA:
    start_state = tuple(nfa.closure(nfa.start_s))
    states = [start_state]
    generated_states = []
    transfer_function = {}
    current_state = start_state
    trap_state = ''.join(choices("abcdefghijklmnopqrstuvwxyz",k=20))
    states.append(trap_state)
    generated_states.append(trap_state)
    transfer_function[trap_state] = {c: trap_state for c in nfa.alpha}
    current_state = states[0]
    while(len(generated_states) != len(states)):
        set_dict = []
        for state in current_state:
            tmp_inner_dict = {}
            inner_dict = nfa.transition[state]
            for character in nfa.alpha:
                if(character in inner_dict):
                    tmp_inner_dict[character] = close_all(nfa,inner_dict[character])
            set_dict.append(tmp_inner_dict)
        union_dict = generate_union_dict(set_dict,nfa.alpha)
        for char in nfa.alpha:
            if(char not in union_dict):
                union_dict[char] = trap_state
        transfer_function[current_state] = union_dict
        all_tuples = get_all_tuples(union_dict)
        states = list(set(states)|set(all_tuples))
        generated_states += [current_state]
        diffs = set(states) - set(generated_states)
        if(len(list(diffs)) != 0):
            current_state = list(diffs)[0]
    accepting = {state: nfa.any_accept(state) if state != trap_state else False for state in states}
    return DFA(states,nfa.alpha,transfer_function,start_state,accepting)

def fork_string(nfa,state,traces,string):
    current_dict = Tree()
    #print(string)
    if(len(string) != 0):
        #print(string)
        if string[0] in nfa.transition[state]:
            for states in nfa.transition[state][string[0]]:
                if(states not in traces):
                    val = fork_string(nfa,states,[],string[1:])
                    if(val != None):
                        current_dict[(states,nfa.accepting[states])] = val
                else:
                    current_dict[(states,nfa.accepting[states])] = "loopback"
    if "" in nfa.transition[state]:
        #print("\"\"")
        for states in nfa.transition[state][""]:
            if(states not in traces):
                val = fork_string(nfa,states,traces+[state],string)
                if(val != None):
                    current_dict[(states,nfa.accepting[states])] = val
            else:
                current_dict[(states,nfa.accepting[states])] = "loopback"
    if(len(current_dict) == 0 and len(string) == 0):
        return None
    if(len(current_dict) == 0):
        return "END"
    return current_dict
def DFS(nfa,state,traces):
    current_dict = Tree()
    for key in nfa.transition[state]:
        try:
            for states in nfa.transition[state][key]:
                if(states not in traces):
                    val = DFS(nfa,states,traces+[states])
                    current_dict[(states,nfa.accepting[states])] = val if val != None else {}
                else:
                    current_dict[(states,nfa.accepting[states])]="loopback"
        except:
            pass
    if(len(current_dict) != 0):
        return current_dict
    return None

# traces are for epsilon in this
def BackTrack(nfa,state,traces,string):
    if(string == ""):
        return nfa.accepting[state]
    #print(string[0])
    char = string[0]
    if char in nfa.transition[state]:
        for states in nfa.transition[state][char]:
            #print(BackTrack(nfa,states,[],string[1:]))
            if(BackTrack(nfa,states,[], string[1:])):
                return True
    if "" in nfa.transition[state]:
        for states in nfa.transition[state][""]:
            if states not in traces:
                if(BackTrack(nfa,states,traces + [states], string)):
                    return True
    return False

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
    Accepting_States={"initial":False,"nmod5=0":True,"nmod3=0":True,"initial":True,"nmod3=1":False,"nmod5=1":False,
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
    Alphabet="abcdefghijklmnopqrstuvwxyz0",
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
"""
    initialc->cOG->O->G
            ->cAT->cAT->cAT
    initialc->cAT->A->T
            ->cOG->cOG->cOG
"""
Fizz = NFA(
    States=["nmod3=0","nmod3=1","nmod3=2"],
    Alphabet="0",
    Transition_function={
        "nmod3=0":{"0":["nmod3=1"]},
        "nmod3=1":{"0":["nmod3=2"]},
        "nmod3=2":{"0":["nmod3=0"]}
    },
    Start_State="nmod3=0",
    Accepting_States={"nmod3=0":True,"nmod3=1":False,"nmod3=2":False}
)

Buzz = NFA(
    States=["nmod5=0","nmod5=1","nmod5=2","nmod5=3","nmod5=4"],
    Alphabet="0",
    Transition_function={
        "nmod5=0":{"0":["nmod5=1"]},
        "nmod5=1":{"0":["nmod5=2"]},
        "nmod5=2":{"0":["nmod5=3"]},
        "nmod5=3":{"0":["nmod5=4"]},
        "nmod5=4":{"0":["nmod5=0"]}
    },
    Start_State="nmod5=0",
    Accepting_States={"nmod5=0":True,"nmod5=1":False,"nmod5=2":False,"nmod5=3":False,"nmod5=4":False} 
)
doubleZero = NFA(
    States=["not0","0","00"],
    Alphabet="01",
    Transition_function={
        "not0":{"0":["0"],"1":["not0"]},
        "0":{"0":["00"],"1":["not0"]},
        "00":{}
    },
    Start_State="not0",
    Accepting_States={"00":True,"0":False,"not0":False}
)
doubleOne = NFA(
    States=["not1","1","11"],
    Alphabet="01",
    Transition_function={
        "not1":{"0":["not1"],"1":["1"]},
        "1":{"1":["11"],"0":["not1"]},
        "11":{}
    },
    Start_State="not1",
    Accepting_States={"not1":False,"1":False,"11":True}
)

FizzBuzzUnion = NFA(
    States=["","nmod5=0","nmod5=1","nmod5=2","nmod5=3","nmod5=4","nmod3=0","nmod3=1","nmod3=2"],
    Alphabet="0",
    Transition_function=
    {
        "":{"":["nmod3=0","nmod5=0"]},
        "nmod3=0":{"0":["nmod3=1"]},
        "nmod3=1":{"0":["nmod3=2"]},
        "nmod3=2":{"0":["nmod3=0"]},
        "nmod5=0":{"0":["nmod5=1"]},
        "nmod5=1":{"0":["nmod5=2"]},
        "nmod5=2":{"0":["nmod5=3"]},
        "nmod5=3":{"0":["nmod5=4"]},
        "nmod5=4":{"0":["nmod5=0"]}
    },
    Start_State="",
    Accepting_States={
        "":False,
        "nmod3=0":True,
        "nmod3=1":False,
        "nmod3=2":False,
        "nmod5=0":True,
        "nmod5=1":False,
        "nmod5=2":False,
        "nmod5=3":False,
        "nmod5=4":False
    }
)

ing=NFA(
    States=["initial","i","n","g"],
    Alphabet="abcdefghijklmnopqrstuvwxyz",
    Transition_function=
    {
        "initial":{a:["initial"] if a != "i" else ["i"] for a in "abcdefghijklmnopqrstuvwxyz"},
        "i":{"n":["n"]},
        "n":{"g":["g"]},
        "g":{}
    },
    Start_State="initial",
    Accepting_States={
        "initial":False,
        "i":False,
        "n":False,
        "g":True
    }
)


@decorate("FizzBuzzTest")
def FizzBuzzTest():
    assert FizzBuzz.backtrack("000"), "Returned False"
    assert not FizzBuzz.backtrack("0000"), "Returned True"
@decorate("doubleZeroTest")
def doublezerotest():
    assert doubleZero.backtrack("00"), "returned false"
    assert not doubleZero.backtrack("0"), "returned true"
@decorate("doubleOneTest")
def doubleonetest():
    assert doubleOne.backtrack("11"), "returned false"
    assert not doubleOne.backtrack("1"), "returned true"
@decorate("FizzBuzzUnion")
def fizzbuzzunion():
    assert FizzBuzzUnion.backtrack("000"),"returned false"
    assert not FizzBuzzUnion.backtrack("0000"),"returned true"
@decorate("ingTest")
def ingtest():
    assert ing.backtrack("ing"),"returned false"
    assert ing.backtrack("working"),"returned false"
@decorate("NfaSuite")
def nfasuite():
    FizzBuzzTest()
    doublezerotest()
    doubleonetest()
    fizzbuzzunion()
    ingtest()
@decorate("TreeTest")
def fork():
    assert (Fizz.tree() == 
        {("nmod3=0",True):
            {("nmod3=1",False):
                {("nmod3=2",False):
                    {("nmod3=0",True):
                        "loopback"
                    }
                }
            }
        }), "Trees dont match"
    assert (Buzz.tree() == 
        {("nmod5=0",True):
            {("nmod5=1",False):
                {("nmod5=2",False):
                    {("nmod5=3",False):
                        {("nmod5=4",False):
                            {("nmod5=0",True):
                                "loopback"
                            }
                        }
                    }
                }
            }
        }), "Tree dont match boi"
    assert True, "Didnt throw error"
    
@decorate("UnionTest")
def union():
    assert (Fizz | Buzz).backtrack("000"), "Says union not equal to hand written union"
@decorate("BackTrackTest")
def backtrack_test():
    assert FizzBuzz.backtrack("000"), "backtrack returned false"
    assert not FizzBuzz.backtrack("00"), "backtrack returned true"
@decorate("ConcatenateTest")
def concat_test():
    assert (doubleZero + doubleOne).backtrack("0011"), "returned false"
    assert not (doubleZero + doubleOne).backtrack("1100"), "returned true"
    assert not (doubleOne + doubleZero).backtrack("0011"), "returned false"
    assert (cogOrCat + FizzBuzz).backtrack("cat000"), "returned false"
    assert not (cogOrCat + FizzBuzz).backtrack("cat00"), "returned true"
    assert (cogOrCat + FizzBuzz).backtrack("cog000"), "returned false"
@decorate("ForkTest")
def fork_Test():
    assert (FizzBuzz.fork("000") == 
        {("initial",True):
            {("nmod3=1",False):
                {("nmod3=2",False):
                    "END"
                },
            ("nmod5=1",False):
                {("nmod5=2",False):
                    "END"
                }
            }
        }), "Fork not correct tree"
    assert (ing.fork("working") ==
        {("initial",False):
            {("initial",False):
                {("initial",False):
                    {("initial",False):
                        {("initial",False):
                            {("i",False):
                                {("n",False):"END"}
                            }
                        }
                    }
                }
            }
        }),"not matching"


@decorate("CompileEdges")
def compile_edges():
    compile(FizzBuzz)
    compile(ing)
    compile(Fizz)
    compile(Buzz)

@decorate("Compile")
def compile_test():
    assert FizzBuzz.compile().iterate_DFA("000"), "Returned False when it shouldnt have"
    assert not FizzBuzz.compile().iterate_DFA("0000"), "Returned True"
@decorate("CompileSuite")
def compile_suite():
    compile_edges()
    compile_test()

@decorate("NFACompairsonToDFA")
def tester():
#    print(FizzBuzz.compile().SS)
    d = [("initial",),("nmod3=1","nmod5=1"),("nmod3=2","nmod5=2"),("nmod3=0","nmod5=3"),("nmod3=1","nmod5=4"),("nmod3=2","nmod5=0"),("nmod3=0","nmod5=1"),("nmod3=1","nmod5=2"),("nmod3=2","nmod5=3"),("nmod3=0","nmod5=4"),("nmod3=1","nmod5=0"),("nmod3=2","nmod5=1"),("nmod3=0","nmod5=2"),("nmod3=1","nmod5=3"),("nmod3=2","nmod5=4"),("nmod3=0","nmod5=0")]
    tf = {
        ("initial",):{"0":("nmod3=1","nmod5=1")},
        ("nmod3=1","nmod5=1"):{"0":("nmod3=2","nmod5=2")},
        ("nmod3=2","nmod5=2"):{"0":("nmod3=0","nmod5=3")},
        ("nmod3=0","nmod5=3"):{"0":("nmod3=1","nmod5=4")},
        ("nmod3=1","nmod5=4"):{"0":("nmod3=2","nmod5=0")},
        ("nmod3=2","nmod5=0"):{"0":("nmod3=0","nmod5=1")},
        ("nmod3=0","nmod5=1"):{"0":("nmod3=1","nmod5=2")},
        ("nmod3=1","nmod5=2"):{"0":("nmod3=2","nmod5=3")},
        ("nmod3=2","nmod5=3"):{"0":("nmod3=0","nmod5=4")},
        ("nmod3=0","nmod5=4"):{"0":("nmod3=1","nmod5=0")},
        ("nmod3=1","nmod5=0"):{"0":("nmod3=2","nmod5=1")},
        ("nmod3=2","nmod5=1"):{"0":("nmod3=0","nmod5=2")},
        ("nmod3=0","nmod5=2"):{"0":("nmod3=1","nmod5=3")},
        ("nmod3=1","nmod5=3"):{"0":("nmod3=2","nmod5=4")},
        ("nmod3=2","nmod5=4"):{"0":("nmod3=0","nmod5=0")},
        ("nmod3=0","nmod5=0"):{"0":("nmod3=1","nmod5=1")}
    }
    accepting = {
        ("initial",):True,
        ("nmod3=1","nmod5=1"):False,
        ("nmod3=2","nmod5=2"):False,
        ("nmod3=0","nmod5=3"):True,
        ("nmod3=1","nmod5=4"):False,
        ("nmod3=2","nmod5=0"):True,
        ("nmod3=0","nmod5=1"):True,
        ("nmod3=1","nmod5=2"):False,
        ("nmod3=2","nmod5=3"):False,
        ("nmod3=0","nmod5=4"):True,
        ("nmod3=1","nmod5=0"):True,
        ("nmod3=2","nmod5=1"):False,
        ("nmod3=0","nmod5=2"):True,
        ("nmod3=1","nmod5=3"):False,
        ("nmod3=2","nmod5=4"):False,
        ("nmod3=0","nmod5=0"):True
    }
    D = DFA(d,"0",tf,d[0],accepting)
    v = FizzBuzz.compile()
    assert D == v,  "D did not equal v"
@decorate("TestSuite",True)
def test_suite():
    nfasuite()
    fork()
    union()
    backtrack_test()
    concat_test()
    fork_Test()
    compile_suite()
    tester()
test_suite()

