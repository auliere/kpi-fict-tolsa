#TODO: write some meaningful comments
import graphviz as gv
import functools
import argparse
import copy

graph = functools.partial(gv.Graph, format='svg')
digraph = functools.partial(gv.Digraph, format='svg')
empty_string = "`"

def add_nodes(graph, nodes):
    """
    Adds nodes to a graph and returns a graph
    Taken from http://goo.gl/TZ9dol
    """
    for n in nodes:
        if isinstance(n, tuple):
            graph.node(n[0], **n[1])
        else:
            graph.node(n)
    return graph

def add_edges(graph, edges):
    """
    Adds edges to a graph and returns a graph
    Taken from http://goo.gl/TZ9dol
    """
    for e in edges:
        if isinstance(e[0], tuple):
            graph.edge(*e[0], **e[1])
        else:
            graph.edge(*e)
    return graph
	


    
class Grammar:
    """Class that holds a grammar"""
    #TODO: Add more error handling
    def __init__(self, T, N, P, S):
        self.T = set(T)
        if "\\e" in self.T:
            self.T -= {"\\e"}
            self.T |= {"`"}
        self.N = set(N)
        self.P = self.parse_rules(P)
        self.S = S 
        self.type = "undefined"
        
    def parse_rule(self, rule):
        """
        Parse a grammar rule and return a tuple: 
        a starting symbol and a list of end symbols
        """
        rule = "".join(rule.split())
        rule = rule.replace("||", "|"+empty_string)
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
    
    def is_regular(self, verbose=False):
        """
        Check whether a grammar is regular.
        Return True if a grammar is regular, False otherwise.
        Taken from http://goo.gl/TVvRm1
        """
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
            print (str(self) + "\nThe above grammar is a " + 
                self.type + " regular grammar")
        if not regular and verbose:
            print str(self) + "\nThe above grammar is not a regular grammar"
            print wrong_rule 
            print reason[:-1]
        return regular
    
    def __repr__(self):
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


    
class Automaton:
    
    def __init__(self, grammar):
        self.base_grammar = grammar
        self.grammar = grammar.to_rightRG()
        self.H = ""
        self.Q = set()
        self.T = set()
        self.F = dict()
        self.Z = set()
        self.build_nfa()
        
    def build_nfa(self):
        N = filter((lambda s: not self.grammar.is_symbol(s)), "NMLKQVSPCZJTEIOX")[0]
        for nonterminal in self.base_grammar.N:
            t_set = set()
            nt_set = set()
            for rule in self.grammar.P[nonterminal]:
                n, t = self.grammar.decompose_rule(rule)
                if(n is None):
                    t_set |= {t}
                    self.grammar.remove_rule(nonterminal, rule)
                else:
                    nt_set |= {t}
            for t in t_set:
                self.grammar.create_rule(nonterminal, t, N)                
        self.H = self.grammar.S
        self.Q = self.grammar.N
        self.T = self.grammar.T
        for left in self.grammar.N:
            t_set = set()
            nt_set = set()            
            if(left in self.grammar.P.keys()):
                for rule in self.grammar.P[left]:                
                    n, t = self.grammar.decompose_rule(rule)
                    if(n is not None):
                        self.F.setdefault((left, t), [])
                        self.F[left, t].append(n)
                        nt_set |= {t}                
                    if(n is None):
                        t_set |= {t}
        self.Z |= {N}
        return self
        
    def build_dfa(self):
        N = filter((lambda s: not self.grammar.is_symbol(s)), "NMLKQVSPCZJTEIOX")
        backup = copy.deepcopy(self)
        P = []
        Qd = []
        Fd = dict()
        names = dict()
        P.append(H})
        
    def __str__(self):
        return ("Automaton: " + 
            "\n\tH: " + str(self.H) +
            "\n\tQ: " + str(self.Q) +
            "\n\tT: " + str(self.T) +
            "\n\tZ: " + str(self.Z) +
            "\n\tF: " + str(self.F))
            
parser = argparse.ArgumentParser(
                    description = 'Build an automaton for regular grammar.' + 
                        '\n \\e and ` denote an empty string')
parser.add_argument("--verbose", '-v', action = 'store_true',
                    help='Enable verbose output')                    
parser.add_argument("-T", nargs='+', required=True, 
                    help='List of terminals of a grammar')
parser.add_argument("-N", nargs='+', required=True, 
                    help='List of non-terminals of a grammar')
parser.add_argument("-P", nargs='+', required=True,
                    help='Rules of production for grammar')
parser.add_argument("-S", required=True,
                    help='Starting symbol of a grammar')

args = parser.parse_args()
verbose = args.verbose
g = Grammar(T = args.T, N = args.N, P = args.P, S = args.S)
a = Automaton(g)

print a
print g

a.build_dfa()