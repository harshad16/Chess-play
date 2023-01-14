from Chess.Pieces.piece import Piece


class Knight(Piece):
    def __init__(self, color, position):
        super().__init__("N", color, position)

    def get_legal_moves(self, board, move_history=None, pieces=None):
        # Generate a list of legal moves for the knight based on its movement patterns and the current board state
        legal_moves = []

        # Check the eight squares that the knight can move to
        for row_offset in [-2, -1, 1, 2]:
            for col_offset in [-2, -1, 1, 2]:
                if abs(row_offset) == abs(col_offset):
                    continue
                new_row = self._position[0] + row_offset
                new_col = self._position[1] + col_offset
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    # Check if the square is occupied by a friendly piece
                    if board[new_row][new_col] is None or board[new_row][new_col].color != self.color:
                        legal_moves.append((new_row, new_col))

        return legal_moves
        pass

    def get_value(self):
        # TODO: Implement a better evaluation function
        # Evaluate the value of the knight based on its position and other factors
        return 3  # Hard coded value for now
