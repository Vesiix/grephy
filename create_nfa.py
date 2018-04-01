#!/usr/bin/env python

"""
create_nfa.py

Description
  Creates an NFA from a regular expression.

@author Jesse Opitz
"""
# Python Libraries
import re, logging

# Custom imports
import finite_automata as fa

def create_nfa(rgx):
    # finite_automata(states, alphabet, transitions, init_state, acc_state)
    nfa = fa.finite_automata()

    nfa.add_state('q0', True, False)

    RE(rgx, nfa)
    
    logging.debug("NFA:")
    
    print 'Here'
    print logging.getLogger(__name__).getEffectiveLevel()
    logging.debug(nfa.print_five_tuple())

    return nfa

# Removes the first letter of a string
def next(s):
    return s[1:]

def union_RE(rgx, nfa):
    RE(rgx, nfa)
    if rgx[0] == "|":
        # Create transition/nodes
        rgx = next(rgx)
        simple_RE(rgx, nfa)

def simple_RE(rgx, nfa):
    simple_first_set = re.compile("[\*\+\(\.\$a-zA-Z0-9\\\[") 

    #if rgx[p] in simple_first_set:
    if simple_first_set.match(rgx[0]):
        basic_RE(rgx, nfa)
    else:
        concat_RE(rgx, nfa)

def concat_RE(rgx, nfa):
    simple_RE(rgx, nfa)
    basic_RE(rgx, nfa)

def basic_RE(rgx, nfa):
    star_RE(rgx, nfa)
    plus_RE(rgx, nfa)
    elementary_RE(rgx, nfa)

def star_RE(rgx, nfa):
    elementary_RE(rgx, nfa)
    if rgx[0] == "*":
        rgx = next(rgx)

def plus_RE(rgx, nfa):
    elementary_RE(rgx, nfa)
    if rgx[0] == "+":
        rgx = next(rgx)

def elementary_RE(rgx, nfa):
    group_RE(rgx, nfa)
    any_RE(rgx, nfa)
    eos_RE(rgx, nfa)
    char_RE(rgx, nfa)
    set_RE(rgx, nfa)

def group_RE(rgx, nfa):
    if rgx[0] == "(":
        rgx = next(rgx)
        RE(rgx, nfa)
        if rgx[0] == ")":
            rgx = next(rgx)

def any_RE(rgx, nfa):
    if rgx[0] == ".":
        rgx = next(rgx)

def eos_RE(rgx, nfa):
    if rgx[0] == "$":
        rgx = next(rgx)

def char_RE(rgx, nfa):
    char_patt = re.compile("[a-zA-Z0-9]")
    if char_patt.match(rgx[0]):
        rgx = next(rgx)

def set_RE(rgx, nfa):
    pos_set_RE(rgx, nfa)
    neg_set_RE(rgx, nfa)

def pos_set_RE(rgx, nfa):
    if rgx[0] == "[":
        rgx = next(rgx)
        set_items_RE(rgx, nfa)
        if rgx[0] == "]":
            rgx = next(rgx)

def neg_set_RE(rgx, nfa):
    if rgx[0] == "[":
        rgx = next(rgx)
        if rgx[0] == "^":
            rgx = next(rgx)
            set_items_RE(rgx, nfa)
            if rgx[0] == "]":
                rgx = next(rgx)

def set_items_RE(rgx, nfa):
    set_item_RE(rgx, nfa)

    set_item_RE(rgx, nfa)
    set_items_RE(rgx, nfa)

def set_item_RE(rgx, nfa):
    range_RE(rgx, nfa)
    char_RE(rgx, nfa)

def range_RE(rgx, nfa):
    char_RE(rgx, nfa)
    if rgx[0] == "-":
        rgx = next(rgx)
        char_RE(rgx, nfa)

# Regex parser
def RE(rgx, nfa):
    if re.match('^[a-zA-Z0-9]*$', rgx):
        simple_RE(rgx, nfa)
    else:
        union_RE(rgx, nfa)
        # simple regex with |'s
        #if re.match('^([a-zA-Z0-9]*\|[a-zA-Z0-9]*)*$', rgx):
        #    split_rgx = rgx.split('|')
        #    for s in split_rg        #        simple_rgx(s, nfa)
