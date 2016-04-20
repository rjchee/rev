import itertools

def split(text, delimset=".,?!:;(){}[]'\"/ \n\t\r\f\v"):
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


def rev(text, character, character_level, word, word_level, delimset=".,?!:;(){}[]'\"/ \n\t\r\f\v"):
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
            res = ''.join(text[x:x+character_level][::-1] for x in range(0, len(text), character_level))
    return res


def _parse_args(args=None):
    import argparse
    import sys
    parser = argparse.ArgumentParser(description="Reverse the input")
    parser.add_argument('input', nargs='?', default=sys.stdin, type=argparse.FileType('r'), help="The input file (standard in by default)")
    parser.add_argument('-o', '--output', nargs='?', default=sys.stdout, type=argparse.FileType('w'), help="The output file (standard out by default)")

    
    class WordAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, "word", True)
            if values is not None:
                setattr(namespace, "word_level", values)
            setattr(namespace, "character", False)


    class CharacterAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if values is not None:
                setattr(namespace, "character_level", values)
            setattr(namespace, "character", True)

    
    def positive_int(num):
        val = int(num)
        if val <= 0 or float(num) != int(num):
            raise argparse.ArgumentTypeError("level must be a positive integer")
        return val


    parser.add_argument('-w', '--word', action=WordAction,
            type=positive_int, nargs='?',
            help="Reverse W words at a time. Leaves whitespace intact. (default W is 1, meaning all words are reversed)",
            default=False, metavar='W')

    parser.add_argument('-c', '--character', action=CharacterAction,
            type=positive_int, nargs='?',
            help="Reverse C characters at time. If --word is specified, reverse the characters in a word, and leave the word order intact if W is 1. (default C is 1, meaning all characters are reversed)",
            default=True, metavar='C')

    parser.add_argument('--ignorelines', action='store_true', default=False,
            help="Ignore newlines when reversing (so that using standard input delays output when you enter EOF, nothing is actually changed in the output)")

    parser.set_defaults(word_level=1, character_level=1)
    if args is None:
        return parser.parse_args()
    return parser.parse_args(args)


def _rev_main(args):
    if args.ignorelines:
        text = args.input.read()
        yield rev(text[:len(text)-1], args.character, args.character_level, args.word, args.word_level)
    else:
        for line in args.input:
            yield rev(line[:len(line)-1], args.character, args.character_level, args.word, args.word_level)


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
        print(output_line, file=args.output)

if __name__ == '__main__':
    main()
