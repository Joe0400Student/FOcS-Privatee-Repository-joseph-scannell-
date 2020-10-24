from DFA import DFA
from char import char
from alphabet import alphabet
from IteratedString import IterateString

DFA_Node1 = DFA(True)
DFA_Node2 = DFA(False)

alpha = alphabet([char('0'),char('1')])

DFA_Node1.add_next_table({c: DFA_Node2 for c in alpha})
DFA_Node2.add_next_table({c: DFA_Node2 for c in alpha})

for each in IterateString(alpha):
    cur_node = DFA_Node1
    for c in each:
        cur_node = cur_node.next(c)
    print(each,end=" ")
    print(cur_node.accepting())
    input()

