from DFA import DFA

def dfa_kword():
	begin = DFA(False)
	alphabet = "abcdefghijklmnopqrstuvwxyz "
	d = DFA(False)
	e = DFA(False)
	f = DFA(True)
	contains = DFA(True)
	hold_loop = DFA(False)
	
	begin.add_next_table({c:d if c == "d" else hold_loop if c != " " else begin for a in alphabet})
	hold_loop.add_next_table({c:hold_loop if c != " " else begin for c in alphabet})
	d.add_next_table({c:e if c == "e" else hold_loop if c != " " else begin for a in alphabet})
	e.add_next_table({c:f if c == "f" else hold_loop if c != " " else begin for a in alphabet})
	f.add_next_table({c:hold_loop if c != " " else contains for a in alphabet})

	return begin

