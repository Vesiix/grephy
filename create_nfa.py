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

def create_nfa(rgx):
    nfa = fa.finite_automata()

    nfa.add_state('q0', True, False)
    logging.debug("create_nfa")

    curr_state = 0
    rgx, nfa = RE(rgx, nfa, curr_state)
    
    if len(rgx) == 0:
        logging.debug("Parse completed successfully.")
    else:
        logging.critical("Unable to parse.")
        sys.exit(1)

    logging.debug("NFA:")
    
    print logging.getLogger(__name__).getEffectiveLevel()
    logging.debug(nfa.print_five_tuple())

    return nfa

# Removes the first letter of a string
def next(s):
    return s[1:]

def union_RE(rgx, nfa, curr_state):
    logging.debug("In union:" + rgx)
    list_rgx = rgx.split('|')
    first_rgx, nfa = RE(list_rgx[0], nfa, curr_state)
    if len(first_rgx) > 0:
        if len(list_rgx) > 1:
            r = 1
            while r < (len(list_rgx)-1):
                curr_rgx, nfa = RE(list_rgx[r], nfa, curr_state)
                r += 1
                if len(curr_rgx) > 0:
                    logging.critical("Error while parsing a part of union.")
                    sys.exit(1)
    else:
        logging.critical("Error while parsing first part of union.")
        sys.exit(1)

    #if len(rgx) > 0:
    #    if rgx[0] == "|":
            # Create transition/nodes
    #        rgx = next(rgx)
    #        rgx, nfa = simple_RE(rgx, nfa, curr_state)
    #    else:
    #        logging.critical("Error in union parse.")
    #        sys.exit(1)

    logging.debug("Out union:" + rgx)

    return rgx, nfa

def simple_RE(rgx, nfa, curr_state):
    logging.debug("In simple:" + rgx)
    simple_first_set = re.compile("[\*\+\.\(\$\[\\a-zA-Z0-9]")
    # HOW DO YOU DIFFERENTIATE THESE???
    if len(rgx) > 0:
        if simple_first_set.match(rgx[0]):
            rgx, nfa = basic_RE(rgx, nfa, curr_state)
        else:
            rgx, nfa = concat_RE(rgx, nfa, curr_state)
 
    logging.debug("Out simple:" + rgx)

    return rgx, nfa

def concat_RE(rgx, nfa, curr_state):
    logging.debug("In concat:" + rgx)
    rgx, nfa = simple_RE(rgx, nfa, curr_state)
    rgx, nfa = basic_RE(rgx, nfa, curr_state)
    
    logging.debug("Out concat:" + rgx)

    return rgx, nfa

def basic_RE(rgx, nfa, curr_state):
    logging.debug("In basic:" + rgx)
    rgx, nfa = elementary_RE(rgx, nfa, curr_state)
    if len(rgx) > 0:
        if rgx[0] == "*":
            rgx, nfa = star_RE(rgx, nfa, curr_state)
        elif rgx[0] == "+":
            rgx, nfa = plus_RE(rgx, nfa, curr_state)
    logging.debug("Out basic:" + rgx)

    return rgx, nfa

def star_RE(rgx, nfa, curr_state):
    logging.debug("In star:" + rgx)
    rgx = next(rgx)
    logging.debug("Out star:" + rgx)

    return rgx, nfa

def plus_RE(rgx, nfa, curr_state):
    logging.debug("In plus:" + rgx)
    rgx = next(rgx)
    logging.debug("Out plus:" + rgx)

    return rgx, nfa

def elementary_RE(rgx, nfa, curr_state):
    logging.debug("In elementary:" + rgx)
    if len(rgx) > 0:
        if rgx[0] == "(":
            rgx, nfa = group_RE(rgx, nfa, curr_state)
        elif rgx[0] == ".":
            rgx, nfa = any_RE(rgx, nfa, curr_state)
        elif rgx[0] == "$":
            rgx, nfa = eos_RE(rgx, nfa, curr_state)
        elif rgx[0] == "[":
            rgx, nfa = set_RE(rgx, nfa, curr_state)
        else:
            rgx, nfa = char_RE(rgx, nfa, curr_state)

    logging.debug("Out elementary:" + rgx)
    return rgx, nfa

def group_RE(rgx, nfa, curr_state):
    logging.debug("In group:" + rgx)
    if len(rgx) > 0:
        if rgx[0] == "(":
            rgx = next(rgx)
            rgx, nfa = RE(rgx, nfa, curr_state)
            if rgx[0] == ")":
                rgx = next(rgx)
            else:
                logging.critical("Error in group parse. Missing ')'")
                sys.exit(1)
        else:
            logging.critical("Error in group parse. Missing '('")
            sys.exit(1)

    logging.debug("Out group:" + rgx)
    return rgx, nfa

def any_RE(rgx, nfa, curr_state):
    logging.debug("In any:" + rgx)
    val_chars = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for l in val_chars:
        if l not in nfa.get_alphabet():
            nfa.add_to_ab(l)
    rgx = next(rgx)

    logging.debug("Out any:" + rgx)
    return rgx, nfa

def eos_RE(rgx, nfa, curr_state):
    logging.debug("In eos:" + rgx)
    rgx = next(rgx)

    logging.debug("Out eos:" + rgx)
    return rgx, nfa

def char_RE(rgx, nfa, curr_state):
    logging.debug("In char:" + rgx)
    char_patt = re.compile("[a-zA-Z0-9]")
    if len(rgx) > 0:
        if char_patt.match(rgx[0]):
            nfa.add_to_ab(rgx[0])
            rgx = next(rgx)
        else:
            logging.critical("Error in character parse. Invalid character")
            sys.exit(1)

    logging.debug("Out char:" + rgx)

    return rgx, nfa

def set_RE(rgx, nfa, curr_state):
    logging.debug("In set:" + rgx)
    if len(rgx) > 0:
        if rgx[0] == "[":
            if rgx[1] == "^":
                rgx, nfa = neg_set_RE(rgx, nfa, curr_state)
            else:
                rgx, nfa = pos_set_RE(rgx, nfa, curr_state)

    logging.debug("Out set:" + rgx)

    return rgx, nfa

def pos_set_RE(rgx, nfa, curr_state):
    logging.debug("In pos_set:" + rgx)
    if len(rgx) > 0:
        if rgx[0] == "[":
            rgx = next(rgx)
            rgx, nfa = set_items_RE(rgx, nfa, curr_state)
            if rgx[0] == "]":
                rgx = next(rgx)

    logging.debug("Out pos_set:" + rgx)

    return rgx, nfa

# IF I have [^a], is a part of the alphabet?
def neg_set_RE(rgx, nfa, curr_state):
    logging.debug("In neg_set:" + rgx)
    if len(rgx) > 0:
        if rgx[0] == "[":
            rgx = next(rgx)
            if rgx[0] == "^":
                rgx = next(rgx)
                rgx, nfa = set_items_RE(rgx, nfa, curr_state)
                if rgx[0] == "]":
                    rgx = next(rgx)

    logging.debug("Out neg_set:" + rgx)

    return rgx, nfa

# ------ Needs fixing --------
def set_items_RE(rgx, nfa, curr_state):
    logging.debug("In set_items:" + rgx)
    rgx, nfa = set_item_RE(rgx, nfa, curr_state)

    rgx, nfa = set_item_RE(rgx, nfa, curr_state)
    rgx, nfa = set_items_RE(rgx, nfa, curr_state)

    logging.debug("Out set_items:" + rgx)

    return rgx, nfa

def set_item_RE(rgx, nfa, curr_state):
    logging.debug("In set_item:" + rgx)
    rgx, nfa = range_RE(rgx, nfa, curr_state)
    #rgx, nfa = char_RE(rgx, nfa)

    logging.debug("Out set_item:" + rgx)
    return rgx, nfa

# Looks at char
# checks if range or just char
def range_RE(rgx, nfa, curr_state):
    logging.debug("In range:" + rgx)
    rgx, nfa = char_RE(rgx, nfa, curr_state)
    if len(rgx) > 0:
        if rgx[0] == "-":
            rgx = next(rgx)
            rgx, nfa = char_RE(rgx, nfa, curr_state)

    logging.debug("Out range:" + rgx)

    return rgx, nfa

# Regex parser
def RE(rgx, nfa, curr_state):
    logging.debug("In RE:" + rgx)
    #rgx, nfa = simple_RE(rgx, nfa, curr_state)
    #if re.match('^[a-zA-Z0-9]*$', rgx):
    if '|' in  rgx:
        rgx, nfa = union_RE(rgx, nfa, curr_state)
    else:
        rgx, nfa = simple_RE(rgx, nfa, curr_state)

    logging.debug("Out RE:" + rgx)
    return rgx, nfa
