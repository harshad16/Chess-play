import unittest

from Chess.Pieces.pawn import Pawn


class PawnTest(unittest.TestCase):
    def setUp(self):
        self.board: list[list[Pawn | None]] = [[None for _ in range(8)] for _ in range(8)]
        self.history = []

    def test_starting_square_moves(self):
        pawn = Pawn("w", (1, 0))
        self.board[1][0] = pawn
        # Check if the pawn can move two squares forward if it is on its starting square
        self.assertEqual(pawn.get_legal_moves(self.board, self.history), [(2, 0), (3, 0)])

    def test_not_starting_square_moves(self):
        # Check if the pawn can move one square forward if it is not on its starting square
        pawn = Pawn("w", (2, 4))
        self.board[2][4] = pawn
        self.assertEqual(pawn.get_legal_moves(self.board, self.history), [(3, 4)])

    def test_diagonal_capture(self):
        # Check if the pawn can capture diagonally
        self.board[2][4] = Pawn("w", (2, 4))
        self.board[3][3] = Pawn("b", (3, 3))
        self.board[3][5] = Pawn("b", (3, 5))
        self.assertEqual(self.board[2][4].get_legal_moves(self.board, self.history), [(3, 4), (3, 3), (3, 5)])

    def test_en_passant(self):
        # Check if the pawn can capture en passant
        self.board[3][4] = Pawn("w", (3, 4))
        self.board[3][5] = Pawn("b", (3, 5))
        self.history.append("e2e4")
        self.assertEqual(self.board[3][5].get_legal_moves(self.board, self.history), [(2, 5), (2, 4)])

    def test_en_passant_not_available(self):
        # Check if the pawn can capture en passant
        self.board[3][4] = Pawn("w", (3, 4))
        self.board[3][5] = Pawn("b", (3, 5))
        self.assertEqual(self.board[3][5].get_legal_moves(self.board, self.history), [(2, 5)])

    def test_value(self):
        # Check if the pawn's value is correct
        self.assertEqual(Pawn("w", (0, 0)).get_value(self.board, []), 1.9)


if __name__ == '__main__':
    unittest.main()
