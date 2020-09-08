from DFA import DFA
from char import char
from IteratedString import IterateString

alphabet = [char('0'),char('1')]

begin = DFA(False)
begin.add_next_table({letter: begin for letter in alphabet})

for each in IterateString(alphabet):
    cur_state = begin
    for c in each:
        cur_state = cur_state.next(c)
    print(cur_state.accepting(), end = (each+char("\n")).__repr__())

