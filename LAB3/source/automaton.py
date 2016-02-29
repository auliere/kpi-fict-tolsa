import graphviz as gv
import functools
import copy
import pprint
import grammar

class Digraph:

    def __init__(self):
        self.g = gv.Digraph(format = "svg")
        
    def add_nodes(self, nodes):
        """
        Adds nodes to a graph and returns a graph
        Taken from http://goo.gl/TZ9dol
        """
        for n in nodes:
            if isinstance(n, tuple):
                self.g.node(n[0], **n[1])
            else:
                self.g.node(n)
        return self

    def add_edges(self, edges):
        """
        Adds edges to a graph and returns a graph
        Taken from http://goo.gl/TZ9dol
        """
        for e in edges:
            if isinstance(e[0], tuple):
                self.g.edge(*e[0], **e[1])
            else:
                self.g.edge(*e)
        return self
    
    def render(self, file):
        self.g.render(file)        
    
class Automaton:
    
    def __init__(self, grammar, verbose = False):
        self.base_grammar = grammar
        self.verbose = verbose
        self.digraph = None
        self.H = ""
        self.Q = set()
        self.T = set()
        self.F = dict()
        self.Z = set()
        self.broken = True;
        if(grammar.is_regular()):
            self.broken = False
            self.grammar = grammar.to_rightRG()
            self.build_nfa()            
            if(verbose):
                print self         
        
    def build_nfa(self):
        if(not self.broken):
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
        return self
        
    def build_dfa(self):
        if(not self.broken):
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
        return self
        
    def render(self, file):
        if(not self.broken):
            if(self.digraph is None):
                self.digraph = Digraph()
            g = self.digraph;
            g.add_nodes(
                [
                    ('empty_node', {'style': 'invis'}),
                    (self.H, {'shape': 'circle'})
                ]
            ).add_edges(
                [
                    ('empty_node', self.H)
                ]
            )
            
            for n in self.Z:
                g.add_nodes(
                    [
                        (n, {"shape": "doublecircle"})
                    ]
                )
            for n in (self.Q - {self.H} - self.Z):
                g.add_nodes(
                    [
                        (n, {"shape": "circle"})
                    ]
                )
            tF=[
                    ((n1, n3), n2) 
                    for (n1, n2) in self.F.keys() 
                    for n3 in self.F[n1, n2]
                ]
            for e, lbl in tF:
                g.add_edges(
                    [
                        ( e, {'label': lbl})
                    ]
                )        
            g.render(file)
        
    def __str__(self):
        if(self.broken):
            return "Impossible to build an automaton"
        return ("Automaton: " + 
            "\n\tH: " + str(self.H) +
            "\n\tQ: " + str(self.Q) +
            "\n\tT: " + str(self.T) +
            "\n\tZ: " + str(self.Z) +
            "\n\tF: " + str(self.F))