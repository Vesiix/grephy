#!/usr/bin/env python

"""
create_dfa.py

Description
  Converts an NFA to a DFA

@author Jesse Opitz
"""

import finite_automata as fa

def create_dfa(nfa):
    # finite_automata(states, alphabet, transitions, init_state, acc_state)
    dfa = fa.finite_automata()

    dfa.set_alphabet(nfa.get_alphabet())
    
    state_num = 0

    dfa.add_state('q' + str(state_num), True, False)
    
    state_num += 1

    return dfa
