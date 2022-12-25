import sys

from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import QEvent

from Chess.Board.GameState import GameState, print_board
from Chess.Exceptions.Checkmate import Checkmate
from Chess.Exceptions.IllegalMoveException import IllegalMove
from Chess.Exceptions.WrongColor import WrongColor


class ChessGUI(QObject):
    def __init__(self):
        super().__init__()
        self.chess = GameState()
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
                # QWidget.mousePressEvent = ChessSquare.mousePressEvent
                square = QWidget(self.central_widget)
                square.setAccessibleDescription(self.characters[col] + str(8 - row))
                square.setStyleSheet("background-color: #F0D9B5" if (col + row) % 2 == 0
                                     else "background-color: #B58863")
                square.installEventFilter(self)
                self.grid_layout.addWidget(square, row, col)

        # Create the pieces
        self.pieces = []
        #self.chess.initialize_board_from_fen("r4rk1/1pq2pp1/p1n1p1b1/4P3/7Q/7R/PPP2PP1/2KR1B2 b - - 4 20")
        self.chess.initialize_board()
        self.createPieces()
        print(self.pieces)

        # print_board(self.chess.get_board())
        # print(self.board)
        # Set the central widget
        self.window.setCentralWidget(self.central_widget)

        # Show the main window
        self.window.show()

        # Run the application
        sys.exit(self.app.exec_())

    # def unholyHandler(self, label, event):
    #     print('aaaaaaaaaaaaaa')
    #     if event.type() == QEvent.MouseButtonPress:
    #         print(label.text())

    def createPieces(self):
        # go over gamestate board and create pieces
        for col in self.chess.get_board():
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

    def recreatePieces(self):
        for piece in self.pieces:
            self.grid_layout.removeWidget(piece)
        self.pieces = []
        self.createPieces()

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:  # from PyQt5.QtCore import QEvent
            print(source.accessibleDescription())
            if isinstance(source, QLabel):
                if self.source is None:
                    self.source = source
                else:
                    try:
                        self.chess.make_move(self.source.accessibleDescription() + source.accessibleDescription())
                    except IllegalMove as e:
                        print(e)
                    except WrongColor as e:
                        print(e)
                    except Checkmate as e:
                        raise e
                    print_board(self.chess.get_board())
                    self.recreatePieces()
                    # Clear the source square
                    self.source = None
                # self.grid_layout.removeWidget(source)
                # self.pieces.remove(source)
                # source.deleteLater()
            elif self.source is not None:
                try:
                    self.chess.make_move(self.source.accessibleDescription() + source.accessibleDescription())
                except IllegalMove as e:
                    print(e)
                except WrongColor as e:
                    print(e)
                except Checkmate as e:
                    raise e
                print_board(self.chess.get_board())
                self.recreatePieces()
                self.source = None
            else:
                self.source = None
        return super().eventFilter(source, event)

    def label_clicked(self, label):
        # Get the position of the clicked label from its accessibleDescription
        position = label.accessibleDescription()

        # If the source square has not been set, set it to the position of the clicked label
        if self.source_square is None:
            self.source_square = position
        # If the source square has been set, set the destination square to the position of the clicked label
        # and reset the source square
        else:
            self.destination_square = position
            self.source_square = None

            # Pass the move to the GameState object for processing
            self.chess.make_move(self.source_square, self.destination_square)

if __name__ == "__main__":
    gui = ChessGUI()
