import pgzrun
from pgzhelper import *
import pygame.math
import game_var

class Menu:
    #Initialization function
    def __init__(self, title, button_text, text_size):
        self.title = title
        self.button_text = button_text
        self.text_size = text_size
    
    def draw(self, screen):
        screen.draw.text(self.title, (230, 200), color=game_var.text_colour, fontsize=self.text_size, fontname=game_var.text_font)
        screen.draw.text(self.button_text, (230, 250), color=game_var.text_colour, fontsize=self.text_size/1.5, fontname=game_var.text_font)

    
    def update(self):
        pass

class StatsMenu(Menu):
    #Initialization function
    def __init__(self, text, text_size, player_pos):
        self.text = text
        self.text_size = text_size
        self.pos = player_pos
    
    def draw(self, screen):
        screen.draw.text(self.text, (self.pos.x - 40, self.pos.y - 60), color=game_var.text_colour, fontsize=self.text_size, fontname=game_var.text_font)
    
    def update(self):
        pass