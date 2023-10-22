from AI.MCTS.monte_carlo_tree_search import MCTS
from AI.Minimax.minimax import Minimax
from Chess.Board.GameState import GameState
from Chess.Exceptions.IllegalMoveException import IllegalMove
from Chess.Exceptions.WrongColor import WrongColor
from Chess.Repository.ChessRepository import ChessRepository


class UI:
    def __init__(self, game_state):
        """ Initializes the UI
        :param game_state: The game state to use """
        self.ai = None
        self.state = game_state

    def handle_algorithm_selection(self):
        """ Handles the selection of the AI algorithm """
        commands = {"minimax": "Minimax",
                    "mcts": "MCTS"
                    }

        while True:
            algorithm = input("Please select algorithm: minimax, mcts\n> ")
            if algorithm in commands:
                return commands[algorithm]
            else:
                print("Invalid algorithm")

    def handle_color_selection(self):
        """ Handles the selection of color the AI will be playing """
        commands = {"white": "w",
                    "black": "b"
                    }

        while True:
            color = input("Please select color: white, black\n> ")
            if color in commands:
                return commands[color]
            else:
                print("Invalid color")

    def handle_difficulty_selection(self):
        """ Handles the difficulty that the AI will be playing at """
        commands = {"easy": 2,
                    "medium": 5,
                    "hard": 10
                    }

        while True:
            difficulty = input("Please select difficulty: easy, medium, hard\n> ")
            if difficulty in commands:
                return commands[difficulty]
            else:
                print("Invalid difficulty")

    def print_board(self, board):
        """ Print the board

         :param board: The board to print"""
        for i in range(len(board.board)):
            string = []
            for j in range(len(board.board[i])):
                if board.board[i][j] is not None:
                    string.append(board.board[i][j])
                else:
                    string.append("")
            print(string)
        print("\n")

    def start(self):
        """ Starts the game """
        difficulty = 2
        color_one = "w"
        minimax_ai = Minimax(self.state, difficulty, color_one)
        color_two = "b"
        mcts_ai = MCTS(self.state, iterations=difficulty, depth_limit=None, use_opening_book=True,color=color_two)
        
        while not self.state.board.game_over:
            if self.state.board.result:
                if self.state.board.turn == "w":
                    print("Minmax wins")
                else:
                    print("Monte wins")
                break

            if self.state.board.turn == color_one:
                print("Player Minimax playing")
                move = minimax_ai.select_move(self.state)
                print("Move made by MinMax:",move)
                self.state.make_move(move)
                self.print_board(self.state.board)
                
            else:
                print("Player Monte carlo playing")
                move = mcts_ai.select_move(self.state)
                print("Move made by MCTS: ",move)
                self.state.make_move(move)
                self.print_board(self.state.board)
                
if __name__ == "__main__":
    game_repository = ChessRepository()
    game_repository.initialize_board()
    game_state = GameState(game_repository)
    ui = UI(game_state)
    ui.start()