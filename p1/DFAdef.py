from DFA import DFA

def dfa_kword():
	begin = DFA(False)
	alphabet = "abcdefghijklmnopqrstuvwxyz()_-,.:{}*[]=+-;*/ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789"
	d = DFA(False)
	e = DFA(False)
	f = DFA(True)
	contains = DFA(True)
	hold_loop = DFA(False)
	begin.add_next_table({c:d if c == "d" else hold_loop if c != " " else begin for c in alphabet})
	hold_loop.add_next_table({c:hold_loop if c != " " else begin for c in alphabet})
	d.add_next_table({c:e if c == "e" else hold_loop if c != " " else begin for c in alphabet})
	e.add_next_table({c:f if c == "f" else hold_loop if c != " " else begin for c in alphabet})
	f.add_next_table({c:hold_loop if c != " " else contains for c in alphabet})
	contains.add_next_table({c:contains for c in alphabet})
	return begin

test_cases = [
	"def function():", #should work as it contains def
			   # begin->d->e->f->accepting_hold->...->accepting->hold
	"deffer", #shouldnt as it has a character continuing it has a character that breaks kword
		  #begin->d->e->f->hold_failure->...->hold_failure
	"class A(inherits_from): def __init__(self, parameter: type): self.parameter = parameter",
		#should as it contains a def command between spaces
	"def __mul__(self,other):",
		#should as it contains def between spaces"
	"int main(int argv, char* argc[]){ return 0;}",
		#shouldnt as it doesnt contain a def between spaces"
	"class test{ public static void main(int argv, String argc[]){ do_something();} }",
		#shouldnt as it doesnt contain a def kword"
	"the keyword for define class-functions or methods in python is def"
		#should as it contains a def kword"
]

node_begin = dfa_kword()
for test in test_cases:
	test_node = node_begin
	for a in test:
		test_node = test_node.next(a)
	print(test + " = " + str(test_node.accepting()))
