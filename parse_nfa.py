#!/usr/bin/env python

import re, sys, logging

# rx is regex
# p is pointer
# curr_state is current state
def parse_RE(rx, nfa, p, curr_state):
    if '|' in rx:
        # if there's a union, split it up into pieces
        rx_list = rx.split('|')
        for x in rx_list:
            parse_RE(x, nfa, 0, 0)
    else:
        while p < len(rx):
            if re.match("[a-zA-Z0-9]", rx[p]):
                # If it's a character
                #try:
                if (p+1) < len(rx):
                    if rx[p+1] != '*' and rx[p+1] != '+':
                        # Make a new transition to the letter
                        nfa, p, curr_state = parse_char(rx, nfa, p, curr_state)
                    elif rx[p+1] == '*':
                        nfa, p, curr_state = parse_star(rx, nfa, p, curr_state)
                    elif rx[p+1] == '+':
                        nfa, p, curr_state = parse_plus(rx, nfa, p, curr_state)
                #except IndexError:
                else:
                    #print("Unexpected error:", sys.exc_info()[0])
                    # This is fine, doesn't have to check for * or + when its last character
                    nfa, p, curr_state = parse_char(rx, nfa, p, curr_state)
            elif rx[p] == '[':
                # If it's a set
                print "["
            elif rx[p] == '(':
                # If it's a group
                print "("

    return nfa

def parse_char(rx, nfa, p, curr_state):
    logging.debug("In char:" + str(p) + " curr_state:" + str(curr_state))
    
    nfa.add_to_ab(rx[p])
    if len(rx) > p+1:
        # If pointer isn't at the end
        nfa.add_state('q' + str(nfa.get_next_state()), False, False)
    else:
        # If pointer is at the end
        # -> Make accepting state
        nfa.add_state('q' + str(nfa.get_next_state()), False, True)
    
    nfa.add_transition(rx[p], 'q' + str(curr_state), 'q' + str(nfa.get_next_state()-1))
    
    curr_state = nfa.get_next_state()-1

    #nfa.next_state = nfa.get_next_state() + 1
    p += 1

    logging.debug("Out char:" + str(p) + " curr_state:" + str(curr_state))

    return nfa, p, curr_state

def parse_star(rx, nfa, p, curr_state):
    logging.debug("In star:" + str(p) + " curr_state:" + str(curr_state))
    
    # Add letter to alphabet
    nfa.add_to_ab(rx[p])
    
    nfa, p, curr_state = loop(rx, nfa, p, curr_state)    

    #nfa.add_transition(rx[p], 'q' + str(curr_state), 'q' + str(curr_state))
    #if len(rx) == p+2:
        # If the star is the last character
        # -> Make curr_state accepting
   #     nfa.set_acc_state('q' + str(curr_state))

    # Jump letter and star
    #p = p + 2
    
    logging.debug("Out star:" + str(p) + " curr_state:" + str(curr_state))

    return nfa, p, curr_state

def parse_plus(rx, nfa, p, curr_state):
    logging.debug("In plus:" + str(p) + " curr_state:" + str(curr_state))
    
    nfa, p, curr_state = parse_char(rx, nfa, p, curr_state)

    nfa, p, curr_state = loop(rx, nfa, p-1, curr_state)
    #nfa.add_to_ab(rx[p]) 
    #nfa.add_transition(rx[p], 'q' + str(curr_state), 'q' + str(nfa.get_next_state()-1))
    #curr_state += nfa.get_next_state() - 1
    #nfa.next_state = nfa.get_next_state()
    
    
    logging.debug("Out plus:" + str(p) + " curr_state:" + str(curr_state))

    return nfa, p, curr_state

def loop(rx, nfa, p, curr_state):
    logging.debug("In loop:" + str(p) + " curr_state:" + str(curr_state))

    nfa.add_transition(rx[p], 'q' + str(curr_state), 'q' + str(curr_state))
    if len(rx) == p+2:
        # If the star is the last character
        # -> Make curr_state accepting
        nfa.set_acc_state('q' + str(curr_state))

    # Jump letter and star/plus
    p = p + 2 

    logging.debug("Out loop:" + str(p) + " curr_state:" + str(curr_state))
    
    return nfa, p, curr_state
