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
        nfa_dot.render('nfa.dot', view=True)
        dfa_dot.render('dfa.dot', view=True)
    elif not args.preview:
        nfa_dot.save('nfa.dot')
        dfa_dot.save('dfa.dot')

    #TODO: Fix bug where matches first letter = matches line
    matches = find_match.find_match(dfa, args.FILE)

    for m in matches:
        print m.strip()

if __name__ == "__main__":
    main()
