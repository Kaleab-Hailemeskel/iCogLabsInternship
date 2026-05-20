import copy

empty = '.'
ai, opponent = '*', '#'
player_symbols = [ai, opponent]

# Global counter to track performance/efficiency
node_count = 0

def evaluate_board(grid):
    """
    Evaluates the board state.
    Returns (True, score) if the game is over, or (False, 0) if it is ongoing.
    """
    n = len(grid)
    
    # Check Columns
    for col in range(n):
        if all(grid[i][col] == grid[i - 1][col] and grid[i - 1][col] != empty for i in range(1, n)):
            return True, (1 if grid[0][col] == ai else -1)

    # Check Rows
    for row in range(n):
        if all(grid[row][i] == grid[row][i - 1] and grid[row][i - 1] != empty for i in range(1, n)):
            return True, (1 if grid[row][0] == ai else -1)
    
    # Check Diagonals
    if all(grid[i][i] == grid[i - 1][i - 1] and grid[i - 1][i - 1] != empty for i in range(1, n)):
        return True, (1 if grid[0][0] == ai else -1)
    
    if all(grid[i][n - i - 1] == grid[i - 1][n - (i - 1) - 1] and grid[i - 1][n - (i - 1) - 1] != empty for i in range(1, n)):
        return True, (1 if grid[0][n - 1] == ai else -1)
    
    # Check for Draw
    for r in range(n):
        for c in range(n):
            if grid[r][c] == empty:
                return False, 0 
                
    return True, 0 

def minimax(grid, turn):
    """
    Standard Minimax tracking recursive game states.
    Increments node_count on every execution.
    """
    global node_count
    node_count += 1
    
    is_over, score = evaluate_board(grid)
    if is_over:
        return score
    
    n = len(grid)
    
    if turn == 0:  # AI's turn (MAX)
        best_score = float('-inf')
        for r in range(n):
            for c in range(n):
                if grid[r][c] == empty:
                    grid[r][c] = ai
                    score = minimax(grid, 1)
                    grid[r][c] = empty
                    best_score = max(best_score, score)
        return best_score
        
    else:          # Human Opponent's turn (MIN)
        best_score = float('inf')
        for r in range(n):
            for c in range(n):
                if grid[r][c] == empty:
                    grid[r][c] = opponent
                    score = minimax(grid, 0)
                    grid[r][c] = empty
                    best_score = min(best_score, score)
        return best_score

def find_best_move(grid):
    """
    Root level driver for the AI. Iterates through immediate moves 
    and returns the best coordinates (row, col).
    """
    n = len(grid)
    best_score = float('-inf')
    best_move = (-1, -1)
    
    for r in range(n):
        for c in range(n):
            if grid[r][c] == empty:
                grid[r][c] = ai
                # Evaluate the outcome of this move
                move_score = minimax(grid, 1)
                grid[r][c] = empty
                
                if move_score > best_score:
                    best_score = move_score
                    best_move = (r, c)
                    
    return best_move

def print_board(grid):
    print("\n  0 1 2")
    for idx, row in enumerate(grid):
        print(f"{idx} {' '.join(row)}")
    print()

def play_game():
    global node_count
    n = 3
    grid = [[empty] * n for _ in range(n)]
    
    print("Welcome to Tic-Tac-Toe! You are '#', AI is '*'")
    print_board(grid)
    
    # Let's decide who goes first (0 for AI, 1 for Human)
    current_turn = 1 
    
    while True:
        is_over, score = evaluate_board(grid)
        if is_over:
            if score == 1:
                print("Game Over: The AI wins!")
            elif score == -1:
                print("Game Over: Wow! You beat the AI!")
            else:
                print("Game Over: It's a draw!")
            break
            
        if current_turn == 1:
            # --- Human Player Move ---
            try:
                move = input("Enter row and col numbers separated by space (e.g. 1 2): ")
                row, col = map(int, move.split())
                if grid[row][col] != empty:
                    print("That slot is already occupied! Try again.")
                    continue
                grid[row][col] = opponent
                current_turn = 0 # Pass turn to AI
            except (ValueError, IndexError):
                print("Invalid input. Please enter valid rows and cols between 0 and 2.")
                continue
        else:
            # --- AI Engine Move ---
            print("AI is calculating best move...")
            node_count = 0 # Reset counter right before calculation
            row, col = find_best_move(grid)
            
            if row != -1 and col != -1:
                grid[row][col] = ai
                print(f"AI placed '*' at position: ({row}, {col})")
                print(f"Nodes evaluated by Minimax for this turn: {node_count}")
            
            current_turn = 1 # Pass turn to Human
            
        print_board(grid)

if __name__ == "__main__":
    play_game()