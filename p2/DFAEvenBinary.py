from DFA import DFA


def make_even_dfa():
	alpha = '01'
	
	even = DFA(True)
	odd = DFA(False)
	even.add_next_table({'0':even,'1':odd})
	odd.add_next_table({'0':odd,'1':even})
	return even

test_cases = [
	"011010011", # should be false as there is a odd number of zeros
		     # even->odd->even->even->odd->odd->odd->even->odd"
	"1", #should be false as it contains 1 1 character
		#even->odd
	"11", #should be true"
	"00", #should be true"
	"101", #should be true"
	"111", #should be false
	"10", #should be false
	"110", #should be true"
	"10110", #should be false
	"1010", #should be true
	"10101100", #should be true
	"10101000" #should be false
]

node = make_even_dfa()

for test in test_cases:
	test_node = node
	for c in test:
		test_node = test_node.next(c)
	print(test + " = " + str(test_node.accepting()))

