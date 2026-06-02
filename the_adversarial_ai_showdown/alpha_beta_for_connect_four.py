import copy
import math

class AlphaBetaPruning:
    def __init__(self, depth=5):
        self.depth = depth

    def best_move(self, curr_game, curr_player):
        best_score = -math.inf
        valid_moves = curr_game.get_possible_col_move()
        best_col = valid_moves[0] if valid_moves else 0
        
        # Center column preference
        valid_moves.sort(key=lambda x: abs(x - curr_game.GAME_COL // 2))

        for col in valid_moves:
            game_copy = self._clone_game(curr_game)
            game_copy.make_move(col)
            
            # Check if this move wins immediately
            if game_copy.check_winner() == curr_player:
                return col
            
            game_copy.switch_player()
            score = self._minimax(game_copy, self.depth - 1, -math.inf, math.inf, False, curr_player)
            
            if score > best_score:
                best_score = score
                best_col = col
                
        return best_col

    def _minimax(self, game, depth, alpha, beta, maximizing_player, ai_player):
        winner = game.check_winner()
        is_terminal = winner is not None or game.is_full()
        
        if depth == 0 or is_terminal:
            if is_terminal:
                if winner == ai_player:
                    return 1000000000
                elif winner == (3 - ai_player):
                    return -1000000000
                else: # Draw
                    return 0
            else:
                return self._evaluate_board(game.board, ai_player)

        valid_moves = game.get_possible_col_move()
        # Order moves to improve pruning efficiency (center first)
        valid_moves.sort(key=lambda x: abs(x - game.GAME_COL // 2))

        if maximizing_player:
            value = -math.inf
            for col in valid_moves:
                game_copy = self._clone_game(game)
                game_copy.make_move(col)
                game_copy.switch_player()
                value = max(value, self._minimax(game_copy, depth - 1, alpha, beta, False, ai_player))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = math.inf
            for col in valid_moves:
                game_copy = self._clone_game(game)
                game_copy.make_move(col)
                game_copy.switch_player()
                value = min(value, self._minimax(game_copy, depth - 1, alpha, beta, True, ai_player))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

    def _evaluate_board(self, board, player):
        score = 0
        opponent = 3 - player
        
        # Center column score
        center_array = [board[r][3] for r in range(6)]
        center_count = center_array.count(player)
        score += center_count * 3

        # Horizontal score
        for r in range(6):
            row_array = board[r]
            for c in range(4):
                window = row_array[c:c+4]
                score += self._evaluate_window(window, player)

        # Vertical score
        for c in range(7):
            col_array = [board[r][c] for r in range(6)]
            for r in range(3):
                window = col_array[r:r+4]
                score += self._evaluate_window(window, player)

        # Positive diagonal score
        for r in range(3):
            for c in range(4):
                window = [board[r+i][c+i] for i in range(4)]
                score += self._evaluate_window(window, player)

        # Negative diagonal score
        for r in range(3):
            for c in range(3, 7):
                window = [board[r+i][c-i] for i in range(4)]
                score += self._evaluate_window(window, player)

        return score

    def _evaluate_window(self, window, player):
        score = 0
        opponent = 3 - player

        if window.count(player) == 4:
            score += 100
        elif window.count(player) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(player) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opponent) == 3 and window.count(0) == 1:
            score -= 4
            
        return score

    def _clone_game(self, game):
        # We need a fast way to clone the game state
        from connect_four import ConnectFour
        new_game = ConnectFour(game.GAME_ROW, game.GAME_COL)
        new_game.board = [row[:] for row in game.board]
        new_game.current_player = game.current_player
        return new_game
