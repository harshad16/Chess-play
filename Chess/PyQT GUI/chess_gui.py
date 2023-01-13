import sys

from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import QEvent

from Chess.Board.ChessRepository import ChessRepository
from Chess.Board.GameState import GameState, print_board
from Chess.Exceptions.Checkmate import Checkmate
from Chess.Exceptions.IllegalMoveException import IllegalMove
from Chess.Exceptions.WrongColor import WrongColor
from Chess.Pieces.king import King


class ChessGUI(QObject):
    def __init__(self, chess_repository):
        super().__init__()
        self.chess = GameState(chess_repository)
        self.app = QApplication(sys.argv)
        # Create the main window
        self.window = QMainWindow()
        self.window.setWindowTitle("Chess")
        self.window.setFixedSize(800, 800)

        # Create the central widget
        self.central_widget = QWidget(self.window)

        # Create the grid layout
        self.grid_layout = QGridLayout(self.central_widget)
        self.grid_layout.setSpacing(0)

        # Create the instance variables to store the source and destination squares
        self.source = None
        self.destination = None

        self.source_square = None
        self.destination_square = None

        # Create the chess board
        self.characters = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

        for row in range(8):
            for col in range(8):
                square = QWidget(self.central_widget)
                square.setAccessibleDescription(self.characters[col] + str(8 - row))
                square.setStyleSheet("background-color: #F0D9B5" if (col + row) % 2 == 0
                                     else "background-color: #B58863")
                square.installEventFilter(self)
                self.grid_layout.addWidget(square, row, col)

        # Create the pieces
        self.pieces = []
        self.createPieces()

        # Set the central widget
        self.window.setCentralWidget(self.central_widget)

        # Show the main window
        self.window.show()

        # Run the application
        sys.exit(self.app.exec_())

    # ! This function is deprecated. And also it's quite cursed.
    # def unholyHandler(self, label, event):
    #     print('aaaaaaaaaaaaaa')
    #     if event.type() == QEvent.MouseButtonPress:
    #         print(label.text())

    def createPieces(self):
        # go over gamestate board and create pieces
        for col in self.chess.board.board:
            for element in col:
                if element is not None:
                    piece = QLabel(self.central_widget)

                    color_name = "white" if element.color == "w" else "black"
                    pixmap = QPixmap(f"../Resources/{color_name}_{type(element).__name__.lower()}.png")
                    piece.setPixmap(pixmap)

                    piece.setAccessibleDescription(self.characters[element.position[1]] + str(element.position[0] + 1))
                    piece.installEventFilter(self)
                    self.grid_layout.addWidget(piece, 7 - element.position[0], element.position[1])
                    self.pieces.append(piece)
        return

    def recreate_pieces(self):
        for piece in self.pieces:
            self.grid_layout.removeWidget(piece)
        self.pieces = []
        self.createPieces()

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:  # from PyQt5.QtCore import QEvent
            # print(source.accessibleDescription())
            if isinstance(source, QLabel):
                if self.source is None:
                    self.source = source
                    legal_moves = self.chess.get_legal_moves(source.accessibleDescription())
                    self.highlight_legal_moves(legal_moves)
                else:
                    self.remove_pending_moves()
                    try:
                        self.chess.make_move(self.source.accessibleDescription() + source.accessibleDescription())
                    except IllegalMove as e:
                        print(e)
                    except WrongColor as e:
                        print(e)
                    except Checkmate as e:
                        raise e
                    print_board(self.chess.get_board())
                    self.recreate_pieces()
                    # Clear the source square
                    self.source = None
                # self.grid_layout.removeWidget(source)
                # self.pieces.remove(source)
                # source.deleteLater()
            elif self.source is not None:
                self.remove_pending_moves()
                try:
                    self.chess.make_move(self.source.accessibleDescription() + source.accessibleDescription())
                except IllegalMove as e:
                    print(e)
                except WrongColor as e:
                    print(e)
                except Checkmate as e:
                    raise e
                print_board(self.chess.get_board())
                self.recreate_pieces()
                self.source = None
            else:
                self.source = None
        return super().eventFilter(source, event)

    def highlight_legal_moves(self, legal_moves):
        """ Highlights the legal moves for the piece on the board """
        for move in legal_moves:
            for i in range(self.grid_layout.count()):
                cell = self.grid_layout.itemAt(i)
                widget = cell.widget()
                row = i // 8
                col = i % 8

                if (7 - row, col) == move:
                    #widget.setStyleSheet(("background-color: #F0D9B5;" if (col + row) % 2 == 0 else "background-color: #B58863;") + "background-image: radial-gradient(10px circle at 10px 10px, rgb(0, 255, 0) 50%, transparent 50.2%); background-size: 20px 20px; background-position: center; background-repeat: no-repeat;")
                    widget.setStyleSheet("background-color:" + ("#F0D9B5" if (col + row) % 2 == 0 else "#B58863") + "; background-image: url(../Resources/circle.png); background-position: center; background-repeat: no-repeat; background-size: 5px 5px; background-size: contain;")

    def remove_pending_moves(self):
        """ Removes the highlighted squares """
        for i in range(self.grid_layout.count()):
            square = self.grid_layout.itemAt(i).widget()
            row = i // 8
            col = i % 8
            square.setStyleSheet("background-color: #F0D9B5" if (col + row) % 2 == 0
                                 else "background-color: #B58863")


if __name__ == "__main__":
    chess_repository = ChessRepository()
    chess_repository.initialize_board()
    gui = ChessGUI(chess_repository)
