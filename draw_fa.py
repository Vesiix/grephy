#!/usr/bin/env python
"""
dot_draw_fa.py

Description:
    Draws a finite automata given a NFA/DFA object in a dot format.

@author: Jesse Opitz

"""
from graphviz import Digraph

def draw(fa):
    dot = Digraph()
    dot.attr(rankdir='LR', size='8,5')    
    # Creates state as nodes
    for s in fa.get_states():
        if s.get_acc() == True:
            dot.attr('node', shape='doublecircle')
            dot.node(s.get_name(), s.get_name())
        else:
            dot.attr('node', shape='circle')
            dot.node(s.get_name(), s.get_name())

    # Creates edges for transitions
    for t in fa.get_transitions():
        dot.edge(t.get_source().get_name(), t.get_target().get_name(), label=(t.get_name()))


    return dot

