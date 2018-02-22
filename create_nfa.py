#!/usr/bin/env python

"""
create_nfa.py

Description
  Creates an NFA from an alphabet and regular expression.

@author Jesse Opitz
"""
# Python Libraries
import re

# Custom imports
import finite_automata as fa

def create_nfa(ab, rgx):
    # finite_automata(states, alphabet, transitions, init_state, acc_state)
    nfa = fa.finite_automata()

    nfa.set_alphabet(ab)

    nfa.add_state('q0', True, False)

    parse_rgx(rgx, nfa)
    
    print "NFA:"

    nfa.print_five_tuple()

    return nfa

# rgx: <string>
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

# rgx: <string>*
def zero_or_more_rgx(rgx, nfa):
    p = 0
    prev_state = nfa.get_state('q0')
    
    nfa.add_state('q' + str(nfa.get_next_state()), False, False)
    nfa.add_transition(u'\u0395', prev_state, nfa.get_state('q' + str(nfa.get_next_state()-1)))
    
    loop_state = nfa.get_state('q' + str(nfa.get_next_state()-1))

    while rgx[p] != '*':
        prev_state = nfa.get_state('q' + str(nfa.get_next_state()-1))
        nfa.add_state('q' + str(nfa.get_next_state()), False, False)
        nfa.add_transition(rgx[p], prev_state, nfa.get_state('q' + str(nfa.get_next_state()-1)))
        p += 1

    prev_state = nfa.get_state('q' + str(nfa.get_next_state()-1))

    nfa.add_state('q' + str(nfa.get_next_state()), False, True)
    nfa.add_transition(u'\u0395', prev_state, nfa.get_state('q' + str(nfa.get_next_state()-1)))
    nfa.add_transition(u'\u0395', nfa.get_state('q' + str(nfa.get_next_state()-1)), loop_state)
    nfa.add_transition(u'\u0395', nfa.get_state('q0'), nfa.get_state('q' + str(nfa.get_next_state()-1)))
    
    
def parse_rgx(rgx, nfa):
    """
    c = 0
    while c < len(rgx):
        if re.match('[a-zA-Z0-9\.]', rgx[c]):
            if c < len(rgx)-1:
                if re.match('[\*\+{\?]', rgx[c+1]):
                    if rgx[c+1] == '*':
                        zero_or_more_rgx(rgx, nfa)

        
        c += 1
    """
    # Simple regex, no symbols 
    if re.match('^[a-zA-Z0-9\.]*$', rgx):
        simple_rgx(rgx, nfa)
    # Or symbol
    elif re.match('^([a-zA-Z0-9\.]*\|[a-zA-Z0-9\.]*)*$', rgx):
        # Only takes in simple rgx
        split_rgx = rgx.split('|')
        for s in split_rgx:
            simple_rgx(s, nfa)
    # Zero or more (*)
    elif re.match('^([a-zA-Z0-9\.]*\*[a-zA-Z0-9\.]*)*$$', rgx):
        # if there's a * somewhere
        zero_or_more_rgx(rgx, nfa)
    
