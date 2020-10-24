from DFA import DFA

# the CB prefix is used in gameboy emulation to show different prefix operators. (All bitwise
# operators)
# see https://www.pastraiser.com/cpu/gameboy/gameboy_opcodes.html for more info

def contains_cb_prefix():
	hexadecimal = "0123456789abcdef"
	begin = DFA(False)
	C = DFA(False)
	B = DFA(True)
	begin.add_next_table({c: C if c == "c" else begin for c in hexadecimal})
	C.add_next_table({c: B if c == "b" else C if c == "c" else begin for c in hexadecimal})
	B.add_next_table({c: B for c in hexadecimal})
	return begin

node = contains_cb_prefix()

test_cases = [
	"cb", # works cause it is the CB prefix on its own
	      # begin->c_state->b_state
	"deadbeef", # shouldnt work as it doesnt contain cb
		    # begin->begin->begin...->begin
	"cb00", # should work, as it contains cb
	"ccb", # should work as it contains cb 
	"0010213012340891234980ccadfc", # shouldnt work as it contains no cb
	"0000", #shouldnt work as it doesnt contains cb
	"abcd", #shouldnt work as it doesnt contains cb
	"ffff", #shouldnt work as it dosent contain cb
	"", #shoulndt as no cb prefix
	"bccb", #should as it contains a cb prefix"
	"bbcb", #should as it contains a cb prefix"
	"cbcb" #should as it contains a cb prefix
]
for test in test_cases:
	test_node = node
	for characters in test:
		test_node = test_node.next(characters)
	print(test + " = " + str(test_node.accepting()))
