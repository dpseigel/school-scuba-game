import pgzrun
from pgzhelper import *
import pygame.math
import menu
import game_var

#*** ALL STATIONS MUST HAVE UPDATE FUNCTION***

#Base Upgrade Station - used for all others
class Station:
    def __init__(self, sprite_image, scale, x, y):
        self.pos = pygame.Vector2(x, y)
        self.start_pos = self.pos
        self.sprite = Actor(sprite_image)
        self.sprite.scale = scale
        self.menu = None
    
    def show(self):
        self.pos = self.start_pos

    def hide(self):
        self.pos = pygame.Vector2(-1000, -1000)

    def use(self):
        print("using")

    def update(self):
        self.sprite.x = self.pos.x
        self.sprite.y = self.pos.y

#Can add custom code to each one so that there is a specific use function
class HiringStation(Station):
    def use(self):
        self.menu = menu.Menu("HIRE", "BUY", 50)

class EquipmentStation(Station):
    def use(self):
        print("Upgrading Equipment...")

class WaterCleaningStation(Station):
    def use(self):
        print("Upgrading Cleaning...")

class SwimmingStartStation(Station):
    def use(self):
        game_var.game_state = 2
        game_var.reset()