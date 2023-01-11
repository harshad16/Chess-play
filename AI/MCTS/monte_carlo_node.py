import math
from typing import Tuple

from Chess.Board.GameState import GameState


class Node:
    """ This is a node in the Monte Carlo Search Tree. """

    def __init__(self, state: GameState, parent=None, move=None, alpha=-float("inf"), beta=float("inf")):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0
        self.alpha = alpha
        self.beta = beta

    def not_fully_expanded(self) -> bool:
        return len(self.children) < len(self.state.possible_moves())

    def ucb1(self, exploration_constant: float) -> float:
        if self.visits == 0:
            return float('inf')
        return self.wins / self.visits + exploration_constant * math.sqrt(math.log(self.parent.visits) / self.visits)