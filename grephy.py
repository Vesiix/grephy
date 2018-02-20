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
import state, edge

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

def find_alphabet(fname):
    """
    Find's the alphabet being used within the 
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

# I think this should be its own file
def create_dfa(nfa):
    dfa = fa.finite_automata()

    dfa.set_alphabet(nfa.get_alphabet)

# I think this should be its own file
def create_nfa(ab, rgx): 
    # finite_automata(states, alphabet, transitions, init_state, acc_state)
    nfa = fa.finite_automata()

    nfa.set_alphabet(ab)
    
    state_num = 0

    nfa.add_state('q' + str(state_num), True, False)

    state_num += 1

    # If simple regex with no |'s, *'s, or groupings
    p = 0
    while p < len(rgx):
        if p == len(rgx)-1:
            nfa.add_state('q' + str(state_num), False, True)
        else:
            nfa.add_state('q' + str(state_num), False, False)
        # TODO: Source and target of transition should be a legit state, not string
        nfa.add_transition(rgx[p], 'q' + str(state_num-1), 'q' + str(state_num))
        state_num += 1
        p += 1

    #split_on_or = rgx.split('|')

    #nfa.add_state('q1', False, True)
    #nfa.add_transition('r', 'q0', 'q1')
    
    print "NFA:"
    nfa.print_five_tuple()

    return nfa

# Kind of useless now that I have creates for each...
"""
def create_fa(rgx, ab):
    
    Creates and draws the NFA/DFA using the finite_automata.py file
    using the given alphabet and regular expression.
    
    @type    rgx: string
    @param   rgx: Regular expression as a string
    @type    ab:  string
    @param   ab:  Alphabet of NFA/DFA
    @rtype:       tuple of finite_automata objects
    @return:      (dfa, nfa)
    

    nfa = create_nfa(ab, rgx)
    dfa = create_dfa(nfa) 
    return dfa, nfa
"""

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')

    parser = argparse.ArgumentParser(description='Searches files for regular expression pattern matches.')
    
    parser.add_argument('-n', '--NFA-FILE', nargs=1, help='Output file for NFA')
    
    parser.add_argument('-d', '--DFA-FILE', nargs=1, help='Output file for DFA')

    parser.add_argument('REGEX', type=str, help='Regular expression file')
    
    parser.add_argument('FILE', type=str, help='Input file')

    args = parser.parse_args()

    ab = find_alphabet(args.FILE)
    
    nfa = create_nfa(ab, args.REGEX)

    dfa = create_dfa(nfa) 

if __name__ == "__main__":
    main()
