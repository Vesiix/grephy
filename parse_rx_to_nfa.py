#!/usr/bin/env python

# TODO: Complete regex for lists and groups

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
                if (p+1) < len(rx):
                    if rx[p+1] != '*' and rx[p+1] != '+':
                        # Make a new transition to the letter
                        nfa, p, curr_state = parse_char(rx, nfa, p, curr_state)
                    elif rx[p+1] == '*':
                        nfa, p, curr_state = parse_star(rx, nfa, p, curr_state)
                        # Jump letter and star/plus
                        p = p + 2
                    elif rx[p+1] == '+':
                        nfa, p, curr_state = parse_plus(rx, nfa, p, curr_state)
                        # Jump letter and star/plus
                        p = p + 2
                else:
                    # This is fine, doesn't have to check for * or + when its last character
                    nfa, p, curr_state = parse_char(rx, nfa, p, curr_state)
            elif rx[p] == '[':
                # If it's a set

                p += 1
                
                # Grabs all characters between square braces
                # into char_list. Then, translates any ranges
                # into usable characters in true_chars and adds
                # all viable chars into true_chars.
                char_list = ''
                
                while not (rx[p] == ']'):
                    char_list += rx[p]
                    p += 1

                if '-' in char_list:
                    c = 0

                    true_chars = ''

                    while c < len(char_list):
                        if c+1 < len(char_list):
                            if char_list[c+1] == '-':
                                first_char = ord(char_list[c])
                                second_char = ord(char_list[c+2])
                                while first_char <= second_char:
                                    true_chars += chr(first_char)
                                    first_char += 1
                                c += 2
                            else:
                                true_chars += char_list[c]
                        else:
                            true_chars += char_list[c]
                        c += 1
                else:
                    true_chars = char_list

                next_state = nfa.get_next_state()

                if p+1 < len(rx):
                    if rx[p+1] == '*':
                        # 0 or more
                        nfa, p, curr_state = parse_star(rx, nfa, p, curr_state, square=True, char_list=true_chars)
                        p = p+2
                    elif rx[p+1] == '+':
                        # 1 or more
                        nfa, p, curr_state = parse_plus(rx, nfa, p, curr_state, square=True, char_list=true_chars)
                        p = p+2
                    else:
                        # Regular characters
                        nfa.add_state('q' + str(nfa.get_next_state()), False, True)

                        for char in true_chars:
                            # Add to alphabet and create transition for each character
                            nfa.add_to_ab(char)
                            nfa.add_transition(char, 'q' + str(curr_state), 'q' + str(next_state))

                        curr_state = next_state

                        p += 1
		else:
                    nfa.add_state('q' + str(nfa.get_next_state()), False, False)

                    for char in true_chars:
                        # Add to alphabet and create transition for each character
                        nfa.add_to_ab(char)
                        nfa.add_transition(char, 'q' + str(curr_state), 'q' + str(next_state))
                    
                    curr_state = next_state

                    p += 1

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

    p += 1

    logging.debug("Out char:" + str(p) + " curr_state:" + str(curr_state))

    return nfa, p, curr_state

def parse_star(rx, nfa, p, curr_state, square=False, paren=False, char_list=[]):
    logging.debug("In star:" + str(p) + " curr_state:" + str(curr_state))
    
    # Save start state
    start_state = curr_state

    # First epsilon transition
    nfa.add_state('q' + str(nfa.get_next_state()), False, False)
    nfa.add_transition('Eps', 'q' + str(curr_state), 'q' + str(nfa.get_next_state()-1))
    curr_state = nfa.get_next_state()-1

    # Save state before character
    state_before_char = curr_state

    # Character transition
    if square:
        nfa.add_state('q' + str(nfa.get_next_state()), False, False)
        for char in char_list:
            nfa.add_to_ab(char)
            nfa.add_transition(char, 'q' + str(curr_state), 'q' + str(nfa.get_next_state()-1))
        curr_state = nfa.get_next_state()-1

    elif paren:
	nfa.add_state('q' + str(nfa.get_next_state()), False, False)
        for char in char_list:
            nfa.add_to_ab(char)
            nfa.add_transition(char, 'q' + str(curr_state), 'q' + str(nfa.get_next_state()-1))
            curr_state = nfa.get_next_state()-1
    else:
        # Add letter to alphabet
        nfa.add_to_ab(rx[p])

        nfa.add_state('q' + str(nfa.get_next_state()), False, False)
        nfa.add_transition(rx[p], 'q' + str(curr_state), 'q' + str(nfa.get_next_state()-1))
        curr_state = nfa.get_next_state()-1

    # Second Epsilon transition
    if p+2 < len(rx):
        nfa.add_state('q' + str(nfa.get_next_state()), False, False)
    else:
        nfa.add_state('q' + str(nfa.get_next_state()), False, True)
    
    nfa.add_transition('Eps', 'q' + str(curr_state), 'q' + str(nfa.get_next_state()-1))
    curr_state = nfa.get_next_state()-1 

    # loopback epsilon transitions
    nfa.add_transition('Eps', 'q' + str(curr_state), 'q' + str(state_before_char))
    nfa.add_transition('Eps', 'q' + str(start_state), 'q' + str(curr_state))
    
    logging.debug("Out star:" + str(p) + " curr_state:" + str(curr_state))

    return nfa, p, curr_state

def parse_plus(rx, nfa, p, curr_state, square=False, paren=False, char_list=[]):
    logging.debug("In plus:" + str(p) + " curr_state:" + str(curr_state))
    
    # Add letter to alphabet
    nfa.add_to_ab(rx[p])

    # Save start state
    start_state = curr_state

    # First epsilon transition
    nfa.add_state('q' + str(nfa.get_next_state()), False, False)
    nfa.add_transition('Eps', 'q' + str(curr_state), 'q' + str(nfa.get_next_state()-1))
    curr_state = nfa.get_next_state()-1

    # Save state before character
    state_before_char = curr_state

    # Character transition
    if square:
        nfa.add_state('q' + str(nfa.get_next_state()), False, False)
        for char in char_list:
            nfa.add_to_ab(char)
            nfa.add_transition(char, 'q' + str(curr_state), 'q' + str(nfa.get_next_state()-1))

        curr_state = nfa.get_next_state()-1

    elif paren:
        nfa.add_state('q' + str(nfa.get_next_state()), False, False)
        for char in char_list:
            nfa.add_to_ab(char)
            nfa.add_transition(char, 'q' + str(curr_state), 'q' + str(nfa.get_next_state()-1))
            curr_state = nfa.get_next_state()-1
    else:
        nfa.add_state('q' + str(nfa.get_next_state()), False, False)
        nfa.add_transition(rx[p], 'q' + str(curr_state), 'q' + str(nfa.get_next_state()-1))
        curr_state = nfa.get_next_state()-1

    # Second Epsilon transition
    if p+2 < len(rx):
        nfa.add_state('q' + str(nfa.get_next_state()), False, False)
    else:
        nfa.add_state('q' + str(nfa.get_next_state()), False, True)

    nfa.add_transition('Eps', 'q' + str(curr_state), 'q' + str(nfa.get_next_state()-1))
    curr_state = nfa.get_next_state()-1

    # loopback epsilon transitions
    nfa.add_transition('Eps', 'q' + str(curr_state), 'q' + str(state_before_char))

    logging.debug("Out plus:" + str(p) + " curr_state:" + str(curr_state))

    return nfa, p, curr_state

