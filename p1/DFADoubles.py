from DFA import DFA
import copy

def gen_double(alphabet):
  begin_node = DFA(False)
  end_node = DFA(True)
  dictionary = {}
  for each in alphabet:
    temp_node = DFA(False)
    dictionary[each] = temp_node
  for each in alphabet:
    new_dict = {c:end_node if c == each else dictionary[c] for c in alphabet}
    dictionary[each].add_next_table(new_dict)
  begin_node.add_next_table(dictionary)
  end_node.add_next_table({e: end_node for e in alphabet})
  return begin_node

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ;:'\"[]{}\|`1234567890-=~!@#$%^&*()_+,./<>? "

node = gen_double(alphabet)

test_cases = [
	"aa", # works
	      # begin -> a_character -> end_state
	"ab", #fails
	      # begin -> a_character -> b_character
	"i like to eat steak", # fails
	"the speedy car drives quickly", # accepts
	"tooling is expensive for manufacturing", #accepts
	"toyota mr2", #fails
	"food is good", #accepts
	"oo is a double o", #accepts
	"you hear wee from a roller coaster", #accepts
	"great things start slowly", #fails
	"DFAs are fun", #fails
	"it is simple and effective" #fails
]

for test in test_cases:
	test_node = node
	for c in test:
		test_node = test_node.next(c)
	print(test + " = " + str(test_node.accepting()))

