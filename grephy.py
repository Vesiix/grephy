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

# Custom python files
import finite_automata as fa

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

def get_alphabet(fname):
    """
    Get's the alphabet being used within the 
    input file

    @type    fname: string
    @param   fname: Name of the input file.
    @rtype:         string
    @return:        The alphabet to being used in the file.
    """
    alphabet = ''
    data = read_file(fname)
    for line in data:
        for c in line:
            if c not in alphabet:
                alphabet += c

    logging.debug("Alphabet: " + repr(alphabet))

    return alphabet

def create_fa(rgx, ab):
    """
    Creates and draws the NFA/DFA using the finite_automata.py file
    using the given alphabet and regular expression.
    
    @type    rgx: string
    @param   rgx: Regular expression as a string
    @type    ab:  string
    @param   ab:  Alphabet of NFA/DFA
    @rtype:       tuple of finite_automata objects
    @return:      (dfa, nfa)
    """
    # finite_automata(states, alphabet, transitions, init_state, acc_state)
    nfa = fa.finite_automata(states=[], alphabet=ab, transitions=[], init_state='', acc_state=[])
    dfa = fa.finite_automata(states=[], alphabet=ab, transitions=[], init_state='', acc_state=[])

    return dfa, nfa

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')

    parser = argparse.ArgumentParser(description='Searches files for regular expression pattern matches.')
    
    parser.add_argument('-n', '--NFA-FILE', nargs=1, help='Output file for NFA')
    
    parser.add_argument('-d', '--DFA-FILE', nargs=1, help='Output file for DFA')

    parser.add_argument('REGEX', type=str, help='Regular expression file')
    
    parser.add_argument('FILE', type=str, help='Input file')

    args = parser.parse_args()

    alphabet = get_alphabet(args.FILE)

    dfa, nfa = create_fa(args.REGEX, alphabet)

if __name__ == "__main__":
    main()
