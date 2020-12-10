from NFA import *
from string import printable
import random
from DFA import *
from string import ascii_uppercase as upper_case

WHOLE_ASCII = printable



def generate_random_name() -> str: return ''.join(random.choices(WHOLE_ASCII,k=20))

class Regex:

    def __repr__(self):
        pass

    def compile(self):
        pass

    def test(self, other):
        return compile(self.compile()) == compile(other.compile())
    
    def generate(self):
        return DFS((v := self.compile()),v.SS,[],[])


class RegexEpsilon(Regex):

    def __init__(self):
        pass
    def compile(self):
        n1, n2 = generate_random_name(), generate_random_name()
        return NFA(
            States=[n1,n2],
            Alphabet=WHOLE_ASCII,
            Start_State=n1,
            Transition_function={
                        n1:{a : [n1] for a in WHOLE_ASCII},
                        n2:{}
                      },
            Accepting_States={n1:True,n2:False}
        )
    
    def __repr__(self):
        return "epsilon"


class RegexEmpty(Regex):

    def __init__(self):
        pass
    
    def compile(self):
        n1 = generate_random_name()
        return NFA(
            States=[n1],
            Alphabet=WHOLE_ASCII,
            Start_State=n1,
            Transition_function={n1:{}},
            Accepting_States={n1:False},
        )
    def __repr__(self):
        return "Empty"

class RegexChar(Regex):
    def __init__(self,character):
        self.character = character
    
    def compile(self):
        n1, n2, n3 = generate_random_name(), generate_random_name(), generate_random_name()
        return NFA(
            States=[n1,n2,n3],
            Alphabet=WHOLE_ASCII,
            Start_State=n1,
            Transition_function={
                        n1:{a: [n2] if a == self.character else [n3] for a in WHOLE_ASCII},
                        n2:{a: [n3] for a in WHOLE_ASCII},
                        n3:{}
            },
            Accepting_States={n1:False,n2:True,n3:False}
        )
    def __repr__(self):
        return self.character

class RegexUnion(Regex):

    def __init__(self,a,b):
        self.a, self.b = a, b

    def compile(self):
        return self.a.compile() | self.b.compile()

    def __repr__(self):
        return f"({self.a.__repr__()})∪({self.b.__repr__()})"

class RegexStar(Regex):

    def __init__(self,a):
        self.a = a 
    
    def compile(self):
        return self.a.compile().kleene_star()

    def __repr__(self):
        return f"({self.a.__repr__()})*"

class RegexConcat(Regex):

    def __init__(self,a,b):
        self.a, self.b = a,b
    
    def compile(self):
        return self.a.compile() + self.b.compile()
    
    def __repr__(self):
        return f"({self.a.__repr__()})⚬({self.b.__repr__()})"

#regex_thing = RegexUnion(RegexConcat(RegexConcat(RegexChar(a),RegexChar(b)),RegexChar(c)),
 #               RegexConcat(RegexConcat(RegexChar(c),RegexChar(b)),RegexChar(a)))

def generate_alphabet_regex():
    current_Regex = RegexEpsilon()
    for c in string.ascii_letters:
        current_Regex = RegexUnion(current_Regex,RegexChar(c))
    return current_Regex


def PatternBuilder(string) -> Regex:
    string = string.__iter__()
    if((val := string.__next__()) == "("):
        return MakeConcat(string)
    elif(val == "|"):
        return MakeUnion(string)
    elif(val == "*"):
        return MakeStar(string)


def MakeUnion(string) -> Regex:
    current_regex = RegexEmpty()
    while((value := string.__next__()) != "]"):
        if(value == "("):
            current_regex = RegexUnion(
                MakeConcat(string),
                current_regex
            )
        elif(value == "|"):
            current_regex = RegexUnion(
                MakeUnion(string),
                current_regex
            )
        elif(value == "*"):
            current_regex = RegexUnion(
                MakeStar(string),
                current_regex
            )
        else:
            current_regex = RegexUnion(
                current_regex,
                RegexChar(value)
            )
    return current_regex


def MakeConcat(string) -> Regex:
    regex_stack = []
    while((value := string.__next__()) != "]"):
        if(value == "("):
            regex_stack.append(MakeConcat(string))
        elif(value == "|"):
            regex_stack.append(MakeUnion(string))
        elif(value == "*"):
            regex_stack.append(MakeStar(string))
        else:
            regex_stack.append(RegexChar(value))
    value = RegexConcat(regex_stack[-2],regex_stack[-1])
    regex_stack = regex_stack[:-2]
    while(len(regex_stack)):
        value = RegexConcat(regex_stack[-1],value)
        regex_stack = regex_stack[:-1]
    return value
def MakeStar(string) -> Regex:
    if((value := string.__next__()) == "("):
        return RegexStar(MakeConcat(string))
    elif(value == "|"):
        return RegexStar(MakeUnion(string))
    elif(value == "*"):
        return RegexStar(MakeStar(string))


tmp = PatternBuilder("*|abcdxyz]")
#compiled = tmp.compile().compile()
#print(str(tmp))
#while(True):
#   print(PatternBuilder("(ab]").compile().compile().iterate_DFA(input()))
#   print(compiled.iterate_DFA(input()))


any_lower = PatternBuilder("|abcdefghijklmnopqrstuvwxyz]")
any_digit = PatternBuilder("|0123456789]")
any_numeric = RegexStar(any_digit)
any_upper = PatternBuilder(f"|{upper_case}]")

#print(any_lower.compile().compile().iterate_DFA(input("lower case: ")))
#print(any_digit.compile().compile().iterate_DFA(input("digit: ")))
#print(any_numeric.compile().compile().iterate_DFA(input("any number: ")))
#print(any_upper.compile().compile().iterate_DFA(input("any upper: ")))
#print(PatternBuilder("(*|01]|(00](11]]]").compile().compile().iterate_DFA("010011"))
"""print(DFS((tmp:=RegexConcat(
    RegexStar(
        RegexUnion(
            RegexChar("0"),
            RegexChar("1")
        )
    ),
    RegexUnion(
        RegexConcat(
            RegexChar("1"),
            RegexChar("1")
        ),
        RegexConcat(
            RegexChar("."),
            RegexChar(".")
        )
    )
).compile().compile()),tmp.SS,[],[]))
"""

#v = (PatternBuilder(f"*|(ing](ly]]").compile().compile())
#print("compiled")
#print(v.iterate_DFA(input()))

@decorate("KleinTest")
def klein_test():
    """
    first is any length 0 character
    second is a string completely consisting of 1001
    third is a string that follows the fizz buzz property
    """
    n_0s = PatternBuilder("*|0]").compile().compile()
    n_1s = PatternBuilder("*|(10](01]]").compile().compile()
    n_2s = PatternBuilder("|*(000]*(00000]]").compile().compile()
    assert n_0s.iterate_DFA("0"), "returned false"
    assert not n_0s.iterate_DFA("1"), "returned true"
    assert n_1s.iterate_DFA("1001"), "retuned false"
@decorate("TestCompiler")
def compiler_test():
    klein_test()

@decorate("Equality_Tester")
def equality_checker():
    assert not PatternBuilder("*|(10](01]]").test(PatternBuilder("|0]")), " Returned True"
    assert not PatternBuilder("*(abc]").test(PatternBuilder("(abc]")), "Returned True"
@decorate("LargePatternCompiler")
def largest_pattern():
    email_tester = PatternBuilder("(|abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVXYZ]*|abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ]@|abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ]*|abcdefghijklmnopqrstuvxwyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789].|(com](org](gov]]]").compile().compile()
    assert (None != DFS(email_tester,email_tester.SS,[],[])), "Returned None, no possible regex pattern"

#print("compiled")
#print(email_tester.iterate_DFA(input("enter a email address here!: ")))
@decorate("RegexTestSuite",True)
def regex_test_suite():
    compiler_test()
    equality_checker()
    largest_pattern()
regex_test_suite()
