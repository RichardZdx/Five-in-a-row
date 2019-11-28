from chess import Chess


class Board():
    def __init__(self, width):
        self.chess_board = [[0
                             for col in range(width)] for row in range(width)]
        self.board_copy = [[Chess() for col in range(width)]
                           for row in range(width)]
        self.width = width

    def detect_conti(self, pos, chess):
        # vertical
        i = 1
        while pos.x - i >= 0 and self.chess_board[pos.x - i][pos.y] == chess.sign:
            self.board_copy[pos.x - i][pos.y].vert += 1
            self.board_copy[pos.x][pos.y].vert = self.board_copy[pos.x - 1][pos.y].vert
            i += 1
        i = 1
        while pos.x + i < self.width and self.chess_board[pos.x + i][pos.y] == chess.sign:
            self.board_copy[pos.x + i][pos.y].vert += 1
            self.board_copy[pos.x][pos.y].vert = self.board_copy[pos.x + 1][pos.y].vert
            i += 1
        # horizon
        i = 1
        while pos.y - i >= 0 and self.chess_board[pos.x][pos.y - i] == chess.sign:
            self.board_copy[pos.x][pos.y - i].hori += 1
            self.board_copy[pos.x][pos.y].hori = self.board_copy[pos.x][pos.y - 1].hori
            i += 1
        i = 1
        while pos.y + i < self.width and self.chess_board[pos.x][pos.y + i] == chess.sign:
            self.board_copy[pos.x][pos.y + i].hori += 1
            self.board_copy[pos.x][pos.y].hori = self.board_copy[pos.x][pos.y + 1].hori
            i += 1
        # left top to right bot
        i = 1
        while pos.y - i >= 0 and pos.x - i >= 0 and self.chess_board[pos.x - i][pos.y - i] == chess.sign:
            self.board_copy[pos.x - i][pos.y - i].lt += 1
            self.board_copy[pos.x][pos.y].lt = self.board_copy[pos.x - 1][pos.y - 1].lt
            i += 1
        i = 1
        while pos.y + i < self.width and pos.x + i < self.width and self.chess_board[pos.x + i][pos.y + i] == chess.sign:
            self.board_copy[pos.x + i][pos.y + i].lt += 1
            self.board_copy[pos.x][pos.y].lt = self.board_copy[pos.x + 1][pos.y + 1].lt
            i += 1
        # right top to left bot
        i = 1
        while pos.y + i < self.width and pos.x - i >= 0 and self.chess_board[pos.x - i][pos.y + i] == chess.sign:
            self.board_copy[pos.x - i][pos.y + i].rt += 1
            self.board_copy[pos.x][pos.y].rt = self.board_copy[pos.x - 1][pos.y + 1].rt
            i += 1
        i = 1
        while pos.y - i >= 0 and pos.x + i < self.width and self.chess_board[pos.x + i][pos.y - i] == chess.sign:
            self.board_copy[pos.x + i][pos.y - i].rt += 1
            self.board_copy[pos.x][pos.y].rt = self.board_copy[pos.x + 1][pos.y - 1].rt
            i += 1
        chess.hori = self.board_copy[pos.x][pos.y].hori
        chess.vert = self.board_copy[pos.x][pos.y].vert
        chess.lt = self.board_copy[pos.x][pos.y].lt
        chess.rt = self.board_copy[pos.x][pos.y].rt
        result = self.board_copy[pos.x][pos.y].get_max()
        if chess.sign == 1:
            print("white")
        else:
            print("black")
        print(result)
        if result == 5:
            return True
        return False

    def update(self, chess, pos):

        if pos.x < 0 or pos.y < 0 or pos.x >= self.width or pos.y >= self.width:
            return
        if chess.sign == 1 and self.chess_board[pos.x][pos.y] == 0:
            self.chess_board[pos.x][pos.y] = 1
            result = self.detect_conti(pos, chess)
            return result
        elif chess.sign == -1 and self.chess_board[pos.x][pos.y] == 0:
            self.chess_board[pos.x][pos.y] = -1
            result = self.detect_conti(pos, chess)
            return result
