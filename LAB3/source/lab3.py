#TODO: write some meaningful comments

import grammar
import automaton
import argparse

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
a = automaton.Automaton(g, verbose = verbose)
a.render("test")
a = a.build_dfa()
a.render("test2")