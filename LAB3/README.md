# Lab3. Building a finite automaton for a regular grammar
## Intention
The program `lab3.py` accepts a formal grammar via command line arguments,
checks the grammar for regularity and, if needed, builds either a
deterministic finite automaton or a 
non-deterministic finite automaton for that grammar. There is an option to 
save the graph of the automaton as a `*.svg` image

## Dependencies
The program is written in Python 2.7 and uses a graphviz library for python 
to produce graphs.

## Usage
```
usage: lab3.py [-h] [--verbose] -T T [T ...] -N N [N ...] -P P [P ...] -S S
               [--non-deterministic-fsa | --deterministic-fsa]
               [--image-name IMAGE_NAME]

Build an automaton for regular grammar. \e and ` denote an empty string

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v         Enable verbose output
  -T T [T ...]          List of terminals of a grammar
  -N N [N ...]          List of non-terminals of a grammar
  -P P [P ...]          Rules of production for grammar (example: "S->aS|a")
  -S S                  Starting symbol of a grammar

  --non-deterministic-fsa, -nfa
                        Build a non-deterministic finite state automaton
  --deterministic-fsa, -dfa
                        Build a deterministic finite state automaton
  --image-name IMAGE_NAME, -i IMAGE_NAME
                        Specify the name of the graph (*.svg) output file.
```
### Example
#### input
`python "..\src\lab3.py" -T a b -N S A -P "S->bA|a" "A->a|aA|bA" -S S -nfa -v -i "graph"`

#### output
```
G = {(a, b), (A, S), P0..P1, S}
        P0 = A -> a | aA | bA;
        P1 = S -> bA | a;
The grammar is a right regular grammar
Automaton:
        H: S
        Q: set(['A', 'S', 'N'])
        T: set(['a', 'b'])
        Z: set(['N'])
        F:
                {('A', 'a'): ['A', 'N'],
                 ('A', 'b'): ['A'],
                 ('S', 'a'): ['N'],
                 ('S', 'b'): ['A']}
```
graph.svg
