from regex import *
from time import time

print("begin_stress")
start = time()
pattern = PatternBuilder("*|0123456789abcdefghijklmnopqrstuvwxyz]").compile()
compiled = 0
while(True):
    print(f"{compiled}")
    pattern.compile()
    compiled += 1
    if(compiled > 10):
        tmp = time()
        print(f"{(tmp - start)/10}")
        start = tmp
        compiled = 0
