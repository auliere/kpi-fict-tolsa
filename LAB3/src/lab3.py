#TODO: write some meaningful comments

import grammar
import automaton
import argparse
import os

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
group2 = parser.add_argument_group()
group = group2.add_mutually_exclusive_group()
group.add_argument("--non-deterministic-fsa", '-nfa', action = 'store_true',
                    help='Build a non-deterministic finite state automaton')
group.add_argument("--deterministic-fsa", '-dfa', action = 'store_true',
                    help='Build a deterministic finite state automaton')
group2.add_argument("--image-name", '-i',
                    help="Specify the name of the graph (*.svg) output file.")
                    
args = parser.parse_args()
verbose = args.verbose
g = grammar.Grammar(
    T = args.T, 
    N = args.N, 
    P = args.P, 
    S = args.S, 
    verbose = verbose)
print "Grammar, ", g.T
if(args.non_deterministic_fsa):
    a = automaton.Automaton(g, verbose)
    if(args.image_name):
        a.render(args.image_name)
        os.remove(args.image_name)
if(args.deterministic_fsa):
    a = automaton.Automaton(g).set_verbose(verbose).build_dfa()
    if(args.image_name):
        a.render(args.image_name)
        os.remove(args.image_name)

    