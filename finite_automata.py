#!/usr/bin/env python
'''
finite_automata.py

Description:
  Creates DFA/NFA objects that can be drawn in dot format.

@author Jesse Opitz
'''

class finite_automata:
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

