#!/usr/bin/env python

"""
parse_nfa_to_dfa.py

Description:
    Converts NFA to DFA
"""

import logging, sys
import finite_automata as fa
import pprint

def parse_NFA(nfa):
    # Check for epsilons
    eps_exist = False
    #eps_states = []
    for t in nfa.get_transitions():
        if t.get_name() == 'Eps':
            #eps_state.append(t.get_source())
            eps_exist = True

    if not eps_exist:
        return nfa
    elif eps_exist:
        dfa = fa.finite_automata()
        
        e_closures = []

        for s in nfa.get_states():
            e_closures.append(e_closure(nfa, dfa, s))
        
        pprint.pprint(e_closures)

        

        sys.exit(1)

def e_closure(nfa, dfa, curr_state):
    #print curr_state
    curr_trans = nfa.find_src_transitions(curr_state.get_name())
    
    targets = [curr_state.get_name()]
    
    for t in curr_trans:
        if t.get_name() == "Eps":
            targets.append(t.get_target().get_name())
    #print 't:', targets    
    return targets 

