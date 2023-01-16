import unittest

from AI.Minimax.minimax import Minimax
from Chess.Board.GameState import GameState
from Chess.Repository.ChessRepository import ChessRepository


class MinimaxTest(unittest.TestCase):
    def setUp(self) -> None:
        self.chess_repository = ChessRepository()
        self.chess_repository.initialize_board("3k4/3p4/8/8/8/8/3P4/3K4 w - - 0 1")
        self.game_state = GameState(self.chess_repository)
        self.minimax = Minimax(self.game_state, 10, "w")

    def test_minimax(self):
        self.assertEqual(self.minimax.best_move(self.game_state)[0], "d1c1")


if __name__ == '__main__':
    unittest.main()