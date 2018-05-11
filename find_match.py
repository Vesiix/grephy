#/usr/bin/env python

"""
find_match.py

Description:
    Finds all lines inside a file that match a 
    pattern specified by a DFA.
"""

import logging

from state import *

def find_match(dfa, input_file):
    """
    @params dfa          DFA used to match patterns
    @params input_file   File to be read
    @type   dfa          finite_automata
    @type   input_file   file
    """
    line_list = []

    # list of line matches
    match_list = []

    with open(input_file, 'r') as f:
        for line in f:
            # Change to true to skip to end of line
            line_list.append(line)

    match_list = []
    
    for l in line_list:
        p = 0
        curr_state = dfa.get_state('q0')
        while p < len(l):
            found = False
            c = l[p].strip()
            if c != '\n':
                if c in dfa.get_alphabet():
                    # If c is in the alphabet

                    # Get a list of possible transitions from the current state
                    poss_trans = dfa.find_src_transitions(curr_state.get_name())

                    # Check to see if any of those transitions match the character
                    for t in poss_trans:
                        if t.get_name() == c:
                            # If transition matches the character
                            # |-> change current state to target
                            trans = t
                            curr_state = t.get_target()
                            found = True
                            break

                    if not found:
                        break
                else:
                    non_acc_state = State('null', False, False)
                    curr_state = non_acc_state
            p+=1

        if curr_state.get_acc():
            logging.debug('Found match: ' + str(l))
            match_list.append(l)

    return match_list
