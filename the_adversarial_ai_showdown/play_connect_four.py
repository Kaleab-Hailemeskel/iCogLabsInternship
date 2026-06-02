import time
from connect_four import ConnectFour
from monte_carlo_tree_serach_for_connect_four import MonteCarloTreeSearch   
from alpha_beta_prunning_for_connect_four import AlphaBetaPruning

GAME_ROW, GAME_COL = 6, 7

def get_agent(choice):
    if choice == '1':
        return "Human"
    elif choice == '2':
        return MonteCarloTreeSearch(number_of_simulations=5_000)
    elif choice == '3':
        return AlphaBetaPruning(depth=5)
    return None

def play_connect_four():
    print("Welcome to Connect Four!")
    print("Select Player 1 type:")
    print("1. Human")
    print("2. Monte Carlo Tree Search")
    print("3. Alpha-Beta Pruning")
    p1_type = get_agent(input("Choice: "))
    
    print("\nSelect Player 2 type:")
    print("1. Human")
    print("2. Monte Carlo Tree Search")
    print("3. Alpha-Beta Pruning")
    p2_type = get_agent(input("Choice: "))
    
    game = ConnectFour(GAME_ROW=GAME_ROW, GAME_COL=GAME_COL)
    players = {1: p1_type, 2: p2_type}
    
    while True:
        game.print_board()
        current_agent = players[game.current_player]
        
        if current_agent == "Human":
            try:
                col = int(input(f"Player {game.current_player} (Human), enter column (0-6): "))
                if not (0 <= col < GAME_COL and game.make_move(col)):
                    print("Invalid move. Try again.")
                    continue
            except ValueError:
                print("Invalid input. Enter a number.")
                continue
        else:
            agent_name = "MCTS" if isinstance(current_agent, MonteCarloTreeSearch) else "Alpha-Beta"
            print(f"Player {game.current_player} ({agent_name}) is thinking...")
            col = current_agent.best_move(game, game.current_player)
            game.make_move(col)
            if players[1] != "Human" and players[2] != "Human":
                time.sleep(1) # Slow down AI vs AI for visibility
        
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