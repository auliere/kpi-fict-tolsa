#TODO: write some meaningful comments
import graphviz as gv
import functools
import argparse
import copy
import pprint
import grammar

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

    


    
class Automaton:
    
    def __init__(self, grammar, verbose = False):
        self.base_grammar = grammar
        self.verbose = verbose
        if(grammar.is_regular()):
            self.grammar = grammar.to_rightRG()
            self.H = ""
            self.Q = set()
            self.T = set()
            self.F = dict()
            self.Z = set()
            self.build_nfa()
            if(verbose):
                print self
        else:
            self = None
        
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
        Qd = set()
        Fd = dict()
        names = dict()
        for q in self.Q:
            fq = frozenset(q)
            names[fq] = q
        P.append({self.H})  
        Qd.add(frozenset(P[0]))
        while (len(P) > 0):            
            pd = P.pop(0)
            fpd = frozenset(pd)
            if(fpd not in names.keys()):
                if(fpd):
                    names[fpd] = N[0]
                    N = N[1:]
                else:
                    names[fpd] = ""
            D = names[fpd]
            for c in self.T:
                qd = set()
                for p in pd:
                    if((p, c) in self.F.keys()):
                        qd |= set(self.F[p, c])
                    fqd = frozenset(qd)
                    Fd[D, c] = fqd
                if (qd not in Qd):
                    P.append(qd)
                    Qd.add(fqd) 
        nQ = set()
        nF = dict()
        nZ = set()       
        for q in Qd:
            D = names[q]
            if(len(D) > 0):
                nQ.add(D)
                if(self.Z & q):
                    nZ |= {D}
        for n, t in [(x, y) for x in nQ for y in self.T]:
            if(Fd[n, t]):
                nF.setdefault((n, t), [])
                nF[n, t].append(names[Fd[n, t]])
        self.F = nF
        self.Z = nZ
        self.Q = nQ
        result = copy.deepcopy(self)
        self = backup
        if(self.verbose):
            print result
        return result
        
        
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
g = grammar.Grammar(T = args.T, N = args.N, P = args.P, S = args.S, verbose = verbose)
a = Automaton(g, verbose = verbose)
a = a.build_dfa()