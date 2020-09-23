from DFA import DFA

def generate_double_0_1():
	begin = DFA(False)
	one_first = DFA(False)
	one_second = DFA(True)
	zero_first = DFA(False)
	zero_second = DFA(True)
	begin.add_next_table({'0':zero_first,'1':one_first})
	one_first.add_next_table({'0':zero_first,'1':one_second})
	one_second.add_next_table({'0':zero_first,'1':one_second})
	zero_first.add_next_table({'0':zero_second,'1':one_first})
	zero_second.add_next_table({'0':zero_second,'1':one_first})
	return begin

