GAME_ROW, GAME_COL = 6, 7

class ConnectFour:
    def __init__(self, GAME_ROW=GAME_ROW, GAME_COL=GAME_COL):
        self.GAME_ROW = GAME_ROW
        self.GAME_COL = GAME_COL
        self.board = [[0 for _ in range(self.GAME_COL)] for _ in range(self.GAME_ROW)]
        self.current_player = 1

    def make_move(self, col):
        for row in range(self.GAME_ROW-1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                return True
        return False

    def check_winner(self):
        # Check horizontal, vertical, and diagonal for a winner
        for row in range(self.GAME_ROW):
            for col in range(self.GAME_COL):
                if self.board[row][col] != 0:
                    player = self.board[row][col]
                    # Check horizontal
                    if col + 3 < self.GAME_COL and all(self.board[row][col+i] == player for i in range(4)):
                        return player
                    # Check vertical
                    if row + 3 < self.GAME_ROW and all(self.board[row+i][col] == player for i in range(4)):
                        return player
                    # Check diagonal (bottom-left to top-right)
                    if row + 3 < self.GAME_ROW and col - 3 >= 0 and all(self.board[row+i][col-i] == player for i in range(4)):
                        return player
                    # Check diagonal (top-left to bottom-right)
                    if row - 3 >= 0 and col + 3 < self.GAME_COL and all(self.board[row-i][col+i] == player for i in range(4)):
                        return player
        return None

    def get_possible_col_move(self):
        return [col for col in range(self.GAME_COL) if self.board[0][col] == 0]

    def is_full(self):
        return all(self.board[0][col] != 0 for col in range(self.GAME_COL))

    def switch_player(self):
        self.current_player = 3 - self.current_player
    
    def print_board(self):
        for row in self.board:
            print(' '.join(str(cell) for cell in row))
        print()
        
    def get_repr(self):
        return '\n'.join(' '.join(str(cell) for cell in row) for row in self.board)
        
        

