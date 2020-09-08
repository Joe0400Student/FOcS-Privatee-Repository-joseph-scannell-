from DFA import DFA
from char import char
from str import string
from alphabet import alphabet

def generate_dfa_of_char(c: char, a: alphabet):{
    
    DFA1 = DFA(False)
    DFA2 = DFA(True)
    DFA3 = DFA(False)
    DFA1.add_next_table({g: DFA2 if g == c else DFA3 for g in a})
    DFA2.add_next_table({g: DFA3 for g in a})
    DFA3.add_next_table({g: DFA3 for g in a})
    return [DFA1,DFA2,DFA3]
    

