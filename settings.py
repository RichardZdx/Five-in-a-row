import pygame
class Settings():
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 1000
        self.bg_color = (120, 60, 80)
        self.font = pygame.font.SysFont("comicsansms", 72)
        self.hint = pygame.font.SysFont("comicsansms", 30)
class Pos():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y
