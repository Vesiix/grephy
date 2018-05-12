#!/usr/bin/env python

"""
grephy.py

Usage:
  grephy.py [-h] [-n NFA_FILE] [-d DFA_FILE] REGEX FILE

Description:
  A grep utility that searches files for regular expression
  pattern matches and produces dot graph file output for the
  automata used in the matching computation.

@author Jesse Opitz

Due Date: 05/07/18
"""
# Python libraries
import argparse, logging, sys
from graphviz import Digraph

# Custom python files
import finite_automata as fa
import create_nfa as cnfa
import create_dfa as cdfa
import state, edge
import draw_fa
import find_match

def read_file(fname):
    """
    Reads data inside a file.

    @type    fname: string
    @param   fname: Name of the file to read
    @rtype:         string
    @return:        Data within the file
    """
    try:
        with open(fname, 'r') as f:
            data = f.read();
        return data
    except IOError as e:
        logging.critical("FILE['{2}'] I/O error({0}): {1}".format(e.errno, e.strerror, fname))
        sys.exit(1)
    except:
        logging.critical("Unexpected error:", sys.exc_info()[0])
        raise
        sys.exit(1)

def main():
    logging.basicConfig(level=logging.CRITICAL, format='%(levelname)s:%(message)s')

    parser = argparse.ArgumentParser(description='Searches files for regular expression pattern matches.')
    
    parser.add_argument('-n', '--NFA-FILE', nargs=1, help='Output file for NFA')
    
    parser.add_argument('-d', '--DFA-FILE', nargs=1, help='Output file for DFA')

    parser.add_argument('-p', '--preview', action="store_true", help='Opens a pdf view of DFA and NFA')

    parser.add_argument('REGEX', type=str, help='Regular expression file')
    
    parser.add_argument('FILE', type=str, help='Input file')

    args = parser.parse_args()

    nfa = cnfa.create_nfa(args.REGEX)

    dfa = cdfa.create_dfa(nfa)

    nfa_dot = draw_fa.draw(nfa)
    dfa_dot = draw_fa.draw(dfa)
    if args.preview:
        if args.NFA_FILE is None:
            nfa_dot.render('nfa.dot', view=True)
        elif args.NFA_FILE is not None:
            nfa_dot.render(args.NFA_FILE[0], view=True)

        if args.DFA_FILE is None:
            dfa_dot.render('dfa.dot', view=True)
        elif args.DFA_FILE is not None:
            nfa_dot.render(args.DFA_FILE[0], view=True)

    elif not args.preview:
        if args.NFA_FILE is None:
            nfa_dot.save('nfa.dot')
        elif args.NFA_FILE is not None:
            nfa_dot.render(args.NFA_FILE[0])

        if args.DFA_FILE is None:
            dfa_dot.save('dfa.dot')
        elif args.DFA_FILE is not None:
            nfa_dot.save(args.DFA_FILE[0])


    #TODO: Fix bug where matches first letter = matches line
    matches = find_match.find_match(dfa, args.FILE)

    for m in matches:
        print m.strip()

if __name__ == "__main__":
    main()
