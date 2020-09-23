from DFA import DFA

def DFA_Tester(DFA_node, string)
	for c in string:
		DFA_node = DFA_node.next(c)
	return DFA_node.accepting()

