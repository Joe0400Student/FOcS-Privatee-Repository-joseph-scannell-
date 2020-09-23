from DFA import DFA

def dfa_int():
	alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-+=(){}[];:\\ ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	
	begin = DFA(False)
	holding = DFA(False)
	accept = DFA(True)
	
	i = DFA(False)
	n = DFA(False)
	t = DFA(True)
	
	begin.add_next_table({c: i if c == 'i' else holding if c != ' ' else begin for c in alphabet})
	holding.add_next_table({c: begin if c == ' ' else holding for c in alphabet for c in alphabet})
	i.add_next_table({c: n if c == 'n' else holding if c != ' ' else begin for c in alphabet})
	n.add_next_table({c: t if c == 't' else holding if c != ' ' else begin for c in alphabet})
	t.add_next_table({c: holding if c != ' ' else accept for c in alphabet})
	accept.add_next_table({c: accept for c in alphabet})
	
	return begin
	

node = dfa_int()

test_cases = [
	"int", #should work, as it contains int seperate from other
	       #begin->i->n->t
	"intt", #should fail"
	"class Integer{ private: int a; public: Integer(int t=0): a(t) {} operator int(){ return a;}}", #should work as it contains a int as a field
	"int()", #should fail, function"
	"int a", #should work, int type
	"integers are a type of number", #should fail 
	"public static void main(){}" #should fail
]

for test in test_cases:
	test_node = node
	for c in test:
		test_node = test_node.next(c)
	print(test + " = " + str(test_node.accepting()))
