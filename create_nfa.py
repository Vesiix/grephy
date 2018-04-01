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

    rgx, nfa = RE(rgx, nfa)
    
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

def union_RE(rgx, nfa):
    logging.debug("In union:" + rgx)
    rgx, nfa = RE(rgx, nfa)
    if len(rgx) > 0:
        if rgx[0] == "|":
            # Create transition/nodes
            rgx = next(rgx)
            rgx, nfa = simple_RE(rgx, nfa)
        else:
            logging.critical("Error in union parse.")

    logging.debug("Out union:" + rgx)

    return rgx, nfa

def simple_RE(rgx, nfa):
    logging.debug("In simple:" + rgx)
    #simple_first_set = re.compile("[\*\+\(\.\$a-zA-Z0-9\\\[]") 
    simple_first_set = re.compile("[\*\+\.\(\$\[a-zA-Z0-9]")
    # HOW DO YOU DIFFERENTIATE THESE???
    if len(rgx) > 0:
        if simple_first_set.match(rgx[0]):
            rgx, nfa = basic_RE(rgx, nfa)
        else:
            rgx, nfa = concat_RE(rgx, nfa)
 
    logging.debug("Out simple:" + rgx)

    return rgx, nfa

def concat_RE(rgx, nfa):
    logging.debug("In concat:" + rgx)
    rgx, nfa = simple_RE(rgx, nfa)
    rgx, nfa = basic_RE(rgx, nfa)
    
    logging.debug("Out concat:" + rgx)

    return rgx, nfa

def basic_RE(rgx, nfa):
    logging.debug("In basic:" + rgx)
    rgx, nfa = elementary_RE(rgx, nfa)
    if len(rgx) > 0:
        if rgx[0] == "*":
            rgx, nfa = star_RE(rgx, nfa)
        elif rgx[0] == "+":
            rgx, nfa = plus_RE(rgx, nfa)
    logging.debug("Out basic:" + rgx)

    return rgx, nfa

def star_RE(rgx, nfa):
    logging.debug("In star:" + rgx)
    rgx = next(rgx)
    logging.debug("Out star:" + rgx)

    return rgx, nfa

def plus_RE(rgx, nfa):
    logging.debug("In plus:" + rgx)
    rgx = next(rgx)
    logging.debug("Out plus:" + rgx)

    return rgx, nfa

def elementary_RE(rgx, nfa):
    logging.debug("In elementary:" + rgx)
    if len(rgx) > 0:
        if rgx[0] == "(":
            rgx, nfa = group_RE(rgx, nfa)
        elif rgx[0] == ".":
            rgx, nfa = any_RE(rgx, nfa)
        elif rgx[0] == "$":
            rgx, nfa = eos_RE(rgx, nfa)
        elif rgx[0] == "[":
            rgx, nfa = set_RE(rgx, nfa)
        else:
            rgx, nfa = char_RE(rgx, nfa)

    logging.debug("Out elementary:" + rgx)
    return rgx, nfa

def group_RE(rgx, nfa):
    logging.debug("In group:" + rgx)
    if len(rgx) > 0:
        if rgx[0] == "(":
            rgx = next(rgx)
            rgx, nfa = RE(rgx, nfa)
            if rgx[0] == ")":
                rgx = next(rgx)
            else:
                logging.critical("Error in group parse. Missing ')'")
        else:
            logging.critical("Error in group parse. Missing '('")

    logging.debug("Out group:" + rgx)
    return rgx, nfa

def any_RE(rgx, nfa):
    logging.debug("In any:" + rgx)
    aToz = 'abcdefghijklmnopqrstuvwxyz'
    for l in aToz:
        if l not in nfa.get_alphabet():
            nfa.add_to_ab(l)
    rgx = next(rgx)

    logging.debug("Out any:" + rgx)
    return rgx, nfa

def eos_RE(rgx, nfa):
    logging.debug("In eos:" + rgx)
    rgx = next(rgx)

    logging.debug("Out eos:" + rgx)
    return rgx, nfa

def char_RE(rgx, nfa):
    logging.debug("In char:" + rgx)
    char_patt = re.compile("[a-zA-Z0-9]")
    if len(rgx) > 0:
        if char_patt.match(rgx[0]):
            nfa.add_to_ab(rgx[0])
            rgx = next(rgx)
        else:
            logging.critical("Error in character parse. Invalid character")

    logging.debug("Out char:" + rgx)

    return rgx, nfa

def set_RE(rgx, nfa):
    logging.debug("In set:" + rgx)
    if len(rgx) > 0:
        if rgx[0] == "[":
            if rgx[1] == "^":
                rgx, nfa = neg_set_RE(rgx, nfa)
            else:
                rgx, nfa = pos_set_RE(rgx, nfa)

    logging.debug("Out set:" + rgx)

    return rgx, nfa

def pos_set_RE(rgx, nfa):
    logging.debug("In pos_set:" + rgx)
    if len(rgx) > 0:
        if rgx[0] == "[":
            rgx = next(rgx)
            rgx, nfa = set_items_RE(rgx, nfa)
            if rgx[0] == "]":
                rgx = next(rgx)

    logging.debug("Out pos_set:" + rgx)

    return rgx, nfa

def neg_set_RE(rgx, nfa):
    logging.debug("In neg_set:" + rgx)
    if len(rgx) > 0:
        if rgx[0] == "[":
            rgx = next(rgx)
            if rgx[0] == "^":
                rgx = next(rgx)
                rgx, nfa = set_items_RE(rgx, nfa)
                if rgx[0] == "]":
                    rgx = next(rgx)

    logging.debug("Out neg_set:" + rgx)

    return rgx, nfa

# ------ Needs fixing --------
def set_items_RE(rgx, nfa):
    logging.debug("In set_items:" + rgx)
    rgx, nfa = set_item_RE(rgx, nfa)

    rgx, nfa = set_item_RE(rgx, nfa)
    rgx, nfa = set_items_RE(rgx, nfa)

    logging.debug("Out set_items:" + rgx)

    return rgx, nfa

def set_item_RE(rgx, nfa):
    logging.debug("In set_item:" + rgx)
    rgx, nfa = range_RE(rgx, nfa)
    #rgx, nfa = char_RE(rgx, nfa)

    logging.debug("Out set_item:" + rgx)
    return rgx, nfa

# Looks at char
# checks if range or just char
def range_RE(rgx, nfa):
    logging.debug("In range:" + rgx)
    rgx, nfa = char_RE(rgx, nfa)
    if len(rgx) > 0:
        if rgx[0] == "-":
            rgx = next(rgx)
            rgx, nfa = char_RE(rgx, nfa)

    logging.debug("Out range:" + rgx)

    return rgx, nfa

# Regex parser
def RE(rgx, nfa):
    logging.debug("In RE:" + rgx)
    rgx, nfa = simple_RE(rgx, nfa)
    if re.match('^[a-zA-Z0-9]*$', rgx):
        rgx, nfa = simple_RE(rgx, nfa)
    else:
        rgx, nfa = union_RE(rgx, nfa)

    logging.debug("Out RE:" + rgx)
    return rgx, nfa
