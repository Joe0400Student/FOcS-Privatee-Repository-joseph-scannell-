from DFA import DFA


def generate_dfa_for_even_length(a):
	dfa1 = DFA(True)
	dfa2 = DFA(False)
	dfa1.add_next_table({g: dfa2 for g in a})
	dfa2.add_next_table({g: dfa1 for g in a})
	return dfa1

node = generate_dfa_for_even_length("abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ ;:'\"\\[]{},.<>/?!@#$%^&*()-=_+`~")

test_cases = [
	"even", #should be true, as it is even length
		#even->odd->even->odd->even
	"odd",  #should be false, as it is odd length
		#even->odd->even->odd
	"rough", #should be false
	"True", #should be true
	"false", #should be false
	"rand", #should be true
]

for test in test_cases:
	test_node = node
	for c in test:
		test_node = test_node.next(c)
	print(test + " = " + str(test_node.accepting()))

