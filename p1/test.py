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

a = input("enter string")

alpha = "abcdefghijklmnopqrstuvwxyz"

dfa_start = gen_double(alpha)

for c in a:
	dfa_start = dfa_start.next(c)

print(dfa_start.accepting())

