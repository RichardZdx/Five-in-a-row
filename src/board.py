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
        j = 1
        while pos.x + j < self.width and self.chess_board[pos.x + j][pos.y] == chess.sign:
            self.board_copy[pos.x + j][pos.y].vert += 1
            if i > 1 and j == 1:
                self.board_copy[pos.x][pos.y].vert += self.board_copy[pos.x + 1][pos.y].vert
                self.board_copy[pos.x][pos.y].vert -= 1
            elif i == 1:
                self.board_copy[pos.x][pos.y].vert = self.board_copy[pos.x + 1][pos.y].vert
            j += 1
        if i > 1 and j > 1:
            for k in range(1, i):
                self.board_copy[pos.x -
                                k][pos.y].vert = self.board_copy[pos.x][pos.y].vert
            for k in range(1, j):
                self.board_copy[pos.x +
                                k][pos.y].vert = self.board_copy[pos.x][pos.y].vert
        for k in range(i, pos.x + 1):
            if self.chess_board[pos.x - k][pos.y] != 0:
                break
            self.board_copy[pos.x][pos.y].left_ex += 1
        for k in range(j, self.width - pos.x):
            if self.chess_board[pos.x + k][pos.y] != 0:
                break
            self.board_copy[pos.x][pos.y].right_ex += 1
        # horizon
        i = 1
        while pos.y - i >= 0 and self.chess_board[pos.x][pos.y - i] == chess.sign:
            self.board_copy[pos.x][pos.y - i].hori += 1
            self.board_copy[pos.x][pos.y].hori = self.board_copy[pos.x][pos.y - 1].hori
            i += 1
        j = 1
        while pos.y + j < self.width and self.chess_board[pos.x][pos.y + j] == chess.sign:
            self.board_copy[pos.x][pos.y + j].hori += 1
            if i > 1 and j == 1:
                self.board_copy[pos.x][pos.y].hori += self.board_copy[pos.x][pos.y + 1].hori
                self.board_copy[pos.x][pos.y].hori -= 1
            elif i == 1:
                self.board_copy[pos.x][pos.y].hori = self.board_copy[pos.x][pos.y + 1].hori
            j += 1
        if i > 1 and j > 1:
            for k in range(1, i):
                self.board_copy[pos.x][pos.y -
                                       k].hori = self.board_copy[pos.x][pos.y].hori
            for k in range(1, j):
                self.board_copy[pos.x][pos.y +
                                       k].hori = self.board_copy[pos.x][pos.y].hori
        for k in range(i, pos.y + 1):
            if self.chess_board[pos.x][pos.y - k] != 0:
                break
            self.board_copy[pos.x][pos.y].top_ex += 1
        for k in range(j, self.width - pos.y):
            if self.chess_board[pos.x][pos.y + k] != 0:
                break
            self.board_copy[pos.x][pos.y].bot_ex += 1
        # left top to right bot
        i = 1
        while pos.y - i >= 0 and pos.x - i >= 0 and self.chess_board[pos.x - i][pos.y - i] == chess.sign:
            self.board_copy[pos.x - i][pos.y - i].lt += 1
            self.board_copy[pos.x][pos.y].lt = self.board_copy[pos.x - 1][pos.y - 1].lt
            i += 1
        j = 1
        while pos.y + j < self.width and pos.x + j < self.width and self.chess_board[pos.x + j][pos.y + j] == chess.sign:
            self.board_copy[pos.x + j][pos.y + j].lt += 1
            if i > 1 and j == 1:
                self.board_copy[pos.x][pos.y].lt += self.board_copy[pos.x + 1][pos.y + 1].lt
                self.board_copy[pos.x][pos.y].lt -= 1
            elif i == 1:
                self.board_copy[pos.x][pos.y].lt = self.board_copy[pos.x + 1][pos.y + 1].lt
            j += 1
        if i > 1 and j > 1:
            for k in range(1, i):
                self.board_copy[pos.x - k][pos.y -
                                           k].lt = self.board_copy[pos.x][pos.y].lt
            for k in range(1, j):
                self.board_copy[pos.x + k][pos.y +
                                           k].lt = self.board_copy[pos.x][pos.y].lt
        # right top to left bot
        border = min(pos.y + 1, pos.x + 1)
        for k in range(i, border):
            if self.chess_board[pos.x - k][pos.y - k] != 0:
                break
            self.board_copy[pos.x][pos.y].lt_ex += 1
        border = min(self.width - pos.y, self.width - pos.x)
        for k in range(j, border):
            if self.chess_board[pos.x + k][pos.y + k] != 0:
                break
            self.board_copy[pos.x][pos.y].rb_ex += 1
        i = 1
        while pos.y + i < self.width and pos.x - i >= 0 and self.chess_board[pos.x - i][pos.y + i] == chess.sign:
            self.board_copy[pos.x - i][pos.y + i].rt += 1
            self.board_copy[pos.x][pos.y].rt = self.board_copy[pos.x - 1][pos.y + 1].rt
            i += 1
        j = 1
        while pos.y - j >= 0 and pos.x + j < self.width and self.chess_board[pos.x + j][pos.y - j] == chess.sign:
            self.board_copy[pos.x + j][pos.y - j].rt += 1
            if i > 1 and j == 1:
                self.board_copy[pos.x][pos.y].rt += self.board_copy[pos.x + 1][pos.y - 1].rt
                self.board_copy[pos.x][pos.y].rt -= 1
            elif i == 1:
                self.board_copy[pos.x][pos.y].rt = self.board_copy[pos.x + 1][pos.y - 1].rt
            j += 1
        if i > 1 and j > 1:
            for k in range(1, i):
                self.board_copy[pos.x - k][pos.y +
                                           k].rt = self.board_copy[pos.x][pos.y].rt
            for k in range(1, j):
                self.board_copy[pos.x + k][pos.y -
                                           k].rt = self.board_copy[pos.x][pos.y].rt
        border = min(self.width - pos.y, pos.x + 1)
        for k in range(i, border):
            if self.chess_board[pos.x - k][pos.y + k] != 0:
                break
            self.board_copy[pos.x][pos.y].lb_ex += 1
        border = min(self.width - pos.x, pos.y + 1)
        for k in range(i, border):
            if self.chess_board[pos.x + k][pos.y - k] != 0:
                break
            self.board_copy[pos.x][pos.y].rt_ex += 1
        chess.top_ex = self.board_copy[pos.x][pos.y].top_ex
        chess.bot_ex = self.board_copy[pos.x][pos.y].bot_ex
        chess.left_ex = self.board_copy[pos.x][pos.y].left_ex
        chess.right_ex = self.board_copy[pos.x][pos.y].right_ex
        chess.lt_ex = self.board_copy[pos.x][pos.y].lt_ex
        chess.rt_ex = self.board_copy[pos.x][pos.y].rt_ex
        chess.lb_ex = self.board_copy[pos.x][pos.y].lb_ex
        chess.rb_ex = self.board_copy[pos.x][pos.y].rb_ex
        chess.hori = self.board_copy[pos.x][pos.y].hori
        chess.vert = self.board_copy[pos.x][pos.y].vert
        chess.lt = self.board_copy[pos.x][pos.y].lt
        chess.rt = self.board_copy[pos.x][pos.y].rt
        result = self.board_copy[pos.x][pos.y].get_max()
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
