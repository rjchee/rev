import argparse
import sys


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Reverse the input")
    parser.add_argument('input', nargs='?', default=sys.stdin, type=argparse.FileType('r'), help="The input file (standard in by default)")

    
    class WordAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, "word", True)
            setattr(namespace, "word_level", values)
            setattr(namespace, "character", False)

    
    def positive_int(num):
        val = int(num)
        if val <= 0:
            raise argparse.ArgumentTypeError("level must be a positive integer")
        return val

    parser.add_argument('-w', '--word', action=WordAction, type=positive_int, nargs='?', help="Reverse L words at a time. (default 1)", default=False, metavar='L')
    parser.add_argument('-c', '--character', action='store_true', help="Reverse characters. If word is specified, reverse the characters in a word", default=True)
    parser.add_argument('-l', '--level', default=1, type=positive_int, help="the number of words or characters to reverse")
    args = parser.parse_args()
    print(args.input)
    print(args.word)
    print(args.character)
