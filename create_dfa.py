#!/usr/bin/env python

"""
create_dfa.py

Description
  Converts an NFA to a DFA

@author Jesse Opitz
"""
# Python Libraries
import re, sys, logging

# Custom imports
import finite_automata as fa
import parse_nfa_to_dfa

def create_dfa(nfa):
    dfa = parse_nfa_to_dfa.parse_NFA(nfa)

    logging.debug("DFA:")

    if logging.getLogger(__name__).getEffectiveLevel() == 50:
        logging.debug(dfa.print_five_tuple())

    return dfa

