from NFA import NFA
import string

from random import choices

class Regex:
    
    def __init__(self,empty=None,epsilon=None,char=None,union=None,star=None,circ=None):
        if(empty != None):
            self.empty = empty
            self.type = 0
        elif(epsilon != None):
            self.epsilon = epsilon
            self.type = 1
        elif(char != None):
            self.char = char
            self.type = 2
        elif(union != None):
            self.union = union
            self.type = 3
        elif(star != None):
            self.star = star
            self.type = 4
        elif(circ != None):
            self.circ = crc
            self.type = 5
    
    
    def __repr__(self):
        if(self.type == 0):
            return "∅"
        elif(self.type == 1):
            return "ϵ"
        elif(self.type == 2):
            return self.char
        elif(self.type == 3):
            return f"({self.char[0].__repr__()}) | ({self.char[1].__repr__()})"
        elif(self.type == 4):
            return f"({self.star.__repr__()})*"
        elif(self.type == 5):
            return f"({self.circ[0].__repr__()})⚬({self.cric[1].__repr__()})"
    
    def compile(self):
        if(self.type == 0):
            name = choices("abcdefghijklmnopqrstuvwxyz",k=20)
            return NFA(
                States=[name],
                Alphabet=string.printable,
                Transition_function={name:{}},
                Start_State=name,
                Accepting_States={name:False}
            )
        elif(self.type == 1):
            name = choices("abcdefghijklmnopqrstuvwxyz",k=20)
            name2 = choices("abcdefghijklmnopqrstuvwxyz",k=20)
            return NFA(
                States=[name,name2],
                Alphabet=string.printable,
                Transition_function={name:{c:name2 for c in string.printable},name2:{}},
                Start_State=name,
                Accepting_States={name:True,name2:False}
            )
        elif(self.type == 2):
            name = choices("abcdefghijklmnopqrstuvwxyz",k=20)
            name2 = choices("abcdefghijklmnopqrstuvwxyz",k=20)
            name3 = choices("abcdefghijklmnopqrstuvwxyz",k=20)
            return NFA(
                States=[name,name2,name3],
                Alphabet=string.printable,
                Transition_function={
                                        name:{self.char:name2},
                                        name2:{c:name3 for c in string.printable},
                                        name3:{}
                },
                Start_State = name,
                Accepting_States={name:False,name2:True,name3:False}
            )
        elif(self.type == 3):
            return self.union[0].compile() | self.union[1].compile()
        elif(self.type == 4):
            return self.star[0].compile().kleene_star()
        else
            return self.circ[0].compile() + self.circ[1].compile()


