#!/usr/bin/env python
"""
finite_automata.py

Description:
  Creates DFA/NFA objects that can be drawn in dot format.

@author Jesse Opitz
"""

# Custom python files
import edge, state

class finite_automata:
    """
    Object containing 5 tuple needed for creating an NFA or DFA.
    
    @type   states:      list of type state
    @param  states:      All available states of NFA/DFA
    @type   alphabet:    string
    @param  alphabet:    Alphabet of the NFA/DFA
    @type   transitions: list of type edge
    @param  transitions: (delta) All transitions of the NFA/DFA
    @type   init_state:  string
    @param  init_state:  Initial state of the NFA/DFA
    @type   acc_state:   list of type state
    @param  acc_state:   Accepting states of the NFA/DFA
    """
    def __init__(self, alphabet):
        # List of states
        self.states = []
        
        # Alphabet
        self.alphabet = alphabet
        
        # List of transitions
        self.transitions = []

        # Initial/start state
        self.init_state = ''

        # List of accepting states
        self.acc_states = []
    
    def draw(outfile):
        print 'draw finite automata'
    
    def add_state(name, is_init, is_acc):
        new_state = State(name, is_init, is_acc)
        self.states.append(new_state)

    def rem_state(state_name):
        print 'remove', state_name
    
    def add_transition(name, source, target):
        new_edge = Edge(name, source, target)
        self.transitions.append(new_edge)

    def rem_transition(edge_name):
        print 'remove', edge_name

    def add_acc_state(state):
        # go through list of states
        # change state status is_acc = True
        # add to list of acc_states
        self.acc_states.append(state)
    
    def rem_acc_state(state):
        # go through list of states
        # change state status is_acc = False
        # rem from list of acc_states
        print 'remove', state
    
    def get_states():
        # returns a string of states
        return ''

    def get_alphabet():
        # returns string of alphabet
        return repr(self.alphabet)

    def get_transitions():
        # returns list of transitions
        return []

    def get_init():
        # returns initial state
        return self.init_state

    def get_acc_state():
        # returns list of accepting states
        return []

    def print_transitions():
        # returns a string of a list of transitions
        return ''

    def print_acc_states():
        # returns a string of a list of accepting states
        return ''
