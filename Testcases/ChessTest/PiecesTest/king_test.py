import unittest

from Chess.Pieces.king import King
from Chess.Pieces.piece import Piece
from Chess.Pieces.rook import Rook


class KingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.board: list[list[King | None]] = [[None for _ in range(8)] for _ in range(8)]
        self.pieces: list[list[Piece]] = []

    def test_king_moves(self):
        king = King("w", (0, 0))
        self.board[0][0] = king
        self.pieces.append(king)
        self.assertEqual(king.get_legal_moves(self.board, pieces=self.pieces, move_history=[]), [(0, 1), (1, 0), (1, 1)])

    def test_king_value(self):
        self.assertEqual(King("w", (0, 0)).get_value(), 1000)

    def test_king_castle(self):
        king = King("w", (0, 4))
        self.board[0][4] = king
        king_side_rook = Rook("w", (0, 7))
        self.board[0][7] = king_side_rook
        queen_side_rook = Rook("w", (0, 0))
        self.board[0][0] = queen_side_rook
        self.pieces = [queen_side_rook, king, king_side_rook]
        self.assertEqual(king.get_legal_moves(self.board, pieces=self.pieces, move_history=[]),
                         [(0, 3), (0, 5), (1, 3), (1, 4), (1, 5), (0, 6), (0, 2)])

    def test_king_is_in_check(self):
        king = King("w", (0, 4))
        self.board[0][4] = king
        self.pieces = [king]
        self.assertEqual(king.is_in_check(self.board, pieces=self.pieces, move_history=[]), False)
        self.pieces.append(Rook("b", (0, 0)))
        self.assertEqual(king.is_in_check(self.board, pieces=self.pieces, move_history=[]), True)


if __name__ == '__main__':
    unittest.main()
