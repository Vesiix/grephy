#!/usr/bin/env python

"""
create_nfa.py

Description
  Creates an NFA from a regular expression.

@author Jesse Opitz
"""
# Python Libraries
import re, sys, logging

# Custom imports
import finite_automata as fa
import parse_rx_to_nfa

def create_nfa(rgx):
    nfa = fa.finite_automata()

    nfa.add_state('q0', True, False)
    logging.debug("create_nfa")

    p = 0
    curr_state = 0

    nfa = parse_rx_to_nfa.parse_RE(rgx, nfa, p, curr_state)
    
    #rgx, nfa, curr_state = RE(rgx, nfa, curr_state)
    
    #if len(rgx) == 0:
    #    logging.debug("Parse completed successfully.")
    #else:
    #    logging.critical("Unable to parse.")
    #    sys.exit(1)

    logging.debug("NFA:")
    
    #print logging.getLogger(__name__).getEffectiveLevel()
    logging.debug(nfa.print_five_tuple())

    return nfa
