import sys
from random import choice

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QGridLayout


class DifficultySelector(QObject):
    def __init__(self):
        """ Initialize the difficulty selector """
        super().__init__()
        self.app = QApplication(sys.argv)
        self.window = QWidget()

        self.button_layout = QGridLayout()
        self.difficulties = [QPushButton("Easy"), QPushButton("Medium"), QPushButton("Hard"), QPushButton("Easy"), QPushButton("Medium"), QPushButton("Hard")]
        i = 0
        for button in self.difficulties:
            if i <= 2:
                self.button_layout.addWidget(button, i, 0)
                button.setAccessibleName("Minimax " + button.text())
            else:
                self.button_layout.addWidget(button, i-3, 2)
                button.setAccessibleName("MCTS " + button.text())
            button.setCheckable(True)
            button.clicked.connect(self.difficulty_clicked)
            i += 1

        i = 0
        self.colors = [QPushButton("White"), QPushButton("Random"), QPushButton("Black")]
        for button in self.colors:
            self.button_layout.addWidget(button, 6, i)
            button.setCheckable(True)
            button.clicked.connect(self.color_clicked)
            i += 1

        start_game = QPushButton("Start Game")

        start_game.clicked.connect(self.get_difficulty)
        start_game.clicked.connect(self.window.close)

        self.button_layout.addWidget(start_game, 7, 0, 1, 3)
        self.layout = QGridLayout()

        self.layout.addLayout(self.button_layout, 0, 0)
        self.window.setLayout(self.layout)
        self.window.show()

        self.app.exec_()

    def difficulty_clicked(self):
        """ Only allow one difficulty to be selected at a time """
        sender = self.sender()
        for btn in self.difficulties:
            if btn != sender:
                btn.setChecked(False)

    def color_clicked(self):
        """ Only allow one color to be selected at a time """
        sender = self.sender()
        for btn in self.colors:
            if btn != sender:
                btn.setChecked(False)

    def get_difficulty(self):
        """ Get the selected difficulty and color """
        difficulty, color = None, None
        for btn in self.difficulties:
            if btn.isChecked():
                difficulty = btn.accessibleName()
                break
        for btn in self.colors:
            if btn.isChecked():
                color = btn.text()

        if difficulty is None:
            difficulty = f'{choice(["Minimax", "MCTS"])} {choice(["Easy", "Medium", "Hard"])}'

        if color == "Random" or color is None:
            color = choice(["White", "Black"])

        return difficulty, color


if __name__ == '__main__':
    dif = DifficultySelector()
    difficulty, color = dif.get_difficulty()
    print(difficulty, color)
