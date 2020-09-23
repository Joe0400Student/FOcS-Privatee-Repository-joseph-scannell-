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

node = generate_double_0_1()

test_cases = [
	"0010110010", #should fail as it goes 10 at end
		      #begin->0_1->0_2->1_1->0_1->1_1->1_2->0_1->0_2->1_1->0_1
	"001100", #should work as it goes 00 at end
		#begin->0_1->0_2->1_1->1_2->0_1->0_2
	"11011", #should work as it end 11
	"11010", #should fail it end 10
	"1", #should fail single digit
	"11" #should work as its 11
]

for test in test_cases:
	test_node = node
	for c in test:
		test_node = test_node.next(c)
	print(test + " = " + str(test_node.accepting()))

