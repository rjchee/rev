import itertools
import string

__delimset = string.punctuation + string.whitespace

def split(text, delimset=__delimset):
    words = []
    delims = []
    lastword = ''
    lastdelim = ''
    for ch in text:
        if ch in delimset:
            if lastword:
                words.append(lastword)
                lastword = ''
            lastdelim += ch
        else:
            if lastdelim:
                delims.append(lastdelim)
                lastdelim = ''
            lastword += ch
    if lastword:
        words.append(lastword)
    elif lastdelim:
        delims.append(lastdelim)
    return words, delims


def merge(a, b, aFirst):
    if aFirst:
        return ''.join(item for pair in itertools.zip_longest(a, b, fillvalue='') for item in pair)
    return merge(b, a, True)


def rev(text, character, character_level, word, word_level, delimset=__delimset):
    if not text:
        return text
    if word:
        words, spaces = split(text, delimset)
        if word_level == 1 and not character:
            words = words[::-1]
        else:
            words = sum((words[x:x+word_level][::-1] for x in range(0, len(words), word_level)), [])
        if character:
            for i in range(len(words)):
                words[i] = rev(words[i], character, character_level, False, 1)
        res = merge(words, spaces, not text[0] in delimset)
    elif character:
        if character_level == 1:
            res = text[::-1]
        else:
            res = text[0:0].join(text[x:x+character_level][::-1] for x in range(0, len(text), character_level))
    return res


def _parse_args(args=None):
    import argparse
    import sys
    parser = argparse.ArgumentParser(description="Reverse the input")
    parser.add_argument('input', nargs='?', default=None, help="The input file (standard in by default)", metavar='IN')
    parser.add_argument('-o', '--output', default=None, help="The output file (standard out by default)", metavar='OUT')

    
    class WordAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, "word", True)
            if values is not None:
                setattr(namespace, "word_level", values)
            if getattr(namespace, "character") is None:
                setattr(namespace, "character", False)


    def get_action(name):
        class UnitAction(argparse.Action):
            def __call__(self, parser, namespace, values, option_string=None):
                if values is not None:
                    setattr(namespace, name + '_level', values)
                setattr(namespace, name, True)
        return UnitAction
    
    def positive_int(num):
        val = int(num)
        if val <= 0 or float(num) != int(num):
            raise argparse.ArgumentTypeError("level must be a positive integer")
        return val


    parser.add_argument('-w', '--word', action=WordAction, type=positive_int,
            help="Reverse W words at a time. Leaves delimiters (whitespace and punctuation by default) intact. (default W is 1, meaning all words are reversed)",
            nargs='?', default=False, metavar='W')

    parser.add_argument('--ignore-lines', action='store_true', default=False,
            help="Ignore newlines when reversing (so that using standard input delays output when you enter EOF, nothing is actually changed in the output)")

    parser.add_argument('--include-chars', default='', help="Use the characters as delimiters to split on.")
    parser.add_argument('--exclude-chars', default='', help="Do not use the characters provided as delimiters.")
    parser.add_argument('-c', '--character', action=get_action('character'),
            type=positive_int, nargs='?',
            help="Reverse C characters at time. If --word is specified, reverse the characters in a word, and leave the word order intact if W is 1. (default C is 1, meaning all characters are reversed)",
            default=None, metavar='C')

    byte_arg = parser.add_argument('-b', '--byte', action=get_action('byte'), type=positive_int,
            help="Reverse B bytes of the input (default B is 1, meaning all bytes are reversed)",
            nargs='?', default=False, metavar='B')

    parser.set_defaults(word_level=1, character_level=1, byte_level=1)
    parsed_args = parser.parse_args() if args is None else parser.parse_args(args)

    if parsed_args.byte and (parsed_args.word or parsed_args.character):
        raise argparse.ArgumentError(byte_arg, 'Cannot reverse by both bytes and utf strings! (the --byte flag cannot be used with the --word or --character flags)')

    if parsed_args.character is None and not parsed_args.byte:
        parsed_args.character = True

    if parsed_args.byte:
        parsed_args.input = sys.stdin.buffer if parsed_args.input is None else open(parsed_args.input, 'rb')
        parsed_args.output = sys.stdout.buffer if parsed_args.output is None else open(parsed_args.output, 'wb')
    else:
        parsed_args.input = sys.stdin if parsed_args.input is None else open(parsed_args.input, "r")
        parsed_args.output = sys.stdout if parsed_args.output is None else open(parsed_args.output, "w")
        parsed_args.delimset = ''.join(filter(lambda x: x not in parsed_args.exclude_chars, __delimset + parsed_args.include_chars))
    return parsed_args


def _rev_main(args):
    if args.byte:
        bytestr = args.input.read()
        yield rev(bytestr[:len(bytestr)-1], True, args.byte_level, False, 1)
    elif args.ignore_lines:
        text = args.input.read()
        yield rev(text[:len(text)-1], args.character, args.character_level,
                args.word, args.word_level, args.delimset)
    else:
        for line in args.input:
            yield rev(line[:len(line)-1], args.character, args.character_level,
                    args.word, args.word_level, args.delimset)


def main():
    args = _parse_args()
    import signal
    import sys
    def sigint_handler(signal, frame):
        if args.output == sys.stdout:
            print() # print a newline when ctrl+c happens
        sys.exit(0)
    signal.signal(signal.SIGINT, sigint_handler)


    for output_line in _rev_main(args):
        if args.byte:
            args.output.write(output_line)
        else:
            print(output_line, file=args.output)

if __name__ == '__main__':
    main()
