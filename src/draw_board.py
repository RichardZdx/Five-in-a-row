import pygame


def draw_screen(chess_choosing, board, screen, settings, hint, white, black):
    screen.fill(settings.bg_color)
    pvp_text = hint.render("pvp ", True, (200, 140, 100))
    pve_text = hint.render("pve ", True, (200, 140, 100))
    pygame.draw.rect(
        screen, white, (board.width * 11, board.width*30+5, 100, 50))
    if chess_choosing == True:
        pygame.draw.rect(
            screen, black, (board.width * 42, board.width*30+5, 100, 50))
    elif chess_choosing == False:
        pygame.draw.rect(
            screen, white, (board.width * 42, board.width*30+5, 100, 50))
        screen.blit(
            pvp_text, (board.width * 11 + 30, board.width*30+15))
        screen.blit(
            pve_text, (board.width * 42 + 30, board.width*30+15))
    pygame.display.update()
