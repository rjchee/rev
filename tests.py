import unittest
from reverse import merge
from reverse import split
from reverse import reverse


class TestSplit(unittest.TestCase):


    def test_split(self):
        self.assertEqual(split('abcd ef'), ('abcd ef'.split(), [' ']))
        self.assertEqual(split('123 14412\t\t 717\n\n\r\n'), ('123 14412\t\t 717\n\n\r\n'.split(), [' ', '\t\t ', '\n\n\r\n']))
        self.assertEqual(split('  123 14412\t\t 717\n\n\r\n'), ('  123 14412\t\t 717\n\n\r\n'.split(), ['  ', ' ', '\t\t ', '\n\n\r\n']))
        self.assertEqual(split('  123 14412\t\t 717\n\n\r\na'), ('  123 14412\t\t 717\n\n\r\na'.split(), ['  ', ' ', '\t\t ', '\n\n\r\n']))


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
        self.assertEqual(reverse('a b c d e f g', False, 1, True, 1), 'g f e d c b a')
        self.assertEqual(reverse('ab bc cd de ef fg gh', False, 1, True, 1), 'gh fg ef de cd bc ab')
        self.assertEqual(reverse('ab', False, 1, True, 1), 'ab')
        self.assertEqual(reverse('ab cd', False, 1, True, 1), 'cd ab')
        self.assertEqual(reverse('', False, 1, True, 1), '')
        self.assertEqual(reverse('reallyreallyreallyreallyreallylongword' * 10000, False, 1, True, 1), 'reallyreallyreallyreallyreallylongword' * 10000)
        self.assertEqual(reverse('12 345 543 21', False, 1, True, 1), '21 543 345 12')
        self.assertEqual(reverse('12 34 5195 43 21', False, 1, True, 1), '21 43 5195 34 12')


    
    def test_wordn(self):
        self.assertEqual(reverse('a b c d e f g', False, 1, True, 2), 'b a d c f e g')
        self.assertEqual(reverse('ab bc cd de ef fg gh', False, 1, True, 2), 'bc ab de cd fg ef gh')
        self.assertEqual(reverse('12 345 543 21', False, 1, True, 2), '345 12 21 543')
        self.assertEqual(reverse('12 34 5195 43 21', False, 1, True, 2), '34 12 43 5195 21')
        self.assertEqual(reverse('a b c d e f g', False, 1, True, 3), 'c b a f e d g')
        self.assertEqual(reverse('ab bc cd de ef fg gh', False, 1, True, 3), 'cd bc ab fg ef de gh')
        self.assertEqual(reverse('12 345 543 21', False, 1, True, 3), '543 345 12 21')
        self.assertEqual(reverse('12 34 5195 43 21', False, 1, True, 3), '5195 34 12 21 43')
        self.assertEqual(reverse('12 34 5195 43 21 000', False, 1, True, 3), '5195 34 12 000 21 43')


    def test_wordn_high_level(self):
        self.assertEqual(reverse('', False, 1, True, 2), '')
        self.assertEqual(reverse('', False, 1, True, 44), '')
        self.assertEqual(reverse('', False, 1, True, 100000), '')
        self.assertEqual(reverse('ab', False, 1, True, 2), 'ab')
        self.assertEqual(reverse('ab', False, 1, True, 44), 'ab')
        self.assertEqual(reverse('ab', False, 1, True, 100000), 'ab')
        self.assertEqual(reverse('ab cd', False, 1, True, 2), 'cd ab')
        self.assertEqual(reverse('ab cd', False, 1, True, 44), 'cd ab')
        self.assertEqual(reverse('ab cd', False, 1, True, 100000), 'cd ab')
        self.assertEqual(reverse('ab cd ef', False, 1, True, 100000), 'ef cd ab')

    def test_word_whitespace(self):
        self.assertEqual(reverse('ab\tcd', False, 1, True, 1), 'cd\tab')
        self.assertEqual(reverse('  ab\tcd', False, 1, True, 1), '  cd\tab')
        self.assertEqual(reverse('ab \t \t  cd', False, 1, True, 1), 'cd \t \t  ab')
        self.assertEqual(reverse('ab \t \t  cd         ', False, 1, True, 1), 'cd \t \t  ab         ')
        self.assertEqual(reverse('\t\r\t\n\f   \t \t\t', False, 1, True, 1), '\t\r\t\n\f   \t \t\t')
        self.assertEqual(reverse('\t\r\t\n\f   \t \t\t', False, 1, True, 500), '\t\r\t\n\f   \t \t\t')


    def test_word_newlines(self):
        self.assertEqual(reverse('ab\ncd\nef', False, 1, True, 1), 'ef\ncd\nab')
        self.assertEqual(reverse('ab\ncd\nef', False, 1, True, 2), 'cd\nab\nef')
        self.assertEqual(reverse('ab\ncd\nef', False, 1, True, 3), 'ef\ncd\nab')
        self.assertEqual(reverse('ab\ncd\nef', False, 1, True, 4), 'ef\ncd\nab')
        self.assertEqual(reverse('ab cd ef\nab cd ef\nab cd ef', False, 1, True, 1), 'ef cd ab\nef cd ab\nef cd ab')
        self.assertEqual(reverse('ab cd ef\nab cd ef\nab cd ef', False, 1, True, 2), 'cd ab ab\nef ef cd\ncd ab ef')
        self.assertEqual(reverse('ab cd ef\nab cd ef\nab cd ef', False, 1, True, 3), 'ef cd ab\nef cd ab\nef cd ab')
        self.assertEqual(reverse('ab cd ef\nab cd ef\nab cd ef', False, 1, True, 4), 'ab ef cd\nab cd ab\nef cd ef')
        self.assertEqual(reverse('ab cd ef\nab cd ef\nab cd ef', False, 1, True, 5), 'cd ab ef\ncd ab ef\ncd ab ef')
        self.assertEqual(reverse('ab cd ef\nab\nab cd', False, 1, True, 1), 'cd ab ab\nef\ncd ab')
        self.assertEqual(reverse('ab cd ef\nab\nab cd', False, 1, True, 2), 'cd ab ab\nef\ncd ab')
        self.assertEqual(reverse('ab cd ef\nab\nab cd', False, 1, True, 3), 'ef cd ab\ncd\nab ab')


    def test_character1(self):
        texts = ['abcdefg', 'aaaaa1a', '12', '@@@', 'a@a', '', 'z', 'reallyreallyreallyreallyreallyreallyreallylongword', 'longword' * 10000]
        for text in texts:
            self.assertEqual(reverse(text, True, 1, False, 1), text[::-1])
        self.assertEqual(reverse('50', True, 1, False, 1), '05')
        self.assertEqual(reverse('50 101', True, 1, False, 1), '101 05')
        self.assertEqual(reverse('50 13 81731', True, 1, False, 1), '13718 31 05')
        self.assertEqual(reverse(' \t\n', True, 1, False, 1), '\n\t ')


    def test_charactern(self):
        self.assertEqual(reverse('abcdefg', True, 3, False, 1), 'cbafedg')
        self.assertEqual(reverse('abcdefg', True, 4, False, 1), 'dcbagfe')
        self.assertEqual(reverse('abc defg', True, 2, False, 1), 'ba cedgf')
        self.assertEqual(reverse('abc defg', True, 3, False, 1), 'cbaed gf')
        self.assertEqual(reverse('abc defg', True, 4, False, 1), ' cbagfed')
        self.assertEqual(reverse('abc defg', True, 7, False, 1), 'fed cbag')
        self.assertEqual(reverse('abc defg', True, 8, False, 1), 'gfed cba')
        text = 'reallylongword' * 100
        self.assertEqual(reverse(text, True, len('reallylongword') * 50, False, 1), ('reallylongword' * 50)[::-1] * 2)


    def test_character_word11(self):
        self.assertEqual(reverse('abc def ghi', True, 1, True, 1), 'cba fed ihg')
        self.assertEqual(reverse('abcd ef ghi', True, 1, True, 1), 'dcba fe ihg')
        self.assertEqual(reverse('abcd iiiiiiiiiiiiiiii', True, 1, True, 1), 'dcba iiiiiiiiiiiiiiii')
        self.assertEqual(reverse('abc', True, 1, True, 1), 'cba')
        self.assertEqual(reverse('', True, 1, True, 1), '')
        self.assertEqual(reverse('abc\t', True, 1, True, 1), 'cba\t')
        self.assertEqual(reverse('\tabc ', True, 1, True, 1), '\tcba ')
        self.assertEqual(reverse('\tabc', True, 1, True, 1), '\tcba')


    def test_character_wordn1(self):
        self.assertEqual(reverse('abc def ghi', True, 2, True, 1), 'bac edf hgi')
        self.assertEqual(reverse('abcd defg ghij', True, 2, True, 1), 'badc edgf hgji')
        self.assertEqual(reverse('abcd defg ghij', True, 3, True, 1), 'cbad fedg ihgj')
        self.assertEqual(reverse('abcdef gh ijkl', True, 3, True, 1), 'cbafed hg kjil')
        self.assertEqual(reverse('abcdef\ngh \tijkl', True, 3, True, 1), 'cbafed\nhg \tkjil')
        self.assertEqual(reverse('abc def ghi', True, 500, True, 1), 'cba fed ihg')


    def test_character_word1n(self):
        self.assertEqual(reverse('abc def ghi', True, 1, True, 2), 'fed cba ihg')
        self.assertEqual(reverse('abc def ghi jkl', True, 1, True, 2), 'fed cba lkj ihg')
        self.assertEqual(reverse('\n   2134 17 8 8 8 8 8', True, 1, True, 3), '\n   8 71 4312 8 8 8 8')
        self.assertEqual(reverse('2134 17 8 8 8 8 8 ', True, 1, True, 3), '8 71 4312 8 8 8 8 ')
        self.assertEqual(reverse('abc def ghi', True, 1, True, 3), 'ihg fed cba')
        self.assertEqual(reverse('abc def ghi', True, 1, True, 500), 'ihg fed cba')


    def test_character_wordnn(self):
        self.assertEqual(reverse('abc def ghi', True, 2, True, 2), 'edf bac hgi')
        self.assertEqual(reverse('abcd defg ghij', True, 2, True, 2), 'edgf badc hgji')
        self.assertEqual(reverse('abcd defg ghij klmn', True, 2, True, 2), 'edgf badc lknm hgji')
        self.assertEqual(reverse('abc d efgh ij k lmnop qrstuv', True, 2, True, 3), 'fehg d bac mlonp k ji rqtsvu')
        self.assertEqual(reverse('abc d efgh ij k lmnop qrstuv', True, 3, True, 2), 'd cba ji gfeh nmlpo k srqvut')
        self.assertEqual(reverse(' abc\nd efgh ij k lmnop qrstuv', True, 3, True, 2), ' d\ncba ji gfeh nmlpo k srqvut')
        self.assertEqual(reverse('abc\td efgh ij k lmnop qrstuv\r \r', True, 3, True, 2), 'd\tcba ji gfeh nmlpo k srqvut\r \r')
        self.assertEqual(reverse('abc def ghi', True, 500, True, 2), 'fed cba ihg')
        self.assertEqual(reverse('abc def ghi', True, 2, True, 500), 'hgi edf bac')
        self.assertEqual(reverse('abc def ghi', True, 500, True, 500), 'ihg fed cba')
        self.assertEqual(reverse('abc def ghi\t', True, 500, True, 500), 'ihg fed cba\t')


if __name__ == '__main__':
    unittest.main()
