# grephy
A python2.7 grep utility that searches files for regular expression pattern matches and produces dot graph file output for the automata used in the matching computation.

# Usage
```
grephy.py [-h] [-n NFA_FILE] [-d DFA_FILE] REGEX-FILE

Searches files for regular expression pattern matches.

positional arguments:
  REGEX-FILE            Regular expression file

optional arguments:
  -h, --help            show this help message and exit
  -n NFA_FILE, --NFA-FILE NFA_FILE
                        File for NFA
  -d DFA_FILE, --DFA-FILE DFA_FILE
                        File for DFA
```