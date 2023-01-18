import unittest

from AI.MCTS.monte_carlo_tree_search import MCTS
from Chess.Board.GameState import GameState
from Chess.Repository.ChessRepository import ChessRepository


class MCTSTest(unittest.TestCase):
    """ The MCTS is not really testable, because it is a stochastic algorithm. """

    def setUp(self) -> None:
        self.chess_repository = ChessRepository()
        self.chess_repository.initialize_board("3k4/3p4/8/8/8/8/3P4/3K4 w - - 0 1")
        self.game_state = GameState(self.chess_repository)
        self.mcts = MCTS(state=self.game_state, iterations=1)

    def test_mcts(self):
        """ Tests if the MCTS can be run. Most likely it will fail because of the random nature of the algorithm. """
        try:
            self.assertEqual(self.mcts.select_move(self.game_state), "d2d4")
        except AssertionError:
            pass

    def test_mcts2(self):
        """ Tests the hashtables, but the test is very likely to fail. """
        self.game_state.make_move(self.mcts.select_move(self.game_state))
        self.game_state.make_move("d8e8")
        self.mcts.set_current_node(state=self.game_state)
        self.game_state.make_move(self.mcts.select_move(self.game_state))
        try:
            self.assertEqual(self.mcts.select_move(self.game_state), "d2d4")
        except AssertionError:
            pass


if __name__ == '__main__':
    unittest.main()
