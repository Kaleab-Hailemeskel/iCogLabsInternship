# Connect Four: Adversarial AI Showdown

This directory contains a complete implementation of a Connect Four game, featuring two distinct AI strategies: **Monte Carlo Tree Search (MCTS)** and **Alpha-Beta Pruning**.

## File Overview

- `connect_four.py`: The core game engine containing the rules, board state, and win conditions.
- `play_connect_four.py`: The main entry point for the interactive game. It allows users to play against either AI agent.
- `monte_carlo_tree_serach_for_connect_four.py`: Implements the `MonteCarloTreeSearch` agent.
- `alpha_beta_prunning_for_connect_four.py`: Implements the `AlphaBetaPruning` agent.
- `__init__.py`: Makes the directory a Python package.

---

## Detailed Component Documentation

### 1. `connect_four.py`
Contains the `ConnectFour` class, which manages the game state.

#### Methods:
- `__init__(self, GAME_ROW, GAME_COL)`: Initializes the board (default 6x7) and sets the starting player to 1.
- `make_move(self, col)`: Drops a piece into the specified column. It finds the lowest available row in that column and updates the board with the current player's ID. Returns `True` if successful, `False` if the column is full.
- `check_winner(self)`: Scans the board for four consecutive pieces of the same player horizontally, vertically, or diagonally. Returns the player ID if a winner is found, else `None`.
- `get_possible_col_move(self)`: Returns a list of column indices that are not yet full.
- `is_full(self)`: Checks if the board is completely full (a draw condition).
- `switch_player(self)`: Toggles `self.current_player` between 1 and 2.
- `print_board(self)`: Utility to print the board state to the console.
- `get_repr(self)`: Returns a string representation of the board.

### 2. `monte_carlo_tree_serach_for_connect_four.py`
Contains the `MonteCarloTreeSearch` class.

#### Methods:
- `__init__(self, number_of_simulations)`: Sets how many random playouts the AI will perform per move.
- `best_move(self, curr_game, curr_player)`: 
    1.  Starts from the current state.
    2.  For each simulation, it clones the board and performs a "rollout" (randomly picking moves until the game ends).
    3.  Scores the outcome: positive if the AI wins, negative if the opponent wins.
    4.  Aggregates scores for each possible starting move and returns the one with the highest total.

### 3. `alpha_beta_prunning_for_connect_four.py`
Contains the `AlphaBetaPruning` class.

#### Methods:
- `__init__(self, depth)`: Sets the maximum search depth for the minimax tree.
- `best_move(self, curr_game, curr_player)`: The root driver. It evaluates all valid moves and uses the `_minimax` function to find the move that leads to the best possible future state.
- `_minimax(self, game, depth, alpha, beta, maximizing_player, ai_player)`:
    - Recursively explores the move tree.
    - Uses **Alpha-Beta Pruning** to "cut off" branches that cannot possibly affect the final decision, significantly improving performance.
    - If a terminal state (win/loss/draw) or the max depth is reached, it returns a score.
- `_evaluate_board(self, board, player)`: The heuristic "brain". It assigns a numerical value to a non-terminal board state by checking every possible 4-slot window (horizontal, vertical, diagonal) and scoring them based on how many pieces the AI has vs the opponent.
- `_evaluate_window(self, window, player)`: A helper for the heuristic. It gives high points for 3-in-a-row (threats) and low points for 2-in-a-row. It also heavily penalizes allowing the opponent to have a 3-in-a-row.
- `_clone_game(self, game)`: Creates a lightweight deep copy of the game state for simulations.

### 4. `play_connect_four.py`
The interactive script that ties everything together.

#### Execution Flow:
1.  Prompts the user to select an AI opponent (MCTS or Alpha-Beta).
2.  Enters a `while True` loop.
3.  If it's the Human's turn (Player 1), it takes console input.
4.  If it's the AI's turn (Player 2), it calls `ai.best_move()`.
5.  Checks for a winner or draw after every move.
6.  Switches players and repeats until the game concludes.
