from alphabet import alphabet
from char import char
from str import string
import math

def find_n(a: alphabet, n: int) -> string:
    
    depth = math.floor(math.log(n+1,len(a)))
    n -= len(a) ** depth - 1
    s = string()
    for pos in range(depth-1,-1,-1):
        s = s + a.chars[math.floor(n / len(a)**pos)]
        n = n % len(a)**pos
    return s
    
for i in range(11):
    print(i,end=":")
    print(find_n(alphabet([char('0'),char('1')]),i))

