from DFA import DFA
from char import char
from alphabet import alphabet

def make_even_dfa():
	alpha = alphabet([char('0'),char('1')])
	
	dfa1 = DFA(True)
	dfa2 = DFA(False)
	dfa1.add_next_table({char('0'):dfa1,char('1'):dfa2})
	dfa2.add_next_table({char('0'):dfa1,char('1'):dfa2})
	return dfa1

