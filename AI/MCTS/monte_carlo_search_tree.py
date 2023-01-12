import random
import math
from copy import deepcopy
from typing import Tuple

from AI.MCTS.monte_carlo_node import Node
from Chess.Board.GameState import GameState, print_board
from Chess.Exceptions.Checkmate import Checkmate


class MCTS:
    def __init__(self, state: GameState, iterations: int, exploration_constant: float = 1.4142135623730951):
        self.iterations = iterations
        self.exploration_constant = exploration_constant
        self.root = Node(state)

    def _select(self, node: Node) -> Node:
        """
        Select the next node to explore using the UCB1 algorithm
        """
        while not node.state.game_over:
            if node.not_fully_expanded():
                return node
            node = max(node.children, key=lambda c: c.ucb1(self.exploration_constant))
        return node

    def _expand(self, node: Node) -> Node:
        """
        Expand the selected node by creating new children
        """
        next_state = deepcopy(node.state)
        next_state.play_random_move()
        new_node = Node(next_state, parent=node)
        node.children.append(new_node)
        return new_node

    def _simulate(self, node: Node) -> int:
        """
        Simulate the game to a terminal state and return the result
        """
        state = deepcopy(node.state)
        while not state.game_over:
            try:
                state.play_random_move()
            except Checkmate as e:
                print(e)
        return state.result

    def _backpropagate(self, node: Node, result: int):
        """
        Backpropagate the result of the simulation from the terminal node to the root node
        """
        while node is not None:
            node.visits += 1
            node.wins += result
            node = node.parent

    def select_move(self) -> Tuple[int, int]:
        """
        Perform the MCTS algorithm and select the best move
        """
        for _ in range(self.iterations):
            node = self._select(self.root)
            if node.not_fully_expanded():
                node = self._expand(node)
            result = self._simulate(node)
            self._backpropagate(node, result)
        best_child = max(self.root.children, key=lambda c: c.visits)
        print(best_child)
        return best_child.move


if __name__ == "__main__":
    # Initialize a new game
    state = GameState()
    state.initialize_board()

    # Run the MCTS algorithm for 1000 iterations
    mcts = MCTS(state, 2)
    move = mcts.select_move()
    print(f"Selected move: {move}")