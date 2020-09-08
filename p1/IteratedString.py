from str import string
from char import char
from itertools import product
import time

'''
main_alpha = string() + char('0') + char('1')
'''
class IterateString:
    def __init__(self, alphabet):
        self.alpha = alphabet
    def __iter__(self):
        self.N = 0
        self.l = []
        return self

    def __next__(self):
        if(len(self.l) == 0):
            for c in product(self.alpha, repeat=self.N):
                s = string()
                for g in c:
                    s = s + g
                self.l.append(s)
            self.N += 1
        s = self.l[0]
        self.l = self.l[1:]
        return s
'''
test
for g in IterateString(main_alpha):
    print(g)
'''
