#!/usr/bin/env python

'''
grephy.py

Usage:
  grephy.py [-h] [-n NFA_FILE] [-d DFA_FILE] REGEX FILE

Description:
  A grep utility that searches files for regular expression
  pattern matches and produces dot graph file output for the
  automata used in the matching computation.

@author Jesse Opitz

Due Date: 05/07/18
'''

import argparse, logging, sys

def read_file(fname):
    try:
        with open(fname, 'r') as f:
            data = f.read();

        return data
    except IOError as e:
        logging.critical("FILE['{2}'] I/O error({0}): {1}".format(e.errno, e.strerror, fname))
        sys.exit(1)
    except:
        logging.critical("Unexpected error:", sys.exc_info()[0])
        raise
        sys.exit(1)

def get_alphabet(fname):
    alphabet = ''
    data = read_file(fname)
    for line in data:
        for c in line:
            if c not in alphabet:
                alphabet += c

    logging.debug("Alphabet: " + repr(alphabet))

    return alphabet

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')

    parser = argparse.ArgumentParser(description='Searches files for regular expression pattern matches.')
    
    parser.add_argument('-n', '--NFA-FILE', nargs=1, help='Output file for NFA')
    
    parser.add_argument('-d', '--DFA-FILE', nargs=1, help='Output file for DFA')

    #parser.add_argument('REGEX', type=str, help='Regular expression file')
    
    parser.add_argument('FILE', type=str, help='Input file')

    args = parser.parse_args()

    alphabet = get_alphabet(args.FILE)


if __name__ == "__main__":
    main()
