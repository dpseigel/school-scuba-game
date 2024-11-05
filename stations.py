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
        self.update()

    def use(self):
        print("using")

    def update(self):
        self.sprite.x = self.pos.x
        self.sprite.y = self.pos.y

#Can add custom code to each one so that there is a specific use function
class HiringStation(Station):
    def use(self):
        if self.menu:
            game_var.hired_people += 1
        else:
            self.menu = menu.Menu("HIRE", "BUY", 50)

    def value():
        return 1
    
class EquipmentStation(Station):
    def use(self):
        if self.menu:
            if game_var.money >= 5:
                game_var.money -= 5
                game_var.player_speed += 1
        else:
            self.menu = menu.Menu("UPGRADE EQ", "BUY 5$", 50)
    
    def value():
        return 2

class WaterCleaningStation(Station):
    def use(self):
        if self.menu:
            if game_var.money >= 20:
                game_var.money -= 20
                game_var.person_speed += 1
        else:
            self.menu = menu.Menu("UPGRADE WC", "BUY 20$", 50)
    def value():
        return 3

class SwimmingStartStation(Station):
    def use(self):
        print("yoooo")
        game_var.game_state = 2
        game_var.reset()
    
    def value():
        return 4