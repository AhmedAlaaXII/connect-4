# Connect-4 Game with Minimax and Alpha-Beta Algorithms
This is a Python implementation of the Connect-4 game using the Minimax algorithm with Alpha-Beta pruning. The game is played on a 6x7 grid and supports two players: level of computer (AI) and level of computer (AI).
## Dependencies

The following dependencies are required to run the game:

- matplotlib.pyplot (as plt)
- numpy (as np)
- pygame
- sys
- math
- random
You can install these dependencies using pip:
```shell
pip install matplotlib numpy pygame
```
## Usage
To start the game, run the following command:
```shell
python main.py
```
## Game Rules
The game is played on a vertical board with 6 rows and 7 columns. Two players take turns to drop their colored discs into the grid. The objective of the game is to connect four of your own discs in a row, column, or diagonal.

- Player 1: Disc color is red ('R')
- Player 2 (AI): Disc color is yellow ('Y')
The game will prompt the current player to enter their move by selecting the column number (0-6) where they want to drop their disc. The AI player will automatically make its move using the Minimax algorithm with Alpha-Beta pruning.

The game ends when one of the players connects four discs or there are no more empty spaces left on the board. The game will display the winner or declare a tie.
## Implementation Details
- main: Main class that handles the run of the code, including the minimax and alpha-beta algorithms calls and the function of measure the performance.
- AI_algorithms: Class that represents the AI player and implements the Minimax algorithm and Alpha-Beta pruning to determine the best move.
- board: Class that handles the board logics and the functions the help the AI algorithms and the graphical user interface using the pygame library.
