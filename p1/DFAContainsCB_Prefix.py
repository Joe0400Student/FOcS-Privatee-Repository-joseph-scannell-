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
	c.add_next_table({c: B if c == "b" else C if c == "c" else begin for c in hexadecimal})
	b.add_next_table({c: B for c in hexadecimal})
	return begin

