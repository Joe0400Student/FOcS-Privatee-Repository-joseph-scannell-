from regex import Regex
from NFA import NFA
from random import choices

class GNFA:
    
    def __init__(self,Q, Sigma, SS, QE, Delta):
        self.Q = Q
        self.Sigma = Sigma
        self.SS = SS
        self.QE = QE
        self.Detla = Delta
    
    def start(nfa: NFA):
        QS = choices("abcdefghijklmnopqrstuvwxyz",k=20)
        QE = choices("abcdefghijklmnopqrstuvwxyz",k=20)
        Q = list(set(nfa.states) | set([QS,QE]))
        Delta = {
                    (QS, nfa.start_s): Regex(epsilon=[])
                }
        for key in nfa.states:
            if(key != nfa.start_s):
                Delta[(QS,key)] = Regex(empty=[])
            if(nfa.accepting[key]):
                Delta[(key,QE)] = Regex(epsilon=[])
            else:
                Delta[(key,QE)] = Regex(emtpy=[])
        for key in nfa.states:
            for c in nfa.transtion[key]:
                Delta((key,nfa.transition[key][c]) = Regex(union=[Regex(c),nfa.transition[key][c]])
        return GNFA(Q,self.alpha,QS,QE,Delta)
    
    def rip(self):
        Q = self.Q
        Sigma = self.Sigma
        SS = self.SS
        QE = self.QE
        Delta = self.Delta
        
        single_r = Delta[0]
        
        
    def end(self):
        
