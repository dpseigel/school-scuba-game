import pgzrun
from pgzhelper import *
import pygame.math

class Menu:
    #Initialization function - has all player variables
    def __init__(self, title, button_text, text_size):
        self.title = title
        self.button_text = button_text
        self.text_size = text_size
    
    def draw(self, screen):
        screen.draw.text(self.title, (300, 100), color="white", fontsize=self.text_size, fontname='mainfont')
        screen.draw.text(self.button_text, (350, 200), color="white", fontsize=self.text_size/1.5, fontname='mainfont')

    
    def update(self):
        pass