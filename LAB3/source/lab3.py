import graphviz as gv
import functools
import argparse

graph = functools.partial(gv.Graph, format='svg')
digraph = functools.partial(gv.Digraph, format='svg')

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
	
def parse_rule(rule):
    """
    Parse a grammar rule and return a tuple: 
    a starting symbol and a list of end symbols
    """
    rule = "".join(rule.split())    
    L, R = rule.split('->') 
    return L, R.split('|')
	
def parse_rules(rules):
    """
    Parse a list of grammar rules.
    Return a dictionary with start symbol as a key
    and list of produced symbols as value.
    """
    rules_dict = {}
    for rule in rules:
        L, R = parse_rule(rule)
        rules_dict[L] = R
    return rules_dict

    
class Grammar:
    """Class that holds a grammar"""
    def __init__(self, T, N, P, S):
        self.T = set(T)
        self.N = set(N)
        self.P = parse_rules(P)
        self.S = S
            
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
                    if verbose:
                        print ("Wrong rule: " + wrong_rule + 
                            "\n" + reason[:-1])
                    return False                
                if len(right_side) > 2:
                    reason += ("\tMore than two symbols in the" + 
                        " right side of the rule\n")
                    wrong_rule = left_side + " -> " + right_side
                    regular = False
                if len(right_side) == 1:
                    if self.is_nonterminal(right_side[0]):
                        reason += ("\tUnexpected nonterminal in the right " +
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
                    if not self.is_rightRG(right_side):
                        reason += ("\tInvalid order for right RG\n")
                        wrong_rule = left_side + " -> " + right_side
                        regular = False
                if leftRG:
                    if not self.is_leftRG(right_side):
                        reason += ("\tInvalid order for left RG\n")
                        wrong_rule = left_side + " -> " + right_side
                        regular = False
        if regular and verbose:
            print str(self) + "\nThe above grammar is a regular grammar"
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
        return "G = {" + Ts + ", " + Ns + ", " + Ps + ", " + self.S + "}\n" + Pns
    
       
parser = argparse.ArgumentParser(
                    description = 'Build an automaton for regular grammar.')
parser.add_argument("-T", nargs='+', required=True, 
                    help='List of terminals of a grammar')
parser.add_argument("-N", nargs='+', required=True, 
                    help='List of non-terminals of a grammar')
parser.add_argument("-P", nargs='+', required=True,
                    help='Rules of production for grammar')
parser.add_argument("-S", required=True,
                    help='Starting symbol of a grammar')

args = parser.parse_args()

g = Grammar(T = args.T, N = args.N, P = args.P, S = args.S)
g.is_regular(verbose=True)