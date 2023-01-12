from Chess.Board.GameState import GameState


class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def hash(self, state: GameState) -> int:
        """ Create a unique hash value for the current state """
        return hash(str(state)) % self.size

    def lookup(self, state: GameState):
        """ Look up the value and best move for the current state in the hash table """
        h = self.hash(state)
        if self.table[h]:
            return self.table[h]
        return None

    def store(self, state: GameState, value: int, move):
        """ Store the value and best move for the current state in the hash table """
        h = self.hash(state)
        self.table[h] = (value, move)
