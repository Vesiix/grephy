#!/usr/bin/env python
"""
finite_automata.py

Description:
  Creates DFA/NFA objects that can be drawn in dot format.

@author Jesse Opitz
"""

class finite_automata:
    """
    Object containing 5 tuple needed for creating an NFA or DFA.
    
    @type   states:      list
    @param  states:      All available states of NFA/DFA
    @type   alphabet:    string
    @param  alphabet:    Alphabet of the NFA/DFA
    @type   transitions: list
    @param  transitions: (delta) All transitions of the NFA/DFA
    @type   init_state:  string
    @param  init_state:  Initial state of the NFA/DFA
    @type   acc_state:   list
    @param  acc_state:   Accepting states of the NFA/DFA
    """
    def __init__(self, states, alphabet, transitions, init_state, acc_state):
        # List of states
        self.states = []
        
        # Alphabet
        self.alphabet = ''
        
        # List of transitions
        self.transitions = []

        # Initial/start state
        self.init_state = ''

        # List of accepting states
        self.acc_states = []
    
    def draw(outfile):
        print 'draw finite automata'

