"""
Tests for model.py.

Note that the unittest module predates PEP-8 guidelines, which
is why we have a bunch of names that don't comply with the
standard.
"""
from model import Board
from model import Vec
import unittest
import sys

class TestBoardConstructor(unittest.TestCase):

    def test_default(self):
        board = Board()
        self.assertEqual(board.tiles, [[None, None, None, None],
                                       [None, None, None, None],
                                       [None, None, None, None],
                                       [None, None, None, None]])

    def test_3x5(self):
        board = Board(rows=3, cols=5)
        self.assertEqual(board.tiles, [[None, None, None, None, None],
                                 [None, None, None, None, None],
                                 [None, None, None, None, None]])

if __name__ == "__main__":
    unittest.main()
