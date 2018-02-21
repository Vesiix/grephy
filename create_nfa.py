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

    state_num = 0

    nfa.add_state('q' + str(state_num), True, False)

    state_num += 1
    if re.match('[a-z]*', rgx):
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
