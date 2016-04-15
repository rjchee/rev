import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Reverse the input")
    parser.add_argument('input', nargs='?', default=sys.stdin, type=argparse.FileType('r'), help="The input file (standard in by default)")

    
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

    parser.add_argument('-w', '--word', action=WordAction, type=positive_int, nargs='?', help="Reverse W words at a time. (default W is 1, meaning all words are reversed)", default=False, metavar='W')
    parser.add_argument('-c', '--character', action=CharacterAction,
            type=positive_int, nargs='?',
            help="Reverse C characters at time. If --word is specified, reverse the characters in a word. (default C is 1, meaning all characters are reversed)",
            default=True, metavar='C')
    parser.set_defaults(word_level=1, character_level=1)
    args = parser.parse_args()
