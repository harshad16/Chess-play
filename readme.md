### Project overview
- This project is a fully functional chess game implemented in Python, that allows the users to play against a computer using various algorithms (MCTS and Minmax). It includes:
  - A chess repository class that manages the game board and the pieces
  - A game state class that handles the game logic
  - A MCTS class that implements the Monte Carlo Tree Search algorithm
  - A Minimax class that implements the Minimax algorithm
  - A GUI class that implements the graphical user interface
  - A UI class that implements the command line user interface

### Getting started
- Prerequisites:
  - Python 3.10.2 or newer
  - PyQT5.15 or newer
- Running the project:
  - To run the project, you need to run the main.py file.
  - To switch between the command line and the graphical user interface, you need to change the value of the variable `use_gui` to `True` or `False` in the main.py file.
- Running the tests:
  - To run the tests, you need to run the test_runner.py file.
- Making moves:
  - To make moves in the command line interface, you need to enter the coordinates of the piece you want to move, and then the coordinates of the square you want to move it to.
  - To make moves in the graphical user interface, you need to click on the piece you want to move, and then click on the square you want to move it to.

### Code Structure
- ChessRepository: Handles the game board and pieces, each chess piece has its own class.
- GameState: Implements game logic and rules.
- MCTS: Implements Monte Carlo Tree Search algorithm for AI.
- Minimax: Implements Minimax algorithm for AI.
- GUI: Implements the graphical user interface.
- UI: Implements the command line user interface.

