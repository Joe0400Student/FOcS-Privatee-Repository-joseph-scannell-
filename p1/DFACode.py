from char import char
from alphabet import alphabet
from str import string
from DFA import DFA


#for c style comments only
def currently_commented_out(a: alphabet):
	
	dfa1 = DFA(True)
	dfa2 = DFA(True)
	dfa3 = DFA(False)

	dfa1.add_next_table({g:dfa1 if not g == char("/")  else dfa2 for g in a})
	dfa2.add_next_table({g:dfa1 if not g == char("/")  else dfa3 for g in a})
	dfa3.add_next_table({g:dfa3 if not g == char("\n") else dfa1 for g in a})
	
	return dfa

