import unittest

from Chess.Repository.ChessRepository import ChessRepository


class ChessRepositoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = ChessRepository()

    def test_get_all_pieces(self):
        self.assertEqual(self.repository.pieces, [])

    def test_initialize_board(self):
        self.repository.initialize_board()
        self.assertEqual(len(self.repository.pieces), 32)

    def test_initialize_from_fen(self):
        """ Test that the board is initialized correctly from a FEN string. """
        self.repository.initialize_board("k7/8/8/8/8/8/2k5/8 w KQkq - 0 1")
        self.assertEqual(len(self.repository.pieces), 2)

    def test_remove_piece(self):
        self.repository.initialize_board()
        self.repository.remove_piece(self.repository.board[0][0])
        self.assertEqual(len(self.repository.pieces), 31)

    def test_fen(self):
        self.repository.initialize_board()
        self.assertEqual(self.repository.fen(), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def test_setters_and_getters(self):
        self.repository.initialize_board()
        self.repository.game_over = True
        self.assertEqual(self.repository.game_over, True)
        self.repository.turn = "b"
        self.assertEqual(self.repository.turn, "b")
        self.repository.history = "e2e4"
        self.assertEqual(self.repository.history, ["e2e4"])
        self.repository.result = "1-0"
        self.assertEqual(self.repository.result, "1-0")
        self.repository.half_moves = 1
        self.assertEqual(self.repository.half_moves, 1)
        self.repository.number_of_moves = 1
        self.assertEqual(self.repository.number_of_moves, 1)

if __name__ == '__main__':
    unittest.main()