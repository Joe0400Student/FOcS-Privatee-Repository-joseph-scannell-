from DFA import DFA

def DFA_Tester(DFA_node, string):
	for c in string:
		DFA_node = DFA_node.next(c)
	return DFA_node.accepting()
print("--------------------------------------")
print("ContainsCB_Prefix_tests")
print("--------------------------------------")
import DFAContainsCB_Prefix
print("--------------------------------------")
print("TesterFunction")
print("--------------------------------------")

for test in DFAContainsCB_Prefix.test_cases:
	print(test + " = " + str(DFA_Tester(
		DFAContainsCB_Prefix.contains_cb_prefix(),
		test)))



print("\n\n\n\n\n")
print("--------------------------------------")
print("DFADef")
print("---------------------------------------")

import DFAdef
print("--------------------------------------")
print("TesterFUnction")
print("---------------------------------------")

for test in DFAdef.test_cases:
        print(test + " = " + str(DFA_Tester(
                DFAdef.dfa_kword(),
                test)))

print("\n\n\n\n\n")
print("--------------------------------------")
print("DFAdouble01end")
print("--------------------------------------")
import DFAdouble01end
print("--------------------------------------")
print("testerfunction")
print("_---------------------------------------")

for test in DFAdouble01end.test_cases:
	print(test + " = " + str(DFA_Tester(DFAdouble01end.generate_double_0_1(),test)))

print("\n\n\n\n\n")
print("--------------------------------------")
print("DFADoubles")
print("--------------------------------------")
import DFADoubles
print("--------------------------------------")
print("Testerfunction")
print("---------------------------------------")

for test in DFADoubles.test_cases:
	print(test + " = " + str(DFA_Tester(DFADoubles.gen_double(DFADoubles.alphabet),test)))

print("\n\n\n\n\n")
print("--------------------------------------")
print("DFAEvenBinary")
print("--------------------------------------")
import DFAEvenBinary
print("--------------------------------------")
print("Testerfunction")
print("--------------------------------------")
for test in DFAEvenBinary.test_cases:
	print(test + " = " + str(DFA_Tester(DFAEvenBinary.make_even_dfa(),test)))


print("\n\n\n\n\n")
print("--------------------------------------")
print("DFAEven")
print("-------------------------------------")
import DFAEven
print("-------------------------------------")
print("TesterFunction")
print("--------------------------------------")
for test in DFAEven.test_cases:
	print(test + " = " + str(DFA_Tester(DFAEven.generate_dfa_for_even_length(DFAEven.alphabet),test)))

print("\n\n\n\n\n")
print("--------------------------------------")
print("DFAint")
print("--------------------------------------")
import DFAint
print("--------------------------------------")
print("TesterFunction")
print("--------------------------------------")
for test in DFAint.test_cases:
	print(test + " = " + str(DFA_Tester(DFAint.dfa_int(),test)))

print("\n\n\n\n\n")
print("--------------------------------------")
print("DFAOdd")
print("--------------------------------------")
import DFAOdd
print("--------------------------------------")
print("TesterFunction")
print("--------------------------------------")
for test in DFAOdd.test_cases:
	print(test + " = " + str(DFA_Tester(DFAOdd.dfa_odd(),test)))

