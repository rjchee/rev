import argparse
import contextlib
import os
from rev import merge
from rev import split
from rev import rev
from rev import _parse_args
import sys
import unittest


class TestSplit(unittest.TestCase):
    def test_split(self):
        self.assertEqual(split('abcd ef'), ('abcd ef'.split(), [' ']))
        self.assertEqual(split('123 14412\t\t 717\n\n\r\n'), ('123 14412\t\t 717\n\n\r\n'.split(), [' ', '\t\t ', '\n\n\r\n']))
        self.assertEqual(split('  123 14412\t\t 717\n\n\r\n'), ('  123 14412\t\t 717\n\n\r\n'.split(), ['  ', ' ', '\t\t ', '\n\n\r\n']))
        self.assertEqual(split('  123 14412\t\t 717\n\n\r\na'), ('  123 14412\t\t 717\n\n\r\na'.split(), ['  ', ' ', '\t\t ', '\n\n\r\n']))


    def test_split_delims(self):
        self.assertEqual(split('/root/home'), ('root home'.split(), ['/', '/']))
        self.assertEqual(split('www.github.com'), ('www github com'.split(), ['.', '.']))
        self.assertEqual(split('http://www.github.com'), ('http www github com'.split(), ['://', '.', '.']))
        self.assertEqual(split('Hi, what is your name?'), (['Hi', 'what', 'is', 'your', 'name'], [', ', ' ', ' ', ' ', '?']))


class TestMerge(unittest.TestCase):
    def test_merge(self):
        self.assertEqual(merge([], [], True), '')
        self.assertEqual(merge(['hi'], [], True), 'hi')
        self.assertEqual(merge([], ['\n'], True), '\n')
        self.assertEqual(merge([], [], False), '')
        self.assertEqual(merge(['hi'], [], False), 'hi')
        self.assertEqual(merge([], ['\n'], False), '\n')
        self.assertEqual(merge(['a', 'bcd', 'efg'], [' '] * 2, True), 'a bcd efg')
        self.assertEqual(merge(['a', 'bcd', 'efg'], [' '] * 3, True), 'a bcd efg ')
        self.assertEqual(merge(['ab'] * 100, [' '] * 99, True), ('ab ' * 100).strip())
        self.assertEqual(merge(['ab'] * 100, [' '] * 100, True), 'ab ' * 100)
        self.assertEqual(merge(['ab'] * 100, ['\t'] * 100, True), 'ab\t' * 100)
        self.assertEqual(merge(['ab'] * 100, ['\n'] * 100, True), 'ab\n' * 100)
        self.assertEqual(merge(['ab'] * 100, ['\t \n'] * 100, True), 'ab\t \n' * 100)
        self.assertEqual(merge(['a', 'bcd', 'efg'], [' '] * 3, False), ' a bcd efg')
        self.assertEqual(merge(['a', 'bcd', 'efg'], [' '] * 4, False), ' a bcd efg ')
        self.assertEqual(merge(['ab'] * 100, [' '] * 100, False), ' ab' * 100)
        self.assertEqual(merge(['ab'] * 99, [' '] * 100, False), (' ab' * 100)[:-2])
        self.assertEqual(merge(['ab'] * 99, ['\t'] * 100, False), ('\tab' * 100)[:-2])
        self.assertEqual(merge(['ab'] * 99, ['\t \n'] * 100, False), ('\t \nab' * 100)[:-2])


class TestReverse(unittest.TestCase):
    def test_word1(self):
        self.assertEqual(rev('a b c d e f g', False, 1, True, 1), 'g f e d c b a')
        self.assertEqual(rev('ab bc cd de ef fg gh', False, 1, True, 1), 'gh fg ef de cd bc ab')
        self.assertEqual(rev('ab', False, 1, True, 1), 'ab')
        self.assertEqual(rev('ab cd', False, 1, True, 1), 'cd ab')
        self.assertEqual(rev('', False, 1, True, 1), '')
        self.assertEqual(rev('reallyreallyreallyreallyreallylongword' * 10000, False, 1, True, 1), 'reallyreallyreallyreallyreallylongword' * 10000)
        self.assertEqual(rev('12 345 543 21', False, 1, True, 1), '21 543 345 12')
        self.assertEqual(rev('12 34 5195 43 21', False, 1, True, 1), '21 43 5195 34 12')


    
    def test_wordn(self):
        self.assertEqual(rev('a b c d e f g', False, 1, True, 2), 'b a d c f e g')
        self.assertEqual(rev('ab bc cd de ef fg gh', False, 1, True, 2), 'bc ab de cd fg ef gh')
        self.assertEqual(rev('12 345 543 21', False, 1, True, 2), '345 12 21 543')
        self.assertEqual(rev('12 34 5195 43 21', False, 1, True, 2), '34 12 43 5195 21')
        self.assertEqual(rev('a b c d e f g', False, 1, True, 3), 'c b a f e d g')
        self.assertEqual(rev('ab bc cd de ef fg gh', False, 1, True, 3), 'cd bc ab fg ef de gh')
        self.assertEqual(rev('12 345 543 21', False, 1, True, 3), '543 345 12 21')
        self.assertEqual(rev('12 34 5195 43 21', False, 1, True, 3), '5195 34 12 21 43')
        self.assertEqual(rev('12 34 5195 43 21 000', False, 1, True, 3), '5195 34 12 000 21 43')


    def test_wordn_high_level(self):
        self.assertEqual(rev('', False, 1, True, 2), '')
        self.assertEqual(rev('', False, 1, True, 44), '')
        self.assertEqual(rev('', False, 1, True, 100000), '')
        self.assertEqual(rev('ab', False, 1, True, 2), 'ab')
        self.assertEqual(rev('ab', False, 1, True, 44), 'ab')
        self.assertEqual(rev('ab', False, 1, True, 100000), 'ab')
        self.assertEqual(rev('ab cd', False, 1, True, 2), 'cd ab')
        self.assertEqual(rev('ab cd', False, 1, True, 44), 'cd ab')
        self.assertEqual(rev('ab cd', False, 1, True, 100000), 'cd ab')
        self.assertEqual(rev('ab cd ef', False, 1, True, 100000), 'ef cd ab')

    def test_word_whitespace(self):
        self.assertEqual(rev('ab\tcd', False, 1, True, 1), 'cd\tab')
        self.assertEqual(rev('  ab\tcd', False, 1, True, 1), '  cd\tab')
        self.assertEqual(rev('ab \t \t  cd', False, 1, True, 1), 'cd \t \t  ab')
        self.assertEqual(rev('ab \t \t  cd         ', False, 1, True, 1), 'cd \t \t  ab         ')
        self.assertEqual(rev('\t\r\t\n\f   \t \t\t', False, 1, True, 1), '\t\r\t\n\f   \t \t\t')
        self.assertEqual(rev('\t\r\t\n\f   \t \t\t', False, 1, True, 500), '\t\r\t\n\f   \t \t\t')


    def test_word_newlines(self):
        self.assertEqual(rev('ab\ncd\nef', False, 1, True, 1), 'ef\ncd\nab')
        self.assertEqual(rev('ab\ncd\nef', False, 1, True, 2), 'cd\nab\nef')
        self.assertEqual(rev('ab\ncd\nef', False, 1, True, 3), 'ef\ncd\nab')
        self.assertEqual(rev('ab\ncd\nef', False, 1, True, 4), 'ef\ncd\nab')
        self.assertEqual(rev('ab cd ef\nab cd ef\nab cd ef', False, 1, True, 1), 'ef cd ab\nef cd ab\nef cd ab')
        self.assertEqual(rev('ab cd ef\nab cd ef\nab cd ef', False, 1, True, 2), 'cd ab ab\nef ef cd\ncd ab ef')
        self.assertEqual(rev('ab cd ef\nab cd ef\nab cd ef', False, 1, True, 3), 'ef cd ab\nef cd ab\nef cd ab')
        self.assertEqual(rev('ab cd ef\nab cd ef\nab cd ef', False, 1, True, 4), 'ab ef cd\nab cd ab\nef cd ef')
        self.assertEqual(rev('ab cd ef\nab cd ef\nab cd ef', False, 1, True, 5), 'cd ab ef\ncd ab ef\ncd ab ef')
        self.assertEqual(rev('ab cd ef\nab\nab cd', False, 1, True, 1), 'cd ab ab\nef\ncd ab')
        self.assertEqual(rev('ab cd ef\nab\nab cd', False, 1, True, 2), 'cd ab ab\nef\ncd ab')
        self.assertEqual(rev('ab cd ef\nab\nab cd', False, 1, True, 3), 'ef cd ab\ncd\nab ab')


    def test_character1(self):
        texts = ['abcdefg', 'aaaaa1a', '12', '@@@', 'a@a', '', 'z', 'reallyreallyreallyreallyreallyreallyreallylongword', 'longword' * 10000]
        for text in texts:
            self.assertEqual(rev(text, True, 1, False, 1), text[::-1])
        self.assertEqual(rev('50', True, 1, False, 1), '05')
        self.assertEqual(rev('50 101', True, 1, False, 1), '101 05')
        self.assertEqual(rev('50 13 81731', True, 1, False, 1), '13718 31 05')
        self.assertEqual(rev(' \t\n', True, 1, False, 1), '\n\t ')


    def test_charactern(self):
        self.assertEqual(rev('abcdefg', True, 3, False, 1), 'cbafedg')
        self.assertEqual(rev('abcdefg', True, 4, False, 1), 'dcbagfe')
        self.assertEqual(rev('abc defg', True, 2, False, 1), 'ba cedgf')
        self.assertEqual(rev('abc defg', True, 3, False, 1), 'cbaed gf')
        self.assertEqual(rev('abc defg', True, 4, False, 1), ' cbagfed')
        self.assertEqual(rev('abc defg', True, 7, False, 1), 'fed cbag')
        self.assertEqual(rev('abc defg', True, 8, False, 1), 'gfed cba')
        text = 'reallylongword' * 100
        self.assertEqual(rev(text, True, len('reallylongword') * 50, False, 1), ('reallylongword' * 50)[::-1] * 2)


    def test_character_word11(self):
        self.assertEqual(rev('abc def ghi', True, 1, True, 1), 'cba fed ihg')
        self.assertEqual(rev('abcd ef ghi', True, 1, True, 1), 'dcba fe ihg')
        self.assertEqual(rev('abcd iiiiiiiiiiiiiiii', True, 1, True, 1), 'dcba iiiiiiiiiiiiiiii')
        self.assertEqual(rev('abc', True, 1, True, 1), 'cba')
        self.assertEqual(rev('', True, 1, True, 1), '')
        self.assertEqual(rev('abc\t', True, 1, True, 1), 'cba\t')
        self.assertEqual(rev('\tabc ', True, 1, True, 1), '\tcba ')
        self.assertEqual(rev('\tabc', True, 1, True, 1), '\tcba')


    def test_character_wordn1(self):
        self.assertEqual(rev('abc def ghi', True, 2, True, 1), 'bac edf hgi')
        self.assertEqual(rev('abcd defg ghij', True, 2, True, 1), 'badc edgf hgji')
        self.assertEqual(rev('abcd defg ghij', True, 3, True, 1), 'cbad fedg ihgj')
        self.assertEqual(rev('abcdef gh ijkl', True, 3, True, 1), 'cbafed hg kjil')
        self.assertEqual(rev('abcdef\ngh \tijkl', True, 3, True, 1), 'cbafed\nhg \tkjil')
        self.assertEqual(rev('abc def ghi', True, 500, True, 1), 'cba fed ihg')


    def test_character_word1n(self):
        self.assertEqual(rev('abc def ghi', True, 1, True, 2), 'fed cba ihg')
        self.assertEqual(rev('abc def ghi jkl', True, 1, True, 2), 'fed cba lkj ihg')
        self.assertEqual(rev('\n   2134 17 8 8 8 8 8', True, 1, True, 3), '\n   8 71 4312 8 8 8 8')
        self.assertEqual(rev('2134 17 8 8 8 8 8 ', True, 1, True, 3), '8 71 4312 8 8 8 8 ')
        self.assertEqual(rev('abc def ghi', True, 1, True, 3), 'ihg fed cba')
        self.assertEqual(rev('abc def ghi', True, 1, True, 500), 'ihg fed cba')


    def test_character_wordnn(self):
        self.assertEqual(rev('abc def ghi', True, 2, True, 2), 'edf bac hgi')
        self.assertEqual(rev('abcd defg ghij', True, 2, True, 2), 'edgf badc hgji')
        self.assertEqual(rev('abcd defg ghij klmn', True, 2, True, 2), 'edgf badc lknm hgji')
        self.assertEqual(rev('abc d efgh ij k lmnop qrstuv', True, 2, True, 3), 'fehg d bac mlonp k ji rqtsvu')
        self.assertEqual(rev('abc d efgh ij k lmnop qrstuv', True, 3, True, 2), 'd cba ji gfeh nmlpo k srqvut')
        self.assertEqual(rev(' abc\nd efgh ij k lmnop qrstuv', True, 3, True, 2), ' d\ncba ji gfeh nmlpo k srqvut')
        self.assertEqual(rev('abc\td efgh ij k lmnop qrstuv\r \r', True, 3, True, 2), 'd\tcba ji gfeh nmlpo k srqvut\r \r')
        self.assertEqual(rev('abc def ghi', True, 500, True, 2), 'fed cba ihg')
        self.assertEqual(rev('abc def ghi', True, 2, True, 500), 'hgi edf bac')
        self.assertEqual(rev('abc def ghi', True, 500, True, 500), 'ihg fed cba')
        self.assertEqual(rev('abc def ghi\t', True, 500, True, 500), 'ihg fed cba\t')


class TestParseArgs(unittest.TestCase):
    def test_no_args(self):
        args = _parse_args([])
        self.assertTrue(args.character)
        self.assertEqual(args.character_level, 1)
        self.assertFalse(args.word)
        self.assertFalse(args.byte)
        self.assertIs(args.input, sys.stdin)
        self.assertIs(args.output, sys.stdout)
        self.assertEqual(args.include_chars, '')
        self.assertEqual(args.exclude_chars, '')


    def test_io(self):
        import tempfile
        input_file = tempfile.NamedTemporaryFile(delete=False)
        input_file.write(b'testing testing')
        input_file.close()
        args = _parse_args([input_file.name])
        self.assertEqual(args.input.read(), 'testing testing')
        args.input.close()
        self.assertIs(args.output, sys.stdout)

        output_file = tempfile.NamedTemporaryFile(delete=False)
        args = _parse_args(['--output', output_file.name])
        args.output.write('abc def')
        args.output.close()
        self.assertEqual(output_file.read(), b'abc def')
        output_file.close()
        self.assertIs(args.input, sys.stdin)

        input_file = tempfile.NamedTemporaryFile(delete=False)
        input_file.write(b'this')
        input_file.close()
        output_file = tempfile.NamedTemporaryFile(delete=False)
        args = _parse_args([input_file.name, '--output', output_file.name])
        self.assertEqual(args.input.read(), 'this')
        args.input.close()
        args.output.write('that')
        args.output.close()
        self.assertEqual(output_file.read(), b'that')
        output_file.close()

        same_file = tempfile.NamedTemporaryFile(delete=False)
        args = _parse_args(['--output', same_file.name, same_file.name])
        args.output.write('goodbye')
        args.output.close()
        self.assertEqual(same_file.read(), b'goodbye')
        same_file.write(b'hello')
        same_file.close()
        self.assertEqual(args.input.read(), 'goodbyehello')
        args.input.close()


    def test_character_args(self):
        args = _parse_args(['-c'])
        self.assertTrue(args.character)
        self.assertEqual(args.character_level, 1)
        self.assertFalse(args.word)
        self.assertFalse(args.byte)
        self.assertIs(args.input, sys.stdin)
        self.assertIs(args.output, sys.stdout)

        args = _parse_args(['--character'])
        self.assertTrue(args.character)
        self.assertEqual(args.character_level, 1)
        self.assertFalse(args.word)
        self.assertFalse(args.byte)

        args = _parse_args(['-c 24'])
        self.assertTrue(args.character)
        self.assertEqual(args.character_level, 24)
        self.assertFalse(args.word)
        self.assertFalse(args.byte)


    def test_word_args(self):
        args = _parse_args(['-w'])
        self.assertFalse(args.character)
        self.assertTrue(args.word)
        self.assertEqual(args.word_level, 1)
        self.assertFalse(args.byte)
        self.assertFalse(args.ignore_lines)
        self.assertIs(args.input, sys.stdin)
        self.assertIs(args.output, sys.stdout)

        args = _parse_args(['--word'])
        self.assertFalse(args.character)
        self.assertTrue(args.word)
        self.assertEqual(args.word_level, 1)
        self.assertFalse(args.byte)

        args = _parse_args('--word 3'.split())
        self.assertFalse(args.character)
        self.assertTrue(args.word)
        self.assertEqual(args.word_level, 3)
        self.assertFalse(args.byte)

    def test_wc(self):
        args = _parse_args('-w -c'.split())
        self.assertTrue(args.word)
        self.assertEqual(args.word_level, 1)
        self.assertTrue(args.character)
        self.assertEqual(args.character_level, 1)
        self.assertFalse(args.ignore_lines)

        args = _parse_args('-c --word'.split())
        self.assertTrue(args.word)
        self.assertEqual(args.word_level, 1)
        self.assertTrue(args.character)
        self.assertEqual(args.character_level, 1)
        self.assertFalse(args.ignore_lines)

        args = _parse_args('--word -c 10 --ignore-lines'.split())
        self.assertTrue(args.word)
        self.assertEqual(args.word_level, 1)
        self.assertTrue(args.character)
        self.assertEqual(args.character_level, 10)
        self.assertTrue(args.ignore_lines)

        args = _parse_args('--ignore-lines -c 3 --word 10'.split())
        self.assertTrue(args.word)
        self.assertEqual(args.word_level, 10)
        self.assertTrue(args.character)
        self.assertEqual(args.character_level, 3)
        self.assertTrue(args.ignore_lines)


    def test_bytes(self):
        args =  _parse_args(['-b'])
        self.assertTrue(args.byte)
        self.assertEqual(args.byte_level, 1)
        self.assertFalse(args.character)
        self.assertFalse(args.word)
        self.assertIs(args.input, sys.stdin.buffer)
        self.assertIs(args.output, sys.stdout.buffer)

        args =  _parse_args(['--byte'])
        self.assertTrue(args.byte)
        self.assertEqual(args.byte_level, 1)
        self.assertFalse(args.character)
        self.assertFalse(args.word)

        args =  _parse_args('--byte 4'.split())
        self.assertTrue(args.byte)
        self.assertEqual(args.byte_level, 4)
        self.assertFalse(args.character)
        self.assertFalse(args.word)


    @contextlib.contextmanager
    def _nostderr():
        old_stderr = sys.stderr
        sys.stderr = open(os.devnull, 'w')
        try:
            yield
        finally:
            sys.stderr.close()
            sys.stderr = old_stderr


    @classmethod
    def _parse_err(cls, arg_str):
        with cls._nostderr():
            _parse_args(arg_str.split())


    def test_err(self):
        with self.assertRaises(argparse.ArgumentError):
            self._parse_err('-b -w')
        with self.assertRaises(argparse.ArgumentError):
            self._parse_err('-b -c')
        with self.assertRaises(argparse.ArgumentError):
            self._parse_err('-c -b')
        with self.assertRaises(argparse.ArgumentError):
            self._parse_err('-w -b')
        with self.assertRaises(SystemExit):
            self._parse_err('-w 0')
        with self.assertRaises(SystemExit):
            self._parse_err('-w 1.3')
        with self.assertRaises(SystemExit):
            self._parse_err('-c 0')
        with self.assertRaises(SystemExit):
            self._parse_err('-c 1.3')
        with self.assertRaises(SystemExit):
            self._parse_err('-c -1.3')
        with self.assertRaises(SystemExit):
            self._parse_err('-c -1')
        with self.assertRaises(SystemExit):
            self._parse_err('-b -1')
        with self.assertRaises(SystemExit):
            self._parse_err('-b 0')
        with self.assertRaises(SystemExit):
            self._parse_err('-b 1.3')
        with self.assertRaises(SystemExit):
            self._parse_err('-w --include-chars')
        with self.assertRaises(SystemExit):
            self._parse_err('-w --exclude-chars')


    def test_delims(self):
        args = _parse_args('-w --include-chars !abcdefghi'.split())
        self.assertEqual(set(ch for ch in args.include_chars), set(ch for ch in "!abcdefghi"))
        self.assertEqual(set(ch for ch in args.exclude_chars), set())
        self.assertTrue(args.word)
        self.assertEqual(args.word_level, 1)
        for ch in '!abcdefghi':
            self.assertTrue(ch in args.delimset)

        args = _parse_args(['--word', '--exclude-chars', "./, \n\ta"])
        self.assertEqual(set(ch for ch in args.exclude_chars), set(ch for ch in "./, \n\ta"))
        self.assertEqual(set(ch for ch in args.include_chars), set())
        self.assertTrue(args.word)
        self.assertEqual(args.word_level, 1)
        for ch in "./, \n\ta":
            self.assertFalse(ch in args.delimset)

        args = _parse_args('--include-chars 012345678 --exclude-chars $%@!# -w 4'.split())
        self.assertEqual(set(ch for ch in args.exclude_chars), set(ch for ch in "$%@!#"))
        self.assertEqual(set(ch for ch in args.include_chars), set(str(i) for i in range(9)))
        self.assertTrue(args.word)
        self.assertEqual(args.word_level, 4)
        for i in range(9):
            self.assertTrue(str(i) in args.delimset)
        for ch in "$%@!#":
            self.assertFalse(ch in args.delimset)


if __name__ == '__main__':
    unittest.main()
