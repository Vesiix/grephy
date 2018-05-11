#!/usr/bin/env python

"""
parse_nfa_to_dfa.py

Description:
    Converts NFA to DFA
"""

import logging, sys
import finite_automata as fa

def parse_NFA(nfa):
    # Check for epsilons
    eps_exist = False
    #eps_states = []
    for t in nfa.get_transitions():
        if t.get_name() == 'Epsilon':
            eps_exist = True

    if not eps_exist:
        return nfa

    elif eps_exist:
        dfa = fa.finite_automata()
        dfa.set_alphabet(nfa.get_alphabet())
        dfa.add_state('q' + str(dfa.get_next_state()), True, False) 
        
        eps_states = e_closure(nfa, dfa, nfa.get_state('q0'))
        
        for e in eps_states:
            curr_state = 0

            n_state = nfa.get_state(e)
            n_transitions = nfa.find_src_transitions(e)

            for t in n_transitions:
                dfa.add_state('q' + str(dfa.get_next_state()), False, False)
                dfa.add_transition(t.get_name(), 'q' + str(curr_state),'q' + str(dfa.get_next_state()-1))
                nfa_state = t.get_target()
                curr_state = dfa.get_next_state()-1
                build_branch(nfa, dfa, curr_state, nfa_state)
           
    return dfa

def e_closure(nfa, dfa, curr_state):
    curr_trans = nfa.find_src_transitions(curr_state.get_name())
    
    targets = []
    
    for t in curr_trans:
        if t.get_name() == "Epsilon":
            targets.append(t.get_target().get_name())
    return targets 

def build_branch(nfa, dfa, curr_state, nfa_state, nfa_done=[]):
    if nfa_state.get_name() in nfa_done:
        return
    nex = nfa.find_src_transitions(nfa_state.get_name())
    for n in nex:
        if n.get_source() == n.get_target():
            dfa.add_transition(n.get_name(), 'q' + str(curr_state), 'q' + str(curr_state))
        else:
            dfa.add_state('q' + str(dfa.get_next_state()), False, False)
            dfa.add_transition(n.get_name(), 'q' + str(curr_state), 'q' + str(dfa.get_next_state()-1))
            curr_state = dfa.get_next_state()-1
        nfa_done.append(nfa_state.get_name())
        build_branch(nfa, dfa, curr_state, n.get_target(), nfa_done=nfa_done)

    dfa.set_acc_state('q' + str(dfa.get_next_state()-1))

    return dfa
