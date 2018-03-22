#!/usr/bin/env python

"""
create_nfa.py

Description
  Creates an NFA from a regular expression.

@author Jesse Opitz
"""
# Python Libraries
import re, logging

# Custom imports
import finite_automata as fa

def create_nfa(rgx):
    # finite_automata(states, alphabet, transitions, init_state, acc_state)
    nfa = fa.finite_automata()

    nfa.add_state('q0', True, False)

    parse_rgx(rgx, nfa)
    
    logging.debug("NFA:")
    
    print 'Here'
    print logging.getLogger(__name__).getEffectiveLevel()
    logging.debug(nfa.print_five_tuple())

    return nfa

def simple_rgx(rgx, nfa):
    p = 0

    if p == len(rgx)-1:
        nfa.add_state('q' + str(nfa.get_next_state()), False, True)
    else:
        nfa.add_state('q' + str(nfa.get_next_state()), False, False)

    nfa.add_transition(rgx[p], nfa.get_state('q0'), nfa.get_state('q' + str(nfa.get_next_state()-1)))
    
    p += 1

    while p < len(rgx):
        prev_state = nfa.get_state('q' + str(nfa.get_next_state()-1))

        if p == len(rgx)-1:
            nfa.add_state('q' + str(nfa.get_next_state()), False, True)
        else:
            nfa.add_state('q' + str(nfa.get_next_state()), False, False)

        nfa.add_transition(rgx[p], prev_state, nfa.get_state('q' + str(nfa.get_next_state()-1)))
        p += 1

def parse_rgx(rgx, nfa):
    if re.match('^[a-zA-Z0-9]*$', rgx):
        simple_rgx(rgx, nfa)
    else:
        # simple regex with |'s
        if re.match('^([a-zA-Z0-9]*\|[a-zA-Z0-9]*)*$', rgx):
            split_rgx = rgx.split('|')
            for s in split_rgx:
                simple_rgx(s, nfa)

