# grephy
A python2.7 grep utility that searches files for regular expression pattern matches and produces dot graph file output for the automata used in the matching computation.

# Usage
```
usage: grephy.py [-h] [-n NFA_FILE] [-d DFA_FILE] [-p] REGEX FILE

Searches files for regular expression pattern matches.

positional arguments:
  REGEX                 Regular expression file
  FILE                  Input file

optional arguments:
  -h, --help            show this help message and exit
  -n NFA_FILE, --NFA-FILE NFA_FILE
                        Output file for NFA
  -d DFA_FILE, --DFA-FILE DFA_FILE
                        Output file for DFA
  -p, --preview         Opens a pdf view of DFA and NFA
```

# Requirements
```
This python2.7 program requires the basic python libraries and graphviz.
```

# Examples

Command: 
```
./grephy.py "hel*o" test.txt
````
Output:
```
hello
```

Command:
```
./grephy.py -p "hel*o" test.txt
```
Output:
```
hello

**Note: This will return the same command line output, while also popping up PDFs of the NFA and DFA
```
