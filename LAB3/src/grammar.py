import copy
import pprint

empty_string = "`"

class Grammar:
    """Class that holds a grammar"""
    #TODO: Add more error handling
    def __init__(self, T, N, P, S, verbose = False):
        self.T = set(T)        
        if "\\e" in self.T:
            self.T -= {"\\e"}
            self.T |= {"`"}
            print self.T
        self.N = set(N)
        self.P = self.parse_rules(P)
        self.verbose = verbose;
        self.S = S 
        self.type = "undefined"
        if(verbose):
            print self        
        
    def parse_rule(self, rule):
        """
        Parse a grammar rule and return a tuple: 
        a starting symbol and a list of end symbols
        """
        rule = "".join(rule.split())
        rule = rule.replace("||", "|"+empty_string)
        if (rule == "|"+empty_string):
            rule = empty_string
        L, R = rule.split('->') 
        return L, R.split('|')
        
    def parse_rules(self, rules):
        """
        Parse a list of grammar rules.
        Return a dictionary with start symbol as a key
        and list of produced symbols as value.
        """
        rules_dict = {}
        for rule in rules:
            L, R = self.parse_rule(rule)
            rules_dict[L] = R
        return rules_dict
        
    def is_symbol(self, letter):
        return self.is_terminal(letter) or self.is_nonterminal(letter)
        
    def is_terminal(self, letter):
        return letter in self.T
        
    def is_nonterminal(self, letter):
        return letter in self.N

    def is_rightRG(self, line):
        return (self.is_terminal(line[0]) and 
                self.is_nonterminal(line[1]) and 
                len(line) == 2)
                
    def is_leftRG(self, line):
        return (self.is_terminal(line[1]) and 
                self.is_nonterminal(line[0]) and 
                len(line) == 2)
    
    def add_terminal(self, t):
        if (not self.is_nonterminal(t)):
            self.T |= {t}        

    def add_nonterminal(self, n):
        if (not self.is_terminal(n)):
            self.N |= {n}
    
    def decompose_rule(self, line):
        """
        Returns a tuple: (non-terminal, terminal)
        """
        if(len(line) == 1):
            return None, line
        else:
            if(self.type == "right"):
                return line[1], line[0]
            else:
                return line[0], line[1]
            
    def add_rule(self, left, right):
    #TODO: Use exceptions instead of returning bool
        if ((self.type == "undefined") or
            (not self.is_nonterminal(left))):
            return False
        if((len(right) == 1)):
            if (self.is_terminal(right)):
                self.P.setdefault(left, [])
                self.P[left].append(right)
                return True
            else:
                return False
        if (not ((self.type == 'right' and self.is_rightRG(right)) or
            (self.type == 'left' and self.is_leftRG(right)))):
            return False
        self.P.setdefault(left, [])
        self.P[left].append(right)
        return True

    def create_rule(self, nl, t, nr):
        left = nl
        if self.type == "left":
            right = nr+t
        else:
            right = t+nr
        self.add_terminal(t)
        self.add_nonterminal(nl)
        self.add_nonterminal(nr)
        return self.add_rule(left, right)  
        
    def remove_rule(self, left, right):
        self.P[left].remove(right)
    
    def to_rightRG(self):
        if(self.type == "right"):
            return copy.deepcopy(self)
        rRG = copy.deepcopy(self);
        rRG = Grammar(T=rRG.T, N=rRG.N, P=dict(), S=rRG.S)
        rRG.type = "right"
        for left in self.N:
            for right in self.P[left]:
                n, t = self.decompose_rule(right)
                if(left == self.S):
                    if(n is None):
                        rRG.add_rule(left, right)
                    else:
                        rRG.add_rule(n, t)
                else:
                    if(n is None):
                        rRG.create_rule(rRG.S, t, left)
                    else:
                        rRG.create_rule(n, t, left)
        return rRG                        
    
    def is_regular(self):
        """
        Check whether a grammar is regular.
        Return True if a grammar is regular, False otherwise.
        Taken from http://goo.gl/TVvRm1
        """
        verbose = self.verbose
        regular = True
        leftRG = False
        rightRG = False
        reason = ""
        wrong_rule = ""
        for left_side in self.P:
            if not self.is_nonterminal(left_side):
                reason += "\tTerminal in the left side of the rule\n"
                wrong_rule = left_side + " -> " + self.P[left_side][0]
                regular = False
            right_sides = self.P[left_side]
            for right_side in right_sides:
                if not regular:
                    break;                
                if len(right_side) > 2:
                    reason += ("\tMore than two symbols in the" + 
                        " right side of the rule\n")
                    wrong_rule = left_side + " -> " + right_side
                    regular = False
                if len(right_side) == 1:
                    if (self.is_nonterminal(right_side[0]) or 
                        not self.is_terminal(right_side[0])):
                        reason += ("\tUnexpected symbol in the right " +
                            "side of the rule\n")
                        wrong_rule = left_side + " -> " + right_side
                        regular = False
                    continue
                if not(leftRG or rightRG):
                    leftRG = self.is_leftRG(right_side)
                    rightRG = self.is_rightRG(right_side)
                    if not(leftRG or rightRG):
                        reason += ("\tTwo consecutive terminals or " +
                            "nonterminals\n")
                        wrong_rule = left_side + " -> " + right_side
                        regular = False
                if rightRG:
                    self.type = "right"
                    if not self.is_rightRG(right_side):
                        reason += ("\tInvalid order for right RG\n")
                        wrong_rule = left_side + " -> " + right_side
                        regular = False
                if leftRG:
                    self.type = "left"
                    if not self.is_leftRG(right_side):
                        reason += ("\tInvalid order for left RG\n")
                        wrong_rule = left_side + " -> " + right_side
                        regular = False
            if not regular:
                break
        if regular and verbose:
            print ("The grammar is a " + 
                self.type + " regular grammar") 
        if not regular and verbose:
            print "The grammar is not a regular grammar"
            print wrong_rule 
            print reason[:-1]
        
        return regular
    
    def __str__(self):
        Ts = '('
        for item in self.T:
            Ts += item + ', '
        Ts = Ts[:-2] + ')'
        Ns = '('
        for item in self.N:
            Ns += item + ', '
        Ns = Ns[:-2] + ')'
        Ps = 'P0..P' + str(len(self.P)-1)
        Pns = ''
        i = 0
        for key in self.P:
            R = ''
            for item in self.P[key][:-1]:
                R += item + ' | '
            R += self.P[key][-1]
            Pns += "\tP" + str(i) + " = " + key + " -> " + R + ';\n'
            i = i+1
        Pns = Pns[:-1]
        return ("G = {" + Ts + ", " + Ns + ", " + 
            Ps + ", " + self.S + "}\n" + Pns)

        