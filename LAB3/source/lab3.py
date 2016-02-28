import graphviz as gv
import functools
import argparse

graph = functools.partial(gv.Graph, format='svg')
digraph = functools.partial(gv.Digraph, format='svg')

def add_nodes(graph, nodes):
    """
    Adds nodes to a graph and returns a graph
    Taken from http://matthiaseisen.com/articles/graphviz/
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
    Taken from http://matthiaseisen.com/articles/graphviz/
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
    print rules
    for rule in rules:
        print rule
        L, R = parse_rule(rule)
        rules_dict[L] = R
    return rules_dict

    
class Grammar:
    """Class that holds a grammar"""
    def __init__(self, T, N, P, S):
        self.T = T
        self.N = N
        self.P = parse_rules(P)
        self.S = S
    
    def __repr__(self):
        Ts = '('
        for item in self.T[:-1]:
            Ts += item + ', '
        Ts += self.T[-1] + ')'
        Ns = '('
        for item in self.N[:-1]:
            Ns += item + ', '
        Ns += self.N[-1] + ')'
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
        
       
parser = argparse.ArgumentParser(description = 'Build an automaton for regular grammar.')
parser.add_argument("-T", nargs='+', required=True, help='List of terminals of a grammar');
parser.add_argument("-N", nargs='+', required=True, help='List of non-terminals of a grammar');
parser.add_argument("-P", nargs='+', required=True, help='Rules of production for grammar');
parser.add_argument("-S", required=True, help='Starting symbol of a grammar');

args = parser.parse_args()

print Grammar(T = args.T, N = args.N, P = args.P, S = args.S)