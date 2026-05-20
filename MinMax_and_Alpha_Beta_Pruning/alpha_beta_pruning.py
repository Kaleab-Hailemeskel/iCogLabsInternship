empty = '.'
ai, opponent = '*', '#'
player_symbols = [ai, opponent]

# global counter to track efficiency
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

def minimax_alphabeta(grid, turn, alpha, beta):
    """
    Minimax with Alpha-Beta Pruning.
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
                    score = minimax_alphabeta(grid, 1, alpha, beta)
                    grid[r][c] = empty
                    
                    best_score = max(best_score, score)
                    alpha = max(alpha, score) # Update the lower bound for MAX
                    
                    if beta <= alpha:
                        break # Beta cutoff: Opponent has a better alternative, stop searching
            if beta <= alpha:
                break
        return best_score
        
    else:          # Human Opponent's turn (MIN)
        best_score = float('inf')
        for r in range(n):
            for c in range(n):
                if grid[r][c] == empty:
                    grid[r][c] = opponent
                    score = minimax_alphabeta(grid, 0, alpha, beta)
                    grid[r][c] = empty
                    
                    best_score = min(best_score, score)
                    beta = min(beta, score) # Update the upper bound for MIN
                    
                    if beta <= alpha:
                        break # Alpha cutoff: AI has a better alternative, stop searching
            if beta <= alpha:
                break
        return best_score

def find_best_move(grid):
    """
    Root level driver for the AI using Alpha-Beta Pruning.
    """
    n = len(grid)
    best_score = float('-inf')
    best_move = (-1, -1)
    
    # Initialize Alpha as negative infinity and Beta as positive infinity
    alpha = float('-inf')
    beta = float('inf')
    
    for r in range(n):
        for c in range(n):
            if grid[r][c] == empty:
                grid[r][c] = ai
                # Evaluate this move with initial bounds
                move_score = minimax_alphabeta(grid, 1, alpha, beta)
                grid[r][c] = empty
                
                if move_score > best_score:
                    best_score = move_score
                    best_move = (r, c)
                
                # Update alpha at the root level as well
                alpha = max(alpha, best_score)
                    
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
    
    print("Welcome to Tic-Tac-Toe with Alpha-Beta Pruning! You are '#', AI is '*'")
    print_board(grid)
    
    # 1 for Human goes first, 0 for AI goes first
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
            try:
                move = input("Enter row and col numbers separated by space (e.g. 1 2): ")
                row, col = map(int, move.split())
                if grid[row][col] != empty:
                    print("That slot is already occupied! Try again.")
                    continue
                grid[row][col] = opponent
                current_turn = 0 
            except (ValueError, IndexError):
                print("Invalid input. Please enter numbers between 0 and 2.")
                continue
        else:
            print("AI is calculating best move with Alpha-Beta Pruning...")
            node_count = 0 
            row, col = find_best_move(grid)
            
            if row != -1 and col != -1:
                grid[row][col] = ai
                print(f"AI placed '*' at position: ({row}, {col})")
                print(f"Nodes evaluated with Alpha-Beta: {node_count}")
            
            current_turn = 1 
            
        print_board(grid)

if __name__ == "__main__":
    play_game()