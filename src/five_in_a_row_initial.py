import pygame
import copy
import random
from time import sleep
from chess import Chess
from settings import Settings
from settings import Pos
from board import Board
import draw_board


def get_conti(chess, board, i, j):
    if i + 1 < board.width and board.chess_board[i + 1][j] == chess.sign:
        chess.vert = board.board_copy[i + 1][j].vert + 1
    if i - 1 >= 0 and board.chess_board[i - 1][j] == chess.sign:
        chess.vert += board.board_copy[i - 1][j].vert
    if j + 1 < board.width and board.chess_board[i][j + 1] == chess.sign:
        chess.hori = board.board_copy[i][j + 1].hori + 1
    if j - 1 >= 0 and board.chess_board[i][j - 1] == chess.sign:
        chess.hori += board.board_copy[i][j - 1].hori
    if j + 1 < board.width and i + 1 < board.width and board.chess_board[i + 1][j + 1] == chess.sign:
        chess.lt = board.board_copy[i +
                                    1][j + 1].lt + 1
    if j - 1 >= 0 and i - 1 >= 0 and board.chess_board[i - 1][j - 1] == chess.sign:
        chess.lt += board.board_copy[i - 1][j - 1].lt
    if j + 1 < board.width and i - 1 >= 0 and board.chess_board[i - 1][j + 1] == chess.sign:
        chess.rt = board.board_copy[i -
                                    1][j + 1].rt + 1
    if j - 1 >= 0 and i + 1 < board.width and board.chess_board[i + 1][j - 1] == chess.sign:
        chess.rt += board.board_copy[i + 1][j - 1].rt


def get_extensive(board, chess):
    vert_ex = min(chess.top_ex, chess.bot_ex)
    hori_ex = min(chess.left_ex, chess.right_ex)
    lt_ex = min(chess.lt_ex, chess.rb_ex)
    rt_ex = min(chess.rt_ex, chess.lb_ex)
    ver_ratio = float(vert_ex) / float(len(board.chess_board))
    hori_ratio = float(hori_ex) / float(len(board.chess_board))
    lt_ratio = float(lt_ex) / float(len(board.chess_board))
    rt_ratio = float(rt_ex) / float(len(board.chess_board))
    extensive = ver_ratio + ver_ratio + lt_ratio + rt_ratio
    return extensive


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
    pos = Pos(-1, -1)
    winning = False
    mode = 0
    color = (255, 255, 255)
    white = (255, 255, 255)
    black = (0, 0, 0)
    weight_own = [0, 10, 20, 50, 100, 1000]
    weight_ene = [0, 10, 20, 50, 100, 1000]
    mode_choosing = True
    chess_choosing = False
    ai_working = False
    default_chess = 1
    while running:
        while mode_choosing or chess_choosing:
            draw_board.draw_screen(chess_choosing, board,
                                   screen, settings, hint, white, black)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_q:
                        mode_choosing = False
                        running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if x >= 180 and x <= 280 and y >= board.width*30+5 and y <= board.width*30+55:
                        if chess_choosing == False:
                            mode = 0
                            mode_choosing = False
                            chess_choosing = False
                            break
                        else:
                            chess_choosing = False
                            mode = 1
                            default_chess = -1
                            break

                    elif x >= 680 and x <= 780 and y >= board.width*30+5 and y <= board.width*30+55:
                        if chess_choosing == False:
                            mode = 1
                            mode_choosing = False
                            chess_choosing = True
                            break
                        elif chess_choosing == True:
                            mode = 1
                            mode_choosing = False
                            chess_choosing = False
                            default_chess = 1
                            break

        if running == True:
            screen.fill(settings.bg_color)
            i = 0
            while i <= board.width:
                pygame.draw.line(screen, color, (i*60, 0),
                                 (i*60, board.width*60))
                pygame.draw.line(screen, color, (0, i*60),
                                 (board.width*60, i*60))
                i += 1
            screen.blit(
                turn_text, (50, board.width*60+10))
            if flag == 1:
                pygame.draw.rect(
                    screen, black, (180, board.width*60+5, 30, 30))
            else:
                pygame.draw.rect(
                    screen, white, (180, board.width*60+5, 30, 30))
            for i in range(len(board.chess_board)):
                for j in range(len(board.chess_board[i])):
                    if(board.chess_board[i][j] == 1):
                        pygame.draw.circle(screen, white,
                                           (i * 60 + 30, j * 60 + 30), 29)
                    elif (board.chess_board[i][j] == -1):
                        pygame.draw.circle(screen, black,
                                           (i * 60 + 30, j * 60 + 30), 29)
            if winning == False and pos.x != -1:
                i = pos.x
                j = pos.y
                for count in range(10):
                    r = random.randint(0, 255)
                    g = random.randint(0, 255)
                    b = random.randint(0, 250)
                    chess_color = (r, g, b)
                    pygame.draw.circle(screen, chess_color,
                                       (i * 60 + 30, j * 60 + 30), 29)
                    pygame.display.update()
                    sleep(0.1)
                if board.chess_board[i][j] == 1:
                    pygame.draw.circle(screen, white,
                                       (i * 60 + 30, j * 60 + 30), 29)
                else:
                    pygame.draw.circle(screen, black,
                                       (i * 60 + 30, j * 60 + 30), 29)
            if winning == True:
                screen.fill(settings.bg_color)
                screen.blit(
                    hint_text, (board.width*60-200, board.width*60+10))
                if flag == 1:
                    screen.blit(
                        white_win_text, (settings.screen_height / 2 - 100, settings.screen_width / 2 - 100))
                else:
                    screen.blit(
                        black_win_text, (settings.screen_height / 2 - 100, settings.screen_width / 2 - 100))

            waiting = True
            if mode == 1 and flag != default_chess:
                waiting = False
                ai_working = True
            pygame.display.update()
            while winning:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_r:
                            board = Board(int(settings.screen_width / 60))
                            winning = False
                            waiting = False
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
            if ai_working:
                virtual_own_chess_sample = Chess()
                virtual_enemy_chess_sample = Chess()
                real_chess = Chess()
                if default_chess == -1:
                    real_chess.set_to_black()
                    virtual_own_chess_sample.set_to_black()
                    virtual_enemy_chess_sample.set_to_white()
                else:
                    real_chess.set_to_white()
                    virtual_own_chess_sample.set_to_white()
                    virtual_enemy_chess_sample.set_to_black()
                max_own_point = 0
                max_ene_point = 0
                pos_own_x = 0
                pos_own_y = 0
                pos_ene_x = 0
                pos_ene_y = 0
                for i in range(len(board.chess_board)):
                    for j in range(len(board.chess_board[i])):
                        if board.chess_board[i][j] == 0:
                            virtual_enemy_chess = copy.deepcopy(
                                virtual_enemy_chess_sample)
                            virtual_own_chess = copy.deepcopy(
                                virtual_own_chess_sample)
                            tmp_own_board = copy.deepcopy(board)
                            tmp_ene_board = copy.deepcopy(board)
                            tmp_pos = Pos(i, j)
                            tmp_own_board.detect_conti(
                                tmp_pos, virtual_own_chess)
                            tmp_ene_board.detect_conti(
                                tmp_pos, virtual_enemy_chess)
                            own_hor = virtual_own_chess.hori
                            own_ver = virtual_own_chess.vert
                            own_lt = virtual_own_chess.lt
                            own_rt = virtual_own_chess.rt
                            ene_hor = virtual_enemy_chess.hori
                            ene_ver = virtual_enemy_chess.vert
                            ene_lt = virtual_enemy_chess.lt
                            ene_rt = virtual_enemy_chess.rt
                            own_exten = get_extensive(board, virtual_own_chess)
                            ene_exten = get_extensive(
                                board, virtual_enemy_chess)
                            own_value = weight_own[own_hor] + weight_own[own_ver] + \
                                weight_own[own_rt] + weight_own[own_lt]
                            ene_value = weight_ene[ene_hor] + weight_ene[ene_ver] + \
                                weight_ene[ene_rt] + weight_ene[ene_lt]
                            own_value += own_exten
                            ene_value += ene_exten
                            if own_value > max_own_point:
                                max_own_point = own_value
                                pos_own_x = i
                                pos_own_y = j
                            if ene_value > max_ene_point:
                                max_ene_point = ene_value
                                pos_ene_x = i
                                pos_ene_y = j
                if max_own_point < max_ene_point:
                    pos = Pos(pos_ene_x, pos_ene_y)
                else:
                    pos = Pos(pos_own_x, pos_own_y)
                result = board.update(real_chess, pos)
                if result == True:
                    if flag == 1:
                        print("Black wins")
                    else:
                        print("White wins")
                    winning = True
            flag *= -1
            ai_working = False


main()
