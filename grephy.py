'''
grephy.py

Usage:
  grephy.py [-h] [-n NFA_FILE] [-d DFA_FILE] REGEX-FILE
  
Description:
  A grep utility that searches files for regular expression
  pattern matches and produces dot graph file output for the
  automata used in the matching computation.

@author Jesse Opitz

Due Date: 05/07/18
'''

#!/usr/bin/env python

import argparse


def main():
    parser = argparse.ArgumentParser(description='Searches files for regular expression pattern matches.')
    
    parser.add_argument('-n', '--NFA-FILE', nargs=1, help='File for NFA')
    
    parser.add_argument('-d', '--DFA-FILE', nargs=1, help='File for DFA')

    parser.add_argument('REGEX-FILE', type=str, help='Regular expression file')

    args = parser.parse_args()

if __name__ == "__main__":
    main()
