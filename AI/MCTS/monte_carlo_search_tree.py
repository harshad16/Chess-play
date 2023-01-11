import random
import math
from collections import deque
from copy import deepcopy
from datetime import time
from typing import Tuple

from AI.MCTS.Exceptions.LosingState import LosingState
from AI.MCTS.hash_table import HashTable
from AI.MCTS.monte_carlo_node import Node
from Chess.Board.GameState import GameState, print_board
from Chess.Exceptions.Checkmate import Checkmate
import time

class MCTS:
    def __init__(self, state: GameState, iterations: int, exploration_constant: float = 1.4142135623730951):
        self.iterations = iterations
        self.exploration_constant = exploration_constant
        self.root = Node(state)
        self.hashtable = HashTable(1009)
    #     self.current_node
    #
    # def set_current_node(self, state: GameState):
    #     """Set the current node to the one corresponding to the given state"""
    #     # First look in the children of the current node
    #     for child in self.current_node.children:
    #         if child.state == state:
    #             self.current_node = child
    #             return
    #     # If it's not in the children, look in the entire tree
    #     queue = deque([self.root])
    #     while queue:
    #         node = queue.popleft()
    #         if node.state == state:
    #             self.current_node = node
    #             return
    #         queue.extend(node.children)

    def _select(self, node: Node) -> Node:
        """
        Select the next node to explore using the UCB1 algorithm
        """
        while not node.state.game_over:
            if node.not_fully_expanded():
                return node
            hashtable_result = self.hashtable.lookup(node.state)
            if hashtable_result:
                value, move = hashtable_result
                if node.state.turn == "w":
                    if value >= node.beta:
                        return node
                else:
                    if value <= node.alpha:
                        return node
            children = node.children
            children = [child for child in children if child.alpha <= node.beta]
            if len(children) == 0:
                return node
            node = max(children, key=lambda c: c.ucb1(self.exploration_constant))
        return node

    def _expand(self, node: Node) -> Node:
        """
        Expand the selected node by creating new children
        """
        next_state = deepcopy(node.state)
        next_state.play_random_move()
        new_node = Node(next_state, parent=node, alpha=node.alpha, beta=node.beta, move=next_state.history[-1])
        node.children.append(new_node)
        return new_node

    def _simulate(self, node: Node) -> int:
        """
        Simulate the game to a terminal state and return the result
        """
        state = deepcopy(node.state)
        start = time.time()
        while not state.game_over:
            hashtable_result = self.hashtable.lookup(state)
            if hashtable_result:
                value, move = hashtable_result
                if state.turn == "w":
                    if value >= node.beta:
                        return -1
                    node.alpha = max(node.alpha, value)
                else:
                    if value <= node.alpha:
                        return 1
                    node.beta = min(node.beta, value)
            else:
                try:
                    state.play_random_move()
                except Checkmate as e:
                    print(e)
                    end = time.time()
                    print(end - start)
                    return state.result
        end = time.time()
        print(end - start)
        return state.result

    def _backpropagate(self, node: Node, result: int):
        """
        Backpropagate the result of the simulation from the terminal node to the root node
        """
        while node is not None:
            node.visits += 1
            node.wins += result
            node = node.parent

    def select_move(self): #-> Tuple[int, int]:
        """
        Perform the MCTS algorithm and select the best move
        """
        for _ in range(self.iterations):
            node = self._select(self.root)
            try:
                if node.not_fully_expanded():
                    node = self._expand(node)
            except LosingState:
                pass
            result = self._simulate(node)
            self._backpropagate(node, result)
        best_child = max(self.root.children, key=lambda c: c.visits)
        print(best_child.move)
        return best_child.move


if __name__ == "__main__":
    # Initialize a new game
    state = GameState()
    state.initialize_board()

    # Run the MCTS algorithm for "1000" iterations
    mcts = MCTS(state, 10)
    move = mcts.select_move()
    print(f"Selected move: {move}")

    # Play the selected move
    state.make_move(move)

    # Print the new board
    print_board(state.board)

    move = input("Enter move: ")
    state.make_move(move)
    print_board(state.board)

    # Run the MCTS algorithm for "1000" iterations
    mcts = MCTS(state, 5)
    move = mcts.select_move()
    print_board(state.board)
