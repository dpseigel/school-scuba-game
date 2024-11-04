import pgzrun
from pgzhelper import *
import pygame.math
import game_var
import random


#*** ALL ACTORS MUST HAVE UPDATE FUNCTION***

class Bottle:
    def __init__(self, scale, w, h):
        self.pos = pygame.Vector2(random.randint(0, w), random.randint(0, h))
        self.sprite = Actor('bottle')
        self.sprite.scale = scale
        self.movement()
    

    def movement(self):
        self.sprite.x = self.pos.x
        self.sprite.y = self.pos.y
    
    def update(self):
        if game_var.game_state == 2:
            self.movement()

class Enemy:
    def __init__(self, speed, scale, x, y, left):
        self.left = left
        self.speed = speed
        self.pos = pygame.Vector2(x, y)
        self.sprite = Actor('enemy')
        self.sprite.scale = scale
        self.movement()
    

    def movement(self):
        if self.left:
            self.pos.x += self.speed
        else:
            self.pos.x -= self.speed
        
        self.sprite.x = self.pos.x
        self.sprite.y = self.pos.y
    
    def update(self):
        if game_var.game_state == 2:
            self.movement()

class BuildingPlayer:
    #Initialization function - has all player variables
    def __init__(self, speed, scale, x, y):
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
    def __init__(self, scale, gravity,  x, y):
        self.pos = pygame.Vector2(x, y)
        self.sprite = Actor('player')
        self.sprite.scale = scale
        self.gravity = gravity
    
    #Receives input from the main script - moves pos variable
    def move(self, direction):
        if game_var.game_state == 2:
            self.pos += direction * game_var.player_speed
            self.pos.y += self.gravity

    #Actually moves the sprite
    def movement(self):
        self.sprite.x = self.pos.x
        self.sprite.y = self.pos.y
    
    def update(self):
        if self.pos.x < -10:
            self.pos.x = game_var.screen_width
        elif self.pos.x > game_var.screen_width + 10:
            self.pos.x = 0
        elif self.pos.y > game_var.screen_height + 10:
            self.pos.y = 0
        elif self.pos.y < -10:
            self.pos.y = game_var.screen_height
        self.movement()