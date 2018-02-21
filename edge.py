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

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_source(self):
        return self.source

    def set_source(self, state):
        self.source = state

    def get_target(self):
        return self.target

    def set_target(self, state):
        self.target = state
