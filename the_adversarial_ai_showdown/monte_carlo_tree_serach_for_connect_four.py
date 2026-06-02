from collections import Counter
import copy
import random

from connect_four import ConnectFour

class MonteCarloTreeSearch:
    def __init__(self, number_of_simulations=1000):
        self.simulations = number_of_simulations
    
    def best_move(self, curr_game : ConnectFour, curr_player : int):
        evaluations = Counter()
        
        for _ in range(self.simulations):
            game_copy = ConnectFour()
            game_copy.board = copy.deepcopy(curr_game.board)
            player = curr_player
            
            next_moves = game_copy.get_possible_col_move()
            first_move, last_move = None, None
            score = curr_game.GAME_COL * curr_game.GAME_ROW
            
            while next_moves:
                
                move_index = random.randint(0, len(next_moves) - 1) 
                move = next_moves[move_index]
                game_copy.make_move(move)
                
                if first_move is None:
                    first_move = move
                last_move = move
                
                winner = game_copy.check_winner()
                if winner is not None and winner == player:
                    break
                
                score -= 1
                player = 3 - player
                next_moves = game_copy.get_possible_col_move()
            
            
            
            if player != curr_player:
                winner = game_copy.check_winner()
                if winner is not None and winner != curr_player:
                    score *= -1
                
            evaluations[first_move] += score
        
        best_move = evaluations.most_common(1)[0][0]
        
        return best_move
        
    
                
                
                
                
        

        