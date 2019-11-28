import pygame
import copy
from chess import Chess
from settings import Settings
from settings import Pos
from board import Board
import draw_board


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
                        pygame.draw.rect(screen, white,
                                         (i*60+1, j*60+1, 59, 59))
                    elif (board.chess_board[i][j] == -1):
                        pygame.draw.rect(screen, black,
                                         (i*60+1, j*60+1, 59, 59))
            if winning == True:
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
                viturl_own_chess_sample = Chess()
                viturl_enemy_chess_sample = Chess()
                real_chess = Chess()
                if default_chess == -1:
                    real_chess.set_to_black()
                    viturl_own_chess_sample.set_to_black()
                    viturl_enemy_chess_sample.set_to_white()
                else:
                    real_chess.set_to_white()
                    viturl_own_chess_sample.set_to_white()
                    viturl_enemy_chess_sample.set_to_black()
                max_own_point = 0
                max_ene_point = 0
                pos_own_x = 0
                pos_own_y = 0
                pos_ene_x = 0
                pos_ene_y = 0
                for i in range(len(board.chess_board)):
                    for j in range(len(board.chess_board[i])):
                        if board.chess_board[i][j] == 0:
                            viturl_enemy_chess = copy.deepcopy(
                                viturl_enemy_chess_sample)
                            viturl_own_chess = copy.deepcopy(
                                viturl_own_chess_sample)
                            tmp_own_board = copy.deepcopy(board)
                            tmp_ene_board = copy.deepcopy(board)
                            tmp_pos = Pos(i, j)
                            tmp_ene_board.detect_conti(
                                tmp_pos, viturl_enemy_chess)
                            tmp_own_board.detect_conti(
                                tmp_pos, viturl_own_chess)

                            own_hor = viturl_own_chess.hori
                            own_ver = viturl_own_chess.vert
                            own_lt = viturl_own_chess.lt
                            own_rt = viturl_own_chess.rt
                            ene_hor = viturl_enemy_chess.hori
                            ene_ver = viturl_enemy_chess.vert
                            ene_lt = viturl_enemy_chess.lt
                            ene_rt = viturl_enemy_chess.rt
                            own_value = weight_own[own_hor] + weight_own[own_ver] + \
                                weight_own[own_rt] + weight_own[own_lt]
                            ene_value = weight_ene[ene_hor] + weight_ene[ene_ver] + \
                                weight_ene[ene_rt] + weight_ene[ene_lt]
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
