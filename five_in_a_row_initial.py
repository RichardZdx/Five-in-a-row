import pygame


class Pos():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y


class Settings():
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 1000
        self.bg_color = (120, 60, 80)
        self.font = pygame.font.SysFont("comicsansms", 72)
        self.hint = pygame.font.SysFont("comicsansms", 30)


class Chess():
    def __init__(self):
        self.hori = 1
        self.vert = 1
        self.lt = 1
        self.rt = 1
        self.sign = 0

    def set_to_black(self):
        self.sign = -1

    def set_to_white(self):
        self.sign = 1

    def get_max(self):
        return max(self.hori, self.vert, self.lt, self.rt)


class Board():
    def __init__(self, width):
        self.chess_board = [[0]*width for row in range(width)]
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
            self.board_copy[pos.x][pos.y].rt = self.board_copy[pos.x + 1][pos.y + 1].rt
            i += 1
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


def main():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((
        settings.screen_height, settings.screen_width))
    font = settings.font
    hint = settings.hint
    black_win_text = font.render("Black win", True, (0, 0, 0))
    white_win_text = font.render("White win", True, (255, 255, 255))
    hint_text = hint.render("r to restart, q to quit", True, (90, 180, 50))
    turn_text = hint.render("Waiting for ", True, (200, 140, 100))
    board = Board(int(settings.screen_width / 60))
    running = True
    flag = 1
    winning = False
    while running:
        screen.fill(settings.bg_color)
        color = (255, 255, 255)
        white = (255, 255, 255)
        black = (0, 0, 0)
        i = 0
        while i <= board.width:
            pygame.draw.line(screen, color, (i*60, 0), (i*60, board.width*60))
            pygame.draw.line(screen, color, (0, i*60), (board.width*60, i*60))
            i += 1
        screen.blit(
            turn_text, (50, board.width*60+10))
        if flag == 1:
            pygame.draw.rect(screen, black, (180, board.width*60+5, 30, 30))
        else:
            pygame.draw.rect(screen, white, (180, board.width*60+5, 30, 30))
        for i in range(len(board.chess_board)):
            for j in range(len(board.chess_board[i])):
                if(board.chess_board[i][j] == 1):
                    pygame.draw.rect(screen, white,
                                     (i*60+1, j*60+1, 59, 59))
                elif (board.chess_board[i][j] == -1):
                    pygame.draw.rect(screen, black,
                                     (i*60+1, j*60+1, 59, 59))
        if winning == True:
            screen.blit(
                hint_text, (settings.screen_height - 200, settings.screen_width - 200))
            if flag == 1:
                screen.blit(
                    white_win_text, (settings.screen_height / 2 - 100, settings.screen_width / 2 - 100))
            else:
                screen.blit(
                    black_win_text, (settings.screen_height / 2 - 100, settings.screen_width / 2 - 100))

        waiting = True
        pygame.display.update()
        while winning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_r:
                        board = Board(int(settings.screen_width / 60))
                        winning = False
                    elif event.key == pygame.K_q:
                        winning = False
                        running = False
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_q:
                        winning = False
                        running = False
                        waiting = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    pos_x = int(x / 60)
                    pos_y = int(y / 60)
                    pos = Pos(pos_x, pos_y)
                    chess = Chess()
                    if flag == 1:
                        chess.set_to_black()
                    else:
                        chess.set_to_white()
                    result = board.update(chess, pos)
                    if result == True:
                        if flag == 1:
                            print("Black wins")
                        else:
                            print("White wins")
                        winning = True
                    if result is not None:
                        waiting = False
        flag *= -1


main()
