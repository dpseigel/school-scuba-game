import pgzrun
from pgzhelper import *
import pygame.math
import game_var

#*** ALL ACTORS MUST HAVE UPDATE FUNCTION***

class BuildingPlayer:
    #Initialization function - has all player variables
    def __init__(self, speed, scale,  x, y):
        self.speed = speed
        self.pos = pygame.Vector2(x, y)
        self.sprite = Actor('player')
        self.sprite.scale = scale
    
    #Receives input from the main script - moves pos variable
    def move(self, direction):
        if game_var.game_state == 1:
            self.pos += direction * self.speed

    #Actually moves the sprite
    def movement(self):
        self.sprite.x = self.pos.x
        self.sprite.y = self.pos.y
    
    def update(self):
        if game_var.game_state == 1:
            self.movement()

class SwimmingPlayer:
    #Initialization function - has all player variables
    def __init__(self, speed, scale, gravity,  x, y):
        self.speed = speed
        self.pos = pygame.Vector2(x, y)
        self.sprite = Actor('player')
        self.sprite.scale = scale
        self.gravity = gravity
    
    #Receives input from the main script - moves pos variable
    def move(self, direction):
        if game_var.game_state == 2:
            self.pos += direction * self.speed
            self.pos.y += self.gravity

    #Actually moves the sprite
    def movement(self):
        self.sprite.x = self.pos.x
        self.sprite.y = self.pos.y
    
    def update(self):
        self.movement()