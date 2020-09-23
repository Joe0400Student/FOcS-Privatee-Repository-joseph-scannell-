from DFA import DFA
from char import char
from str import string
from alphabet import alphabet

def generate_dfa_for_even_length(a: alphabet):
	dfa1 = DFA(True)
	dfa2 = DFA(False)
	dfa1.add_next_table({g: dfa2 for g in a})
	dfa2.add_next_table({g: dfa1 for g in a})
	return dfa1


