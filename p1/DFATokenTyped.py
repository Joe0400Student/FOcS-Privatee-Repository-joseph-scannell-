from char import char
from alphabet import alphabet
from str import string
from DFA import DFA

def generate_int_dfa(a: alphabet):
	
	dfa1 = DFA(False)
	dfa2 = DFA(False)
	dfa2.add_next_table({g: dfa1 if g == char(' ') else dfa2 for g in a})
	
	dfaA_after_space = DFA(True)
	dfaA_after_space.add_next_table({g: dfaA_after_space for g in a})


	dfai1 = DFA(False)
	dfai2 = DFA(False)
	dfai3 = DFA(True)
	dfai1.add_next_table({g: dfai2 if g == char('n') else dfa2 for g in a})
	dfai2.add_next_table({g: dfai3 if g == char('t') else dfa2 for g in a})
	dfai3.add_next_table({g: dfaA_after_space if g == char(' ') or g == char('\n') or g == char('\t') else dfa2 for g in a})
	
	dfa1.add_next_table({g: dfai1 if g == char('i') else dfa2 if not g == char(' ') and not g == char('\n') and not g == char('\t') else dfa1 for g in a})
	
	return dfa1
	

while(True):
	a = input()
	
	dfa_node = generate_int_dfa(alphabet([char(chr(i)) for i in range(0,256)]))
	
	for g in a:
		dfa_node = dfa_node.next(char(g))
	
	print(dfa_node.accepting())

