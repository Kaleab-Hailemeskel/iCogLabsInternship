from connect_four import ConnectFour
from monte_carlo_tree_serach_for_connect_four import MonteCarloTreeSearch   
from alpha_beta_prunning_for_connect_four import AlphaBetaPruning

GAME_ROW, GAME_COL = 6, 7

def play_connect_four():
    print("Choose AI opponent:")
    print("1. Monte Carlo Tree Search")
    print("2. Alpha-Beta Pruning")
    choice = input("Enter choice (1 or 2): ")
    
    game = ConnectFour(GAME_ROW=GAME_ROW, GAME_COL=GAME_COL)
    
    if choice == '2':
        ai = AlphaBetaPruning(depth=5)
        print("Alpha-Beta Pruning agent selected.")
    else:
        ai = MonteCarloTreeSearch(number_of_simulations=10_000)
        print("Monte Carlo Tree Search agent selected.")
    
    while True:
        game.print_board()
        if game.current_player == 1:
            try:
                col = int(input("Player 1, enter column (0-6): "))
                if not (0 <= col < GAME_COL and game.make_move(col)):
                    print("Invalid move. Try again.")
                    continue
            except ValueError:
                print("Invalid input. Enter a number.")
                continue
        else:
            print("Player 2 (AI) is thinking...")
            col = ai.best_move(game, game.current_player)
            game.make_move(col)
        
        winner = game.check_winner()
        if winner is not None:
            game.print_board()
            print(f"Player {winner} wins!")
            break
        elif game.is_full():
            game.print_board()
            print("It's a draw!")
            break
        
        game.switch_player()

if __name__ == "__main__":
    play_connect_four()