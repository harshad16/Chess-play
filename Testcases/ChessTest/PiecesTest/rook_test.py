import unittest

from Chess.Pieces.rook import Rook


class RookTest(unittest.TestCase):
    def setUp(self) -> None:
        self.board: list[list[Rook | None]] = [[None for _ in range(8)] for _ in range(8)]

    def test_rook_moves(self):
        rook = Rook("w", (0, 0))
        self.board[0][0] = rook
        self.assertEqual(rook.get_legal_moves(self.board), [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)])

    def test_rook_value(self):
        self.assertEqual(Rook("w", (0, 0)).get_value(), 5)


if __name__ == '__main__':
    unittest.main()
