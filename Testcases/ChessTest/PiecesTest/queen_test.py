import unittest

from Chess.Pieces.queen import Queen


class QueenTest(unittest.TestCase):
    def setUp(self) -> None:
        self.board: list[list[Queen | None]] = [[None for _ in range(8)] for _ in range(8)]

    def test_queen_moves(self):
        queen = Queen("w", (0, 0))
        self.board[0][0] = queen
        self.assertEqual(queen.get_legal_moves(self.board), [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)])

    def test_queen_value(self):
        self.assertEqual(Queen("w", (0, 0)).get_value(), 9)

if __name__ == '__main__':
    unittest.main()
