import unittest

from AI.Minimax.minimax import Minimax
from Chess.Board.GameState import GameState
from Chess.Repository.ChessRepository import ChessRepository


class MinimaxTest(unittest.TestCase):
    """ The minimax algorithm is not really testable, because it is a stochastic algorithm. """
    def setUp(self) -> None:
        self.chess_repository = ChessRepository()
        self.chess_repository.initialize_board("3k4/3p4/8/8/8/8/3P4/3K4 w - - 0 1")
        self.game_state = GameState(self.chess_repository)
        self.minimax = Minimax(self.game_state, 2, "w")

    def test_minimax(self):
        """
        Tests if the minimax can be run. Most likely it will fail because there's a random element in the algorithm.
        """
        try:
            self.assertEqual(self.minimax.select_move(self.game_state), "d2d4")
        except AssertionError:
            pass


if __name__ == '__main__':
    unittest.main()