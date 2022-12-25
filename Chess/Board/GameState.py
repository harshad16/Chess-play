from copy import deepcopy

from Chess.Exceptions.Checkmate import Checkmate
from Chess.Exceptions.IllegalMoveException import IllegalMove
from Chess.Exceptions.WrongColor import WrongColor
from Chess.Pieces.bishop import Bishop
from Chess.Pieces.king import King
from Chess.Pieces.knight import Knight
from Chess.Pieces.pawn import Pawn
from Chess.Pieces.queen import Queen
from Chess.Pieces.rook import Rook
from Chess.utils.move_handlers import process_algebraic_notation


def print_board(board):
    for i in range(len(board)):
        string = []
        for j in range(len(board[i])):
            if board[i][j] is not None:
                string.append(board[i][j])
            else:
                string.append("")
        print(string)
    print("\n")


class GameState:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]  # The board is a 2D array of 8x8 squares
        self.turn = "w"  # White makes the first move
        self.history = []  # Here we will store the history of moves
        self.game_over = False  # Game is still ongoing
        self.pieces = []  # List of pieces
        self.check = {"w": False, "b": False}  # Are the kings in check?
        self.castling_rights = {"w": {"O-O": True, "O-O-O": True}, "b": {"O-O": True, "O-O-O": True}}  # Castling rights

    def initialize_board(self):
        # Initializing the board with the initial position
        # Generate the white pieces
        self.pieces = [
            Rook("w", (0, 0)), Knight("w", (0, 1)), Bishop("w", (0, 2)), Queen("w", (0, 3)), King("w", (0, 4)),
            Bishop("w", (0, 5)), Knight("w", (0, 6)), Rook("w", (0, 7))
        ]
        for col in range(8):
            self.pieces.append(Pawn("w", (1, col)))

        # Generate the black pieces
        self.pieces.extend(
            [Rook("b", (7, 0)), Knight("b", (7, 1)), Bishop("b", (7, 2)), Queen("b", (7, 3)), King("b", (7, 4)),
             Bishop("b", (7, 5)), Knight("b", (7, 6)), Rook("b", (7, 7))]
        )
        for col in range(8):
            self.pieces.append(Pawn("b", (6, col)))

        # Put the pieces on the board
        for piece in self.pieces:
            self.board[piece.position[0]][piece.position[1]] = piece

        for piece in self.pieces:
            self.board[piece.position[0]][piece.position[1]] = piece

    def initialize_board_from_fen(self, FEN):
        # Initialize the board from a FEN string
        pieces = {"r": Rook, "n": Knight, "b": Bishop, "q": Queen, "k": King, "p": Pawn}
        FEN = FEN.split(" ")
        fen = FEN[0].split("/")
        fen.reverse()
        print(FEN)
        pos = (0, 0)
        for row in fen:
            for char in row:
                if char.isdigit():
                    for _ in range(int(char)):
                        self.board[pos[0]][pos[1]] = None
                        pos = (pos[0], pos[1] + 1)
                if char.lower() in pieces:
                    if char.islower():
                        piece = pieces[char]("b", pos)
                        self.pieces.append(piece)
                        self.board[pos[0]][pos[1]] = piece
                    else:
                        piece = pieces[char.lower()]("w", pos)
                        self.pieces.append(piece)
                        self.board[pos[0]][pos[1]] = piece
                    pos = (pos[0], pos[1] + 1)
            pos = (pos[0] + 1, 0)
        # Set the game variables from the FEN string
        self.turn = FEN[1]  # Set the turn
        self.castling_rights = {
            "w": {"O-O": True if "K" in FEN[2] else False, "O-O-O": True if "Q" in FEN[2] else False},
            "b": {"O-O": True if "k" in FEN[2] else False, "O-O-O": True if "q" in FEN[2] else False}
        }

    def make_move(self, move):
        # Make a copy of the board and the pieces
        initial_board = deepcopy(self.board)
        initial_pieces = deepcopy(self.pieces)

        # Calculate the start and end squares
        end, start = process_algebraic_notation(move)

        # Get the piece at the start square
        piece = self.board[start[0]][start[1]]
        print(piece.color, self.turn)
        # Check if the piece is the correct color
        if piece.color != self.turn:
            raise WrongColor("That's not your piece!")
        # Check if the move is legal
        if not isinstance(piece, King):
            if end not in piece.get_legal_moves(self.board, self.history):
                raise IllegalMove("That move is illegal!")
        elif end not in piece.get_king_legal_moves(self.board, self.pieces, self.castling_rights, self.history):
            print(piece.get_king_legal_moves(self.board, self.pieces, self.castling_rights, self.history))
            raise IllegalMove("That move is illegal!")

        # Check if king is in check
        king = None
        for row in self.board:
            for square in row:
                if square is not None and square.color == self.turn and isinstance(square, King):
                    king = square
                    break

        if king.is_in_check(self.board, self.pieces, self.history):
            # Simulate the move to see if the king is still in check
            if self.board[end[0]][end[1]] is not None and self.board[end[0]][end[1]].color != self.turn:
                self.pieces.remove(self.board[end[0]][end[1]])
            self.board[end[0]][end[1]] = piece
            self.board[start[0]][start[1]] = None
            piece.position = end
            if king.is_in_check(self.board, self.pieces, self.history):
                self.rollback(initial_board, initial_pieces)
                raise IllegalMove("You must get out of check!")
            self.turn = "b" if self.turn == "w" else "w"
            return

        # Check if the move is a capture
        if self.board[end[0]][end[1]] is not None:
            # If there is a piece at the end square, check if it is an enemy piece
            if self.board[end[0]][end[1]].color != self.turn:
                # If the piece is an enemy piece, remove it from the list of pieces
                self.pieces.remove(self.board[end[0]][end[1]])
            else:
                # If the piece is a friendly piece, the move is illegal
                raise IllegalMove("You can't capture your own piece!")
        # Castling rights
        if (self.castling_rights[self.turn]["O-O"] or self.castling_rights[self.turn]["O-O-O"]) and (isinstance(piece, King) or isinstance(piece, Rook)):
            if isinstance(piece, King) and abs(end[1] - start[1]) == 1:
                # Remove the castling rights if the king moves
                self.castling_rights[self.turn]["O-O"] = False
                self.castling_rights[self.turn]["O-O-O"] = False

            if isinstance(piece, Rook):
                # Remove the castling rights if the rook moves
                if start == (0, 0) or start == (7, 0):
                    self.castling_rights[self.turn]["O-O-O"] = False
                if start == (0, 7) or start == (7, 7):
                    self.castling_rights[self.turn]["O-O"] = False

            # Check if the move is a castling move
            if isinstance(piece, King) and abs(end[1] - start[1]) == 2 and (self.castling_rights[self.turn]["O-O"] or self.castling_rights[self.turn]["O-O-O"]):
                # Check if there are pieces between the king and the rook
                if end[1] > 4 and self.board[end[0]][end[1] - 1] is not None and self.board[end[0]][end[1] - 2] is not None:
                    raise IllegalMove("You can't castle through pieces!")
                if end[1] < 4 and self.board[end[0]][end[1] + 1] is not None and self.board[end[0]][end[1] + 2] is not None:
                    raise IllegalMove("You can't castle through pieces!")
                # If there are no pieces between the king and the rook, check the castling rights
                elif end not in king.get_king_legal_moves(self.board, self.pieces, self.castling_rights, self.history):
                    raise IllegalMove(f'You don\'t have the right to castle {"king" if self.castling_rights[self.turn]["O-O"] else "queen"} side!')

                # If the king is not in check and there are no pieces between the king and the rook, castle
                else:
                    # Move the rook
                    if end[1] == 6:
                        self.board[end[0]][5] = self.board[end[0]][7]
                        self.board[end[0]][7] = None
                        self.board[end[0]][5].position = (end[0], 5)
                    else:
                        self.board[end[0]][3] = self.board[end[0]][0]
                        self.board[end[0]][0] = None
                        self.board[end[0]][3].position = (end[0], 3)

                # Remove the castling rights
                self.castling_rights[self.turn]["O-O"] = False
                self.castling_rights[self.turn]["O-O-O"] = False


        # Check if the move is an en passant capture
        if isinstance(piece, Pawn) and self.board[end[0]][end[1]] is None and end[1] != start[1]:
            # If the pawn moves diagonally and there is no piece at the end square, it is an en passant capture
            self.board[start[0]][end[1]] = None

        # Move the piece
        self.board[start[0]][start[1]] = None
        self.board[end[0]][end[1]] = piece
        piece.position = end

        # Check if the move is a pawn promotion
        if isinstance(piece, Pawn) and (end[0] == 0 or end[0] == 7):
            # Check if the piece is a pawn and if it is on the last rank
            # If it is, promote it
            self.board[start[0]][start[1]] = None
            self.board[end[0]][end[1]] = Queen(piece.color, end)

        # Update the history
        self.history.append(move)

        # Update the turn
        self.turn = "b" if self.turn == "w" else "w"

        for i in self.pieces:
            if isinstance(i, King) and i.color == self.turn:
                king = i
                break
        initial_board, initial_pieces = self.board, self.pieces
        # Check if the king is in checkmate
        if king.is_in_check(self.board, self.pieces, self.history):
            if king.get_king_legal_moves(self.board, self.pieces, {"w": {"O-O": False, "O-O-O": False}, "b": {"O-O": False, "O-O-O": False}}, self.history) == []:
                # If the king has no legal moves, check if the checking piece can be captured or blocked
                move_found = False
                for i in self.pieces:
                    if i.color == self.turn:
                        if isinstance(i, King):
                            continue
                        legal_moves = i.get_legal_moves(self.board, self.history)
                        for move in legal_moves:
                            i.position = move
                            self.board[move[0]][move[1]] = i
                            self.board[i.position[0]][i.position[1]] = None
                            if not king.is_in_check(self.board, self.pieces, self.history):
                                move_found = True
                            self.rollback(deepcopy(initial_board), deepcopy(initial_pieces))
                            if move_found:
                                break
                if not move_found:
                    self.game_over = True
                    self.rollback(initial_board, initial_pieces)
                    raise Checkmate(f'Game over: {"1-0" if self.turn == "b" else "0-1"}!')

        # Check if the king is in stalemate
        else:
            if king.get_king_legal_moves(self.board, self.pieces, {"w": {"O-O": False, "O-O-O": False}, "b": {"O-O": False, "O-O-O": False}}, self.history) == []:
                # If the king has no legal moves, check if the checking piece can be captured or blocked
                move_found = False
                for i in self.pieces:
                    if i.color == self.turn:
                        self.rollback(deepcopy(initial_board), deepcopy(initial_pieces))
                        if isinstance(i, King):
                            continue
                        legal_moves = i.get_legal_moves(self.board, self.history)
                        if legal_moves != []:
                            move_found = True
                            break
                if not move_found:
                    self.game_over = True
                    self.rollback(initial_board, initial_pieces)
                    raise Checkmate(f'Game over: 1/2-1/2!')
        # Update the list of pieces
        self.pieces = [piece for row in self.board for piece in row if piece is not None]

    def rollback(self, board, pieces):
        self.board = board
        self.pieces = pieces

    def get_board(self):
        # Return the board
        return self.board

if __name__ == "__main__":

    game = GameState()
    game.initialize_board()
    board = game.get_board()

    # Queen's Pawn Opening
    #     game.make_move("d2d4")
    #     print_board(board)
    #     game.make_move("d7d5")
    #     print_board(board)
    # London System
    #     game.make_move("g1f3")
    #     print_board(board)
    #     game.make_move("g8f6")
    #     print_board(board)
    #     game.make_move("c1f4")
    #     print_board(board)

    # Englund Gambit
    #     game.make_move("d2d4")
    #     print_board(board)
    #     game.make_move("e7e5")
    #     print_board(board)
    #     game.make_move("d4e5")
    #     print_board(board)
    #     game.make_move("b8c6")
    #     print_board(board)
    #     game.make_move("g1f3")
    #     print_board(board)
    #     game.make_move("d8e7")
    #     print_board(board)
    #     game.make_move("c1f4")
    #     print_board(board)
    #     game.make_move("e7b4")
    #     print_board(board)
    #     game.make_move("c2c3")
    #     print_board(board)
    #     # Casually hang the queen to test if it can capture/be captured
    #     game.make_move("b4c3")
    #     print_board(board)
    #     game.make_move("b1c3")
    print_board(board)
    # Knight stuff
    while True:
        try:
            game.make_move(input("The move:"))
            print_board(board)
        except Exception as e:
            print(e)
