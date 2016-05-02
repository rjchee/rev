# rev
```rev``` is a Python command line utility that aims to provide more string reversing functionality than the one that already exists.

Usage:
```sh
rev # Read strings line by line from standard input and reverse them
```

Reversing words:
```sh
rev -w # Reverse the word order
```
Blocks of texts are considered to be words if they are between whitespace or punctuation characters. These characters are called delimiters and can be edited with the flags ```--include-chars``` and ```--exclude-chars```. Delimiter characters are kept in the same relative place to preserve sentence structure.
```sh
echo "I'm cool" | rev -w # using default delimiters
cool'm I
echo "I'm cool" | rev -w --exclude-chars "'"
cool I'm
```

If the goal is to reverse both the word order and have each word be reversed, you can specify the ```-c``` flag to also reverse the characters in each word
```sh
rev -w -c # Reverse the word order and the characters in each word
```

Input:
```rev``` takes a positional argument to denote the name of the file to read in from.
```sh
rev file.txt # Output the contents of the file with each line reversed
```
The flag ```--ignore-newlines``` ignores newlines and reverses the entire string.
```sh
rev file.txt --ignore-newlines # Reverse everything in the file, ignoring newlines
```

The full usage is as follows:
```
usage: rev.py [-h] [-o OUT] [-w [W]] [--ignore-lines]
              [--include-chars INCLUDE_CHARS] [--exclude-chars EXCLUDE_CHARS]
              [-c [C]] [-b [B]]
              [IN]

Reverse the input

positional arguments:
  IN                    The input file (standard in by default)

optional arguments:
  -h, --help            show this help message and exit
  -o OUT, --output OUT  The output file (standard out by default)
  -w [W], --word [W]    Reverse W words at a time. Leaves delimiters
                        (whitespace and punctuation by default) intact.
                        (default W is 1, meaning all words are reversed)
  --ignore-lines        Ignore newlines when reversing (so that using standard
                        input delays output when you enter EOF, nothing is
                        actually changed in the output)
  --include-chars INCLUDE_CHARS
                        Use the characters as delimiters to split on.
  --exclude-chars EXCLUDE_CHARS
                        Do not use the characters provided as delimiters.
  -c [C], --character [C]
                        Reverse C characters at time. If --word is specified,
                        reverse the characters in a word, and leave the word
                        order intact if W is 1. (default C is 1, meaning all
                        characters are reversed)
  -b [B], --byte [B]    Reverse B bytes of the input (default B is 1, meaning
                        all bytes are reversed)
```
