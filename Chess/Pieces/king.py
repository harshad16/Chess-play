from copy import deepcopy

from Chess.Pieces.piece import Piece


class King(Piece):
    def __init__(self, color, position):
        super().__init__("K", color, position)

    def can_move_to_square(self, board, position, enemy_pieces, move_history):
        row, col = position
        if not (0 <= row < 8 and 0 <= col < 8):
            return False  # square is not on the board
        if board[row][col] is not None and board[row][col].color == self.color:
            return False  # square is occupied by a friendly piece
        # Check if the king would be in check after moving to the square
        board[self._position[0]][self._position[1]] = None
        board[row][col] = self
        self._position = (row, col)
        if self.is_in_check(board, enemy_pieces, move_history):
            return False  # king would be in check after moving to the square
        # Restore the original board state
        board[row][col] = None
        board[self._position[0]][self._position[1]] = self
        self._position = (self._position[0], self._position[1])
        return True  # king can move to the square

    def get_king_legal_moves(self, board, pieces, castling_rights, move_history):
        legal_moves = []
        # Create a copy of the board
        enemy_pieces = []
        for piece in deepcopy(pieces):
            if piece.color != self.color:
                enemy_pieces.append(piece)
        # Check the eight squares that the king can move to
        for row_offset in [-1, 0, 1]:
            for col_offset in [-1, 0, 1]:
                if row_offset == 0 and col_offset == 0:
                    continue
                board_copy = deepcopy(board)
                initial_position = deepcopy(self._position)
                new_row = self._position[0] + row_offset
                new_col = self._position[1] + col_offset
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    # Check if the square is occupied by a friendly piece
                    if board_copy[new_row][new_col] is None or board_copy[new_row][new_col].color != self.color:
                        # Check if the king would be in check after moving to the square
                        board_copy[self._position[0]][self._position[1]] = None
                        board_copy[new_row][new_col] = self
                        self._position = (new_row, new_col)
                        if not self.is_in_check(board_copy, enemy_pieces, move_history):
                            # Only append the new position if the king would not be in check
                            legal_moves.append((new_row, new_col))
                        board_copy[self._position[0]][self._position[1]] = self
                        board_copy[initial_position[0]][initial_position[1]] = None
                        self._position = initial_position
        row, col = self._position

        # Check if the king can castle
        if castling_rights[self.color]["O-O"]:
            board_copy = deepcopy(board)
            # Check if the squares between the king and the rook are empty
            if board[row][col + 1] is None and board[row][col + 2] is None:
                # Check if the king doesn't pass through or end up in check
                board_copy[row][col] = None
                board_copy[row][col + 1] = self
                self._position = (row, col + 1)
                if not self.is_in_check(board_copy, enemy_pieces, move_history):
                    board_copy[row][col + 1] = None
                    board_copy[row][col + 2] = self
                    self._position = (row, col + 2)
                    if not self.is_in_check(board_copy, enemy_pieces, move_history):
                        legal_moves.append((row, col + 2))
                board_copy[row][col + 2] = None
                board_copy[row][col] = self
                self._position = (row, col)
        if castling_rights[self.color]["O-O-O"]:
            board_copy = deepcopy(board)
            # Check if the squares between the king and the rook are empty
            if board[row][col - 1] is None and board[row][col - 2] is None:
                # Check if the king doesn't pass through or end up in check
                board_copy[row][col] = None
                board_copy[row][col - 1] = self
                self._position = (row, col - 1)
                if not self.is_in_check(board_copy, enemy_pieces, move_history):
                    board_copy[row][col - 1] = None
                    board_copy[row][col - 2] = self
                    self._position = (row, col - 2)
                    if not self.is_in_check(board_copy, enemy_pieces, move_history):
                        legal_moves.append((row, col - 2))
                board_copy[row][col - 2] = None
                board_copy[row][col] = self
                self._position = (row, col)

        return legal_moves

    def is_in_check(self, board, pieces, move_history):
        enemy_pieces = []
        for piece in pieces:
            if piece.color != self.color:
                enemy_pieces.append(piece)
        # Check if the king is in check
        for piece in enemy_pieces:
            if not isinstance(piece, King):
                if self._position in piece.get_legal_moves(board, move_history):
                    return True
        return False
