import unittest

from Chess.Pieces.bishop import Bishop


class BishopTest(unittest.TestCase):
    def setUp(self) -> None:
        self.board: list[list[Bishop | None]] = [[None for _ in range(8)] for _ in range(8)]

    def test_bishop_moves(self):
        bishop = Bishop("w", (0, 0))
        self.board[0][0] = bishop
        self.assertEqual(bishop.get_legal_moves(self.board), [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)])

    def test_bishop_value(self):
        self.assertEqual(Bishop("w", (0, 0)).get_value(), 3)


if __name__ == '__main__':
    unittest.main()
