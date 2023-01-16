import unittest

from Chess.Pieces.knight import Knight


class KnightTest(unittest.TestCase):
    def setUp(self) -> None:
        self.board: list[list[Knight | None]] = [[None for _ in range(8)] for _ in range(8)]

    def test_knight_moves(self):
        knight = Knight("w", (0, 1))
        self.board[0][1] = knight
        self.assertEqual(knight.get_legal_moves(self.board), [(1, 3), (2, 0), (2, 2)])

    def test_knight_value(self):
        self.assertEqual(Knight("w", (0, 0)).get_value(self.board), 3.2)


if __name__ == '__main__':
    unittest.main()
