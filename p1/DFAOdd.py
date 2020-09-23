from DFA import DFA

def dfa_odd():
	alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789[]{};\"'\\|,<.>/?"
	even = DFA(False)
	odd = DFA(True)
	even.add_next_table({a: odd for a in alphabet})
	odd.add_next_table({a: even for a in alphabet})
	return even

test_cases = [
	"a", #returns true even->odd
	"", #returns false even
	"   ", #returns true even->odd->even->odd
	"odd", #returns true 
	"false", #returns true
	"even", #returns false
	"toyota", #returns false
	"nissan", #returns false
	"yorha" #returns true
]
node = dfa_odd()

for test in test_cases:
	test_node = node
	for c in test:
		test_node = test_node.next(c)
	print(test + " = " + str(test_node.accepting()))

