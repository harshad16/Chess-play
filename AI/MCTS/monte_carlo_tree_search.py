import json
import random
import math
from collections import deque
from copy import deepcopy
from datetime import time

from AI.MCTS.Exceptions.LosingState import LosingState
from AI.MCTS.hash_table import HashTable
from AI.MCTS.monte_carlo_node import Node
from Chess.Board.GameState import GameState, print_board
from Chess.Exceptions.Checkmate import Checkmate
import time
import numpy as np

class MCTS:
    def __init__(self, state: GameState, iterations: int, exploration_constant: float = math.sqrt(2), depth_limit=None):
        self.iterations = iterations
        self.exploration_constant = exploration_constant
        self.root = Node(state)
        self.hashtable = HashTable(1009)
        self.current_node = self.root
        self.depth_limit = depth_limit
        # TODO: Implement the opening book to provide stronger play and faster moves in the opening, when there are a lot of possible moves
        self.opening_book = {
            # 6 moves of exchange QGD
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1": "d2d4",
            "rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 2": "c2c4",
            "rnbqkbnr/ppp2ppp/4p3/3p4/2PP4/8/PP2PPPP/RNBQKBNR w KQkq - 0 3": "b1c3",
            "rnbqkb1r/ppp2ppp/4pn2/3p4/2PP4/2N5/PP2PPPP/R1BQKBNR w KQkq - 2 4": "c4d5",
            "rnbqkb1r/ppp2ppp/5n2/3p4/3P4/2N5/PP2PPPP/R1BQKBNR w KQkq - 0 5": "c1g5",
            "rnbqkb1r/pp3ppp/2p2n2/3p2B1/3P4/2N5/PP2PPPP/R2QKBNR w KQkq - 0 6": "e2e3",

            # 4 moves of the Catalan
            "rnbqkb1r/pppppppp/5n2/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 1 2": "c2c4",
            "rnbqkbnr/pppp1ppp/4p3/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 2": "c2c4",  # Transposition
            "rnbqkb1r/pppp1ppp/4pn2/8/2PP4/8/PP2PPPP/RNBQKBNR w KQkq - 0 3": "g2g3",
            "rnbqkb1r/pppp1ppp/4pn2/8/2PP4/8/PP2PPPP/RNBQKBNR w KQkq - 1 3": "g2g3",  # Transposition
            "rnbqk2r/pppp1ppp/4pn2/8/1bPP4/6P1/PP2PP1P/RNBQKBNR w KQkq - 1 4": "c1d2",
            "rnbqk2r/ppppbppp/4pn2/8/2PP4/6P1/PP1BPP1P/RN1QKBNR w KQkq - 3 5": "g1d3"
        }

    def set_current_node(self, state: GameState):
        """ Set the current node to the one corresponding to the given state """
        # First look in the children of the current node
        for child in self.current_node.children:
            if child.state == state:
                self.current_node = child
                print_board(self.current_node.state.get_board())
                return
        # If it's not in the children of the node, look in the entire tree
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            if node.state == state and node != self.root and node != self.current_node:
                self.current_node = node
                print_board(self.current_node.state.get_board())
                return
            queue.extend(node.children)
        if not self.current_node.state == state:
            self.current_node = Node(state)

    def _select(self, node: Node, depth: int) -> Node:
        """ Select the next node to explore using the UCB1 algorithm """
        while not node.state.game_over:
            if node.not_fully_expanded():
                return node
            if self.depth_limit and depth>= self.depth_limit:
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
            depth += 1
        return node

    def _expand(self, node: Node) -> Node:
        """ Expand the selected node by creating new children """
        next_state = deepcopy(node.state)
        next_state.play_random_move()
        new_node = Node(next_state, parent=node, alpha=node.alpha, beta=node.beta, move=next_state.history[-1])
        node.children.append(new_node)
        return new_node

    def _simulate(self, node: Node) -> int:
        """ Simulate the game to a terminal state and return the result """
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
        """ Backpropagate the result of the simulation from the terminal node to the root node """
        while node is not None:
            node.visits += 1
            node.wins += result
            node = node.parent

    def select_move(self):
        """ Perform the MCTS algorithm and select the best move """
        fen = self.root.state.fen()
        if fen in self.opening_book:
            return self.opening_book[fen]

        for _ in range(self.iterations):
            node = self._select(self.current_node, 0)
            try:
                if node.not_fully_expanded():
                    node = self._expand(node)
            except LosingState:
                pass
            result = self._simulate(node)
            self._backpropagate(node, result)

        best_child = max(self.current_node.children, key=lambda c: c.visits)
        self.current_node = best_child
        return best_child.move

# ! Not necessary yet
# def load_dataset():
#     # Load the dataset from a file
#     data = []
#     with open('opening_book.json') as f:
#         data = json.load(f)
#
#     # Split the data into positions and labels
#     fen = data['positions']['fen']
#     move = data['positions']['move']
#     return np.array(fen), np.array(move)


if __name__ == "__main__":
    chess_state = GameState()
    chess_state.initialize_board()
    mcts = MCTS(chess_state, iterations=20)

    while not chess_state.game_over:
        start = time.time()
        move = mcts.select_move()
        print(move)
        print(f"\nTime taken on average/move: {(time.time() - start)/20}")
        chess_state.make_move(move)
        # mcts.set_current_node(chess_state)
        print_board(chess_state.get_board())
        move = input("Move: ")
        chess_state.make_move(move)
        mcts.set_current_node(chess_state)
        print_board(chess_state.get_board())
        print(chess_state.fen())
