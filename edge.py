#/usr/bin/env python
"""
edge.py

Description:
  Transition object for DFA/NFA

@author Jesse Opitz
"""

class Edge:
    def __init__(self, name, source, target):
        self.name = name
        self.source = source
        self.target = target

    def get_name():
        return self.name

    def set_name(name):
        self.name = name

    def get_source():
        return self.source

    def set_source(state):
        self.source = state

    def get_target():
        return self.target

    def set_target(state):
        self.target = state
