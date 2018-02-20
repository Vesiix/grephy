#/usr/bin/env python

"""
state.py

Description:
  State object for DFA/NFA

@author Jesse Opitz
"""

class State:
    def __init__(self, name, is_init, is_acc):
        self.name = name
        self.is_init = is_init
        self.is_acc = is_acc
    
    def flip_acc(self):
        if is_acc:
            is_acc = False
        else:
            is_acc = True

    def flip_init(self):
        if is_init:
            is_init = False
        else:
            is_init = True

    def set_acc(self, val):
        if val == True or val == False:
            self.is_acc = val
        else:
            # Error
            sys.exit(1)
    
    def get_acc(self):
        return self.is_acc

    def set_init(self, val):
        if val == True or val == False:
            self.is_init = val
        else:
            # Error
            sys.exit(1)

    def get_init(self):
        return self.is_init

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

