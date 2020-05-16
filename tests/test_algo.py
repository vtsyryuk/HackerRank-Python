import unittest

from nose.tools import assert_equal
from parameterized import parameterized


class TestAlgo(unittest.TestCase):
    @staticmethod
    def isWeird(n):
        if n % 2 != 0 or 6 <= n <= 20:
            return "Weird"
        else:
            return "Not Weird"

    @staticmethod
    def is_leap(year):
        if 1900 <= year <= 100000:
            if year % 4 == 0:
                if year % 100 == 0 and year % 400 != 0:
                    return False
                return True
        return False

    @parameterized.expand([
        (1, "Weird"),
        (2, "Not Weird"),
        (3, "Weird"),
        (4, "Not Weird"),
        (5, "Weird"),
        (6, "Weird"),
        (7, "Weird"),
        (8, "Weird"),
        (20, "Weird"),
        (21, "Weird"),
        (22, "Not Weird"),
        (23, "Weird"),
        (24, "Not Weird")
    ])
    def test_something(self, num, expected):
        assert_equal(self.isWeird(num), expected)

    def test_leap_year(self):
        assert_equal(False, self.is_leap(1900))
        assert_equal(True, self.is_leap(2000))
        assert_equal(True, self.is_leap(2400))
        assert_equal(False, self.is_leap(1800))
        assert_equal(False, self.is_leap(2100))
        assert_equal(False, self.is_leap(2200))
        assert_equal(False, self.is_leap(2300))
        assert_equal(False, self.is_leap(2500))

    @staticmethod
    def wrap(string, max_width):
        length = len(string)
        blocks = length // max_width
        lines = []
        for i in range(blocks):
            start = max_width * i
            end = max_width * i + max_width
            lines.append(string[start:end])
        end_range = max_width * blocks
        if end_range < length:
            lines.append(string[end_range:length])
        return lines

    def test_wrap(self):
        expected = ['ABCD', 'EFGH', 'IJKL', 'IMNO', 'QRST', 'UVWX', 'YZ']
        assert_equal(expected, self.wrap('ABCDEFGHIJKLIMNOQRSTUVWXYZ', 4))

    @staticmethod
    def sym_diff(mlist, nlist):
        left = set(mlist)
        right = set(nlist)
        diff1 = left.difference(right)
        diff2 = right.difference(left)
        return sorted(diff1.union(diff2))

    def test_sym_diff(self):
        assert_equal(sorted({5, 9, 11, 12}), self.sym_diff([2, 4, 2, 9, 5, 9], [2, 4, 11, 12]))
        assert_equal(sorted({5, 9, 11, 12}), self.sym_diff([2, 4, 11, 9, 2], [2, 4, 5, 12]))


if __name__ == '__main__':
    unittest.main()
